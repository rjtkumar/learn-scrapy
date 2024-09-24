# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Defining our chocolate product item
class ChocolateProduct(scrapy.Item):
    # Define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
