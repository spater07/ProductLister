import scrapy

class Amazon(scrapy.Item):
    # define the fields for your item here like:
    website=scrapy.Field()
    productName = scrapy.Field()
    price=scrapy.Field()
    category=scrapy.Field()
    deals=scrapy.Field()

class Flipkart(scrapy.Item):
    # define the fields for your item here like:
    website=scrapy.Field()
    productName = scrapy.Field()
    price=scrapy.Field()
    category=scrapy.Field()
    deals=scrapy.Field()

class TatCliq(scrapy.Item):
    # define the fields for your item here like:
    website=scrapy.Field()
    productName = scrapy.Field()
    price=scrapy.Field()
    category=scrapy.Field()
    deals=scrapy.Field()