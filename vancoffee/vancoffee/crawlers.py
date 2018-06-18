from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import pandas as pd
from spiders.link_spider import LinkSpider


configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    roaster_filename = 'coffee_roasters_whitelist.txt'
    domains = pd.read_csv(roaster_filename)['URL'].values
    for dom in domains:
        yield runner.crawl(LinkSpider, domain=dom)
    reactor.stop()


crawl()
reactor.run()
