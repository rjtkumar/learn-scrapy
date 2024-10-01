# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
