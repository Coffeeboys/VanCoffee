from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Item, Field
import pandas as pd

class MyItem(Item):
    url = Field()

class LinkSpider(CrawlSpider):
    name = "roaster"
    rules = (Rule(LxmlLinkExtractor(allow=()), callback="parse_obj", follow=True),)

    def __init__(self,domain='', **kwargs):
        self.allowed_domains = [domain]
        self.start_urls = {'http://www.' + domain + '/', }
        print domain
        print self.allowed_domains
        print self.start_urls
        super(LinkSpider, self).__init__(**kwargs)
        #self.log(self.domain)

    #roaster_filename = 'coffee_roasters_whitelist.txt'
    #allowed_domains = pd.read_csv(roaster_filename)['URL'].values
    #start_urls = ['http://' + url + '/' for url in allowed_domains]

    #allowed_domains = ['groundswellroasters.com']
    #start_urls = ['http://groundswellroasters.com/']

    def parse_obj(self, response):
        item = MyItem()
        item['url'] = []
        for link in LxmlLinkExtractor(allow=self.allowed_domains).extract_links(response):
            item['url'].append(link.url)
        return item
