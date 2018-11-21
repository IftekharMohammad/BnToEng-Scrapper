# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import requests
from lxml import html
from BnToEng.items import BntoengItem


class WordSpider(CrawlSpider):
    name = "word"
    allowed_domains = ["english-bangla.com"]

    def start_requests(self):
        req = requests.get("http://www.english-bangla.com/browse/bntoen")
        get_page = html.fromstring(req.content)
        word_urls = get_page.xpath(".//div[@id='wrapper']/div[@id='cat_page']/div[@class='a-z']/a/@href")
        for word_url in word_urls:
            yield scrapy.Request(url=word_url, callback=self.get_word_url)

    def get_word_url(self, response):
        urls = response.xpath(".//div[@id='wrapper']/div[@id='cat_page']/ul/li[1]/a/@href").extract()
        next_page = response.xpath(".//div[@id='wrapper']/div[@class='pagination']/a[1]/@href").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.get_word_url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = BntoengItem()
        item['bangla_word'] = response.xpath(".//div[@id='w_info']/strong/span[@class='stl3']/text()").extract()
        # item['bangla_word'] = response.xpath('.//*[@id="w_info"]/strong')
        # item['word_type'] = response.xpath('.//*[@id="w_info"]/span[1]/span[1]')
        item['word_type'] = response.xpath(".//div[@id='w_info']/span[@class='format1']/span[1]/text()").extract()
        # eng_word = response.xpath('.//*[@id="w_info"]/span[1]/text()[2]')
        eng_word = response.xpath(".//div[@id='w_info']/span[@class='format1']").extract()
        item['translation'] = eng_word[5:-1]
        yield item
