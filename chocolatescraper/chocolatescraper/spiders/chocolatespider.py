"""Built following : Create Your First Scrapy Spider - Python Scrapy Beginner Series [Part 1] by ScrapeOps on youtube
https://youtu.be/NkIlpHTFCIE?si=tdZ7LHLH30w_bGuz"""
import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider" # name of the spider
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"] # domain scrapy will start scraping from

    # Appropriate selector for each product found using scrapy shell and browsers dev tools
    # product.css("a.product-item-meta__title::text").get()
    # product.css("span.price").get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>', "").replace("</span>", "")
    # product.css("a.product-item-meta__title").attrib["href"]

    def parse(self, response):
        products = response.css("product-item")
        for product in products:
            yield {
                "name" : product.css("a.product-item-meta__title::text").get(),
                "price" : product.css("span.price").get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>', "").replace("</span>", ""),
                "url" : product.css("a.product-item-meta__title").attrib["href"]
            }  
                
        # Finding the link to the next page
        # >>> response.css('[rel="next"]::attr(href)').get()
        # '/collections/all?page=2'
            next_page = response.css('[rel="next"]::attr(href)').get()
            if next_page is not None:
                next_page_url = "https://www.chocolate.co.uk" + next_page
                yield response.follow(next_page_url, callback = self.parse)