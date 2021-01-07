# -*- coding: utf-8 -*-
import os
import sys

from scrapy import Spider
from scrapy.item import Item, Field
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

from . import make_requests



"""
https://www.scrapingbee.com/blog/practical-xpath-for-web-scraping/
https://scrapingclub.com/blog/scrapy-tutorial-9-how-use-scrapy-item/
https://docs.scrapy.org/en/latest/topics/practices.html
"""

URLS = []

# 
def create_url(config, currency):
    url = 'https://www.olx.ua/transport/legkovye-avtomobili/'
    url = make_requests.create_url(url, config['brand'], config['model'])
    url = make_requests.append_price_filter(url, config['min_price'], config['max_price'])
    url = make_requests.append_motor_year(url, config['min_motor_year'], config['max_motor_year'])
    url = make_requests.append_motor_mileage(url, config['min_motor_mileage'], config['max_motor_mileage'])
    url = make_requests.append_motor_engine_size(url, config['min_engine_size'], config['max_engine_size'])
    url = make_requests.append_car_body(url, config['body_type'])
    url = make_requests.append_fuel_type(url, config['fuel_type'])
    url = make_requests.append_car_color(url, config['color'])
    url = make_requests.append_transmission_type(url, config['transmission_type'])
    url = make_requests.append_condition(url, config['condition_type'])
    url = make_requests.append_cleared_customs(url, config['custom_type'])
    url = make_requests.append_currency_type(url, currency)
    return url

# 
def test_ctreating_url(config):
    url = create_url(config)
    print(url)

# 
class CustomItem(Item):
    title = Field()
    href = Field()
    image = Field()
    price = Field()
    brand = Field()
    model = Field()
    issue_year = Field()
    city = Field()
    date = Field()
    parse_date = Field()


# 
class OlxSpider(Spider):
    name = 'olxspider'
    allowed_domains = ['olx.ua']
    start_urls = URLS
    
    # 
    def parse(self, response):
        for post in response.xpath('//div[@class="offer-wrapper"]'):
            item = CustomItem()
            item['title'] = post.xpath('.//strong/text()').get()
            item['image'] = post.xpath('.//img[@class="fleft"]/@src').get()
            item['href'] = post.xpath('.//a/@href').get()
            item['price'] = post.xpath('.//p[@class="price"]//strong/text()').get()
            item['city'] = post.xpath('.//p[@class="lheight16"]/small[1]/span/text()').get()
            item['date'] = post.xpath('.//p[@class="lheight16"]/small[2]/span/text()').get()
            yield item

        for next_page in response.xpath('.//div[@class="pager rel clr"]/span/a/@href').getall():
            yield response.follow(next_page, self.parse)


# 
def parse_data(config, currency):
    target_url = create_url(config, currency)
    URLS.append(target_url)
    settings = get_project_settings()

    settings.update({
        'FEEDS': {config['tmp_file']: {
            'format': 'json', 
            'indent': 4, 
            'encoding': 'utf-8',
            'overwrite': True,}
        }
    })

    runner = CrawlerRunner(settings)
    d = runner.crawl(OlxSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()