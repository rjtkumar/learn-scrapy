from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def rating_loader (rating):
    if "One" in rating: return 1
    elif "Two" in rating: return 2
    elif "Three" in rating: return 3
    elif "Four" in rating: return 4
    elif "Five" in rating: return 5
    else: return -1


class BookscraperItemLoader (ItemLoader):
    default_output_processor = TakeFirst()
    
    rating_in = MapCompose( # x = "star-rating One"
        lambda x: rating_loader(x.split(" "))
        )
    
    url_in = MapCompose( # x = 'a-light-in-the-attic_1000/index.html"
        lambda x: "https://books.toscrape.com/" + x
        )
    
    image_url_in = MapCompose( # x = ../media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg
        lambda x: "https://books.toscrape.com/" + x
        )
    
    price_in = MapCompose( # x = £51.77
        lambda x: float(x.lstrip("£"))
        )
    
    in_stock_in = MapCompose( # x = "instock availability"
        lambda x: True if x.split(" ").count("instock") else False
        )
