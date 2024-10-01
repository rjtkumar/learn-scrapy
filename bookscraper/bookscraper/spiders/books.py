import scrapy
from bookscraper.items import BookscraperItem
from bookscraper.itemloaders import BookscraperItemLoader


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    base_url = "https://books.toscrape.com/"

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            book_item_loader = BookscraperItemLoader(item= BookscraperItem(), selector= book)
            book_item_loader.add_css("name", "h3 a::attr(title)")
            book_item_loader.add_css("url", "h3 a::attr(href)")
            book_item_loader.add_css("image_url", "img::attr(src)")
            book_item_loader.add_css("rating", "p.star-rating::attr(class)")
            book_item_loader.add_css("price", "div.product_price p:first-child::text")
            book_item_loader.add_css("in_stock", "p.availability::attr(class)")
            yield book_item_loader.load_item()
        
        # # To scrape next page:
        # next_page = response.css("li.next a::attr(href)").get()
        # if next_page:
        #     yield response.follow(
        #         url= next_page,
        #         callback= self.parse
        #     )