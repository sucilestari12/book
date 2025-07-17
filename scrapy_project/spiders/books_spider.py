import scrapy
from scrapy.http import Request

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/']
    
    def parse(self, response):
        # Ekstrak semua buku di halaman saat ini
        books = response.css('article.product_pod')
        for book in books:
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'availability': book.css('p.instock::text').getall()[1].strip(),
                'rating': book.css('p.star-rating::attr(class)').get().split()[-1]
            }
        
        # Ekstrak link halaman berikutnya
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            # Handle relative URL
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)
