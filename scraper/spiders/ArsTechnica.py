import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scraper.items import ArsTechnicaItem

#
# This class should crawl for links and retrieve
#
class ArstechnicaSpider(CrawlSpider):
    name = 'ArsTechnica'
    allowed_domains = ['arstechnica.com']
    start_urls = ['https://arstechnica.com']
#    custom_settings = {'CLOSESPIDER_PAGECOUNT': 20}
    headers = {
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Windows NT x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'DNT': 1,
        'Sec-Fetch-User': 'navigate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    rules = (
        # Extract category from nav header
        Rule(LinkExtractor(restrict_xpaths=['//*[@id="header-nav-primary"]/ul'])),
        # Parse Items on paginated links
        # Rule(LinkExtractor(restrict_xpaths=['//*[@id="main"]/section[1]/div[1]/ol']), callback='parse_item'),
        # Extract 2nd page links
        Rule(LinkExtractor(restrict_xpaths=['//*[@id="main"]/div/a[1]']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for sel in response.xpath('//*[@id="main"]/section[1]/div[1]/ol/li'):
            item = ArsTechnicaItem()
            item['article_id'] = sel.xpath('@data-post-id').extract()
            item['date'] = sel.xpath('header/p[@class="byline"]/time/@datetime').get()
            item['title'] = sel.xpath('header/h2/a/text()').get().encode('ascii', 'ignore').decode('utf-8').strip()
            item['author'] = sel.xpath('header/p[@class="byline"]/a/span/text()').get().encode('ascii', 'ignore').decode('utf-8').strip()
            item['author_url'] = sel.xpath('header/p[@class="byline"]/a/@href').get()
            item['post_url'] = sel.xpath('a/@href').get()
            item['excerpt'] = sel.xpath('header/p[@class="excerpt"]/text()').get().encode('ascii', 'ignore').decode('utf-8').strip()
            url = sel.xpath('a/@href').get()
            yield response.follow(url, self.parse_page, cb_kwargs=dict(item=item))

    def parse_page(self, response, item):
        item['content'] = response.xpath('//*[@id="main"]/article/div[1]/div[1]/section/div/p/text()').getall()
        item['image'] = response.xpath('//*[@id="main"]/article/div[1]/div[1]/section/div/figure[1]/img/@src').get()
        decoded_item = ""
        for uitem in item['content']:
            decoded_item += uitem.encode('ascii', 'ignore').decode('utf-8')
        item['content'] = decoded_item

        yield item

    def parse(self, response):
        pass
