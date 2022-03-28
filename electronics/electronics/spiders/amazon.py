import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from scrapy.crawler import CrawlerProcess
from ..items import Amazon

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def __init__(self, name='',**kwargs):
        
        self.query=name
        self.catg ='Electronics'
        super().__init__( **kwargs)
    
    def start_requests(self):
        # query='ASUS VivoBook K15 OLED (2021), 15.6-inch (39.62 cms) FHD OLED, Intel Core i3-1115G4 11th Gen, Thin and Light Laptop (8GB/1TB SSD/Integrated Graphics/Office 2019/Windows 10/Black/1.8 Kg), K513EA-L302TS'

        url = 'https://www.amazon.in/s?' + urlencode({'k': self.query})
        yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.in/dp/{asin}"
            yield scrapy.Request(url=product_url, callback=self.parse_product_page, meta={'asin': asin})
            
    def parse_product_page(self, response):
        item=Amazon()
        website=f'Amazon'
        category=self.catg
        title=response.css("#productTitle").css("::text").extract_first()
        price=response.css(".apexPriceToPay").css("::text").extract_first()
        deals=response.xpath('//*[@class="description"]/text()').extract()

        # products for which price is not rendered
        if not price:
            price=response.css(".a-price-whole::text").extract_first()
        
        item['website']=website
        item['category']=category
        item['productName']=title
        item['price']=price
        item['deals']=deals

        print('price')

        yield item

# process=CrawlerProcess()

# process.crawl(AmazonSpider)
# process.start()