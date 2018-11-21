# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import html
from BnToEng.items import BntoengItem


class WordSpider(scrapy.Spider):
    name = "word1"
    allowed_domains = ["english-bangla.com/"]
    start_urls = (
        'http://www.english-bangla.com/browse/bntoen/',
    )

    def parse(self, response):

        def wordFinder(word):
            req = requests.get(word)
            response = html.fromstring(req.content)
            item = BntoengItem()
            item['bangla_word'] = response.xpath(".//div[@id='w_info']/strong/span[@class='stl3']/text()")
            item['word_type'] = response.xpath(".//div[@id='w_info']/span[@class='format1']/span/text()")
            eng_word = response.xpath(".//div[@id='w_info']/span[@class='format1']/text()")
            item['translation'] = eng_word[5:-1]
            yield item
            next_page = response.xpath(".//div[@id='w_info']/span[@class='nextword']/a/@href")
            if next_page:
                wordFinder(next_page)

        alphabets = response.xpath(".//div[@id='wrapper']/div[@id='cat_page']/div[@class='a-z']/a/@href").extract()
        for alphabet in alphabets:
            data = requests.get(alphabet)
            response = html.fromstring(data.content)
            words = response.xpath(".//div[@id='wrapper']/div[@id='cat_page']/ul/li[1]/a/@href")
            for word in words:
                req = requests.get(word)
                response = html.fromstring(req.content)
                #response = response.xpath(".//div[@id='middle_area_f']/div[@class='search'][2]")
                item = BntoengItem()
                item['bangla_word'] = response.xpath(".//div[@id='w_info']/strong/span[@class='stl3']/text()")
                #item['bangla_word'] = response.xpath('.//*[@id="w_info"]/strong')
                #item['word_type'] = response.xpath('.//*[@id="w_info"]/span[1]/span[1]')
                item['word_type'] = response.xpath(".//div[@id='w_info']/span[@class='format1']/span[1]/text()")
                #eng_word = response.xpath('.//*[@id="w_info"]/span[1]/text()[2]')
                eng_word = response.xpath(".//div[@id='w_info']/span[@class='format1']")
                item['translation'] = eng_word[5:-1]
                yield item
                next_page = response.xpath(".//div[@id='w_info']/span[@class='nextword']/a/@href")
                if next_page:
                    wordFinder(next_page)