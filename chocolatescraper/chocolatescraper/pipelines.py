# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import mysql.connector

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

# Declaring pipeline to convevrt GBP to USD and drop item if item has no price
class PriceToUSDPipeline:
    gbp_to_usd_rate = 1.34
    def process_item (self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            floatPrice = float(adapter['price'])
            adapter['price'] = floatPrice * self.gbp_to_usd_rate
            return item
        else:
            raise DropItem(f"Missing price in {item}")

# Declaring pipeline to drop duplicate items
class DuplicatesPipeline:
    def __init__(self):
        self.names_seen = set() 
    def process_item (self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.names_seen.add(adapter['name'])
            return item
# Just declaring won't have scrapy use our pipelines,
# We must tell Scrapy to use our pipelines explicitly through the settings.py file

class SaveToMySQLPipeline(object):
    def __init__(self):
        self.create_connection()
    
    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = "localhost",
            user = "chocolatescraper",
            password= "password",
            database = "chocolates"
            )
        self.curr = self.connection.cursor()
    def process_item (self, item, spider):
        self.store_db(item)
        return item
    def store_db (self, item):
        try:
            self.curr.execute(f"INSERT INTO chocolateproduct (name, price, url) VALUES ('{item["name"]}', {item['price']}, '{item['url']}')")
        except BaseException as e:
            print(e)
        self.connection.commit()