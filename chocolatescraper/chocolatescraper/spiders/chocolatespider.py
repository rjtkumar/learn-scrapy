"""Cleaning & Post-Processing Scrapy Data - Python Scrapy Beginners Series (Part 2) by ScrapeOps on youtube
https://youtu.be/NkIlpHTFCIE?si=tdZ7LHLH30w_bGuz"""
import scrapy
from chocolatescraper.items import ChocolateProduct # importing the scrapy item
from chocolatescraper.itemloaders import ChocolateProductLoader # importing the item loader

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"] # domain scrapy will start scraping from

    def parse(self, response):
        products = response.css("product-item")
        
        for product in products:
            #Refactoring our code to use the ItemLoader
            chocolate = ChocolateProductLoader(item = ChocolateProduct(),selector=product)
            chocolate.add_css("name", "a.product-item-meta__title::text")
            chocolate.add_css("price", "span.price", re= '<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            # Everthing will get removevd only contents at (.*) will be loaded
            chocolate.add_css("url", "a.product-item-meta__title::attr(href)")
            yield chocolate.load_item()
        
        # Finding the link to the next page
        # >>> response.css('[rel="next"]::attr(href)').get()
        # '/collections/all?page=2'
            next_page = response.css('[rel="next"]::attr(href)').get()
            if next_page is not None:
                next_page_url = "https://www.chocolate.co.uk" + next_page
                yield response.follow(next_page_url, callback = self.parse)