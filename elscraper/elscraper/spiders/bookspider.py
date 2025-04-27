import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_url = book.css('h3 a::attr(href)').get()
            if book_url is not None:
                yield response.follow(book_url, callback=self.parse_book_page)
        
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_book_page(self, response):
        tableRows = response.css('table tr')
        yield{
            'url' : response.url,
            'title' : response.css('.product_main h1::text').get(),
            'product_type' : tableRows[1].css('td::text').get(),
            'price_excl_tax': tableRows[2].css('td::text').get(),
            'price_incl_text': tableRows[3].css('td::text').get(),
            'tax': tableRows[4].css('td::text').get(),
            'availability': tableRows[5].css('td::text').get(),
            'num_reviews': tableRows[6].css('td::text').get(),
            'stars': response.css('p.star-rating').attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.css('p.price_color::text').get(), 
        }