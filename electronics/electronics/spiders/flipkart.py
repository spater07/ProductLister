import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from ..items import Flipkart
from scrapy.crawler import CrawlerProcess

class FlipkartspySpider(scrapy.Spider):
    name = 'flipkartSpy'

    def start_requests(self):
        query='ASUS VivoBook K15 OLED (2021) Ryzen 5 Hexa Core 5500U'

        url = 'https://flipkart.com/search?' + urlencode({'q': query})
        yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-id]')
        
        for product in products:
            fsn = product.xpath('@data-id').extract_first()
            product_url = f"https://flipkart.com/product/p/itme?pid={fsn}"

        yield scrapy.Request(url=product_url, callback=self.parse_product_page, )

    def parse_product_page(self, response):
        
        item=Flipkart()

        website=f'Flipkart'
        category=f'Electronics'
        title=response.css(".B_NuCI").css("::text").extract_first()
        price=response.css("._16Jk6d").css("::text").extract_first()
        # offers=response.xpath('//*[@class="XUp0WS"]')
        deals=response.xpath('//span[@class="_3j4Zjq row"]/li[@class="_16eBzU col"]/span[2]/text()').extract()

        item['website']=website
        item['category']=category
        item['productName']=title
        item['price']=price
        item['deals']=deals

        yield item

# process=CrawlerProcess()
# process.crawl(FlipkartspySpider)
# process.start()