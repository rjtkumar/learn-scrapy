"""Bypassing Restrictions - Python Scrapy Beginners Series (Part 4)
https://youtu.be/NiFuoJw0sn8?si=Mq0-84RTn2FSJ1i0"""
import scrapy
from chocolatescraper.items import ChocolateProduct # importing the scrapy item
from chocolatescraper.itemloaders import ChocolateProductLoader # importing the item loader
from urllib.parse import urlencode
import apikeys

def get_proxy_url (url):
    """Builds the proxy url"""
    proxy_params = {
        "api_key" : apikeys.scrapeops_api_key,
        "url" : url
    }
    proxy_url = "https://proxy.scrapeops.io/v1/?" + urlencode(proxy_params)
    return proxy_url 

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    
    def start_requests(self):
        """start_requests generates the first set of requests for a spider
        we could've used the default implementation but to be able to use our proxy we've written our own implementation"""
        start_url = "https://www.chocolate.co.uk/collections/all"
        yield scrapy.Request(url = get_proxy_url(start_url), callback= self.parse)

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
                # take te next_page_url and make a new url out of it to make the request through the proxy aggregator
                yield response.follow(get_proxy_url(next_page_url), callback = self.parse)