import json
from flask import Flask
from scrapy.crawler import CrawlerRunner

from electronics.electronics.spiders.amazon import AmazonSpider

app = Flask(__name__)
crawl_runner = CrawlerRunner()      
quotes_list = []                    
scrape_in_progress = False
scrape_complete = False

# @app.route('/scrap-data', methods=['GET'])
@app.route('/crawl')
def crawl_for_quotes():

    global scrape_in_progress
    global scrape_complete
    global productName
    productName= 'ASUS VivoBook K15 OLED (2021), 15.6-inch (39.62 cms) FHD OLED, Intel Core i3-1115G4 11th Gen, Thin and Light Laptop (8GB/1TB SSD/Integrated Graphics/Office 2019/Windows 10/Black/1.8 Kg), K513EA-L302TS'

    if not scrape_in_progress:
        scrape_in_progress = True
        global quotes_list
        
        eventual = crawl_runner.crawl(AmazonSpider,productName=productName, quotes_list=quotes_list)
        eventual.addCallback(finished_scrape)
        return 'SCRAPING'
    elif scrape_complete:
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'

@app.route('/results')
def get_results():

    global scrape_complete
    if scrape_complete:
        return json.dumps(quotes_list)
    return 'Scrape Still Progress'

def finished_scrape(null):

    global scrape_complete
    scrape_complete = True

if __name__=='__main__':
    from sys import stdout
    from twisted.logger import globalLogBeginner, textFileLogObserver
    from twisted.web import server, wsgi
    from twisted.internet import endpoints, reactor

    globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 9000)
    http_server.listen(factory)

    # start event loop
    reactor.run()
