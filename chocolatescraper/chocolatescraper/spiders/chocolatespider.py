"""Cleaning & Post-Processing Scrapy Data - Python Scrapy Beginners Series (Part 2) by ScrapeOps on youtube
https://youtu.be/NkIlpHTFCIE?si=tdZ7LHLH30w_bGuz"""
import scrapy
from chocolatescraper.items import ChocolateProduct # importing the scrapy item

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"] # domain scrapy will start scraping from

    def parse(self, response):
        products = response.css("product-item")
        
        # Refactoring to use scrapy.Items for better organization of code
        product_item = ChocolateProduct()
        for product in products:
            product_item["name"] = product.css("a.product-item-meta__title::text").get()
            product_item["price"] = product.css("span.price").get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>', "").replace("</span>", "")
            product_item["url"] = product.css("a.product-item-meta__title").attrib["href"]
            yield product_item    
        
        # Finding the link to the next page
        # >>> response.css('[rel="next"]::attr(href)').get()
        # '/collections/all?page=2'
            next_page = response.css('[rel="next"]::attr(href)').get()
            if next_page is not None:
                next_page_url = "https://www.chocolate.co.uk" + next_page
                yield response.follow(next_page_url, callback = self.parse)