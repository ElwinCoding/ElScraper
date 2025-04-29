import scrapy
from elscraper.items import BookItem

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
        book_item = BookItem()
        tableRows = response.css('table tr')

        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['upc'] = tableRows[0].css('td ::text').get()
        book_item['product_type'] = tableRows[1].css('td ::text').get()
        book_item['price_excl_tax'] = tableRows[2].css('td ::text').get()
        book_item['price_incl_tax'] = tableRows[3].css('td ::text').get()
        book_item['tax'] = tableRows[4].css('td ::text').get()
        book_item['availability']= tableRows[5].css('td ::text').get()
        book_item['num_reviews'] = tableRows[6].css('td ::text').get()
        book_item['stars'] = response.css('p.star-rating').attrib['class']
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = response.css('p.price_color ::text').get()

        yield book_item