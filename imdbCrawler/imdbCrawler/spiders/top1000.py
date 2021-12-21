# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:46:40 2021

@author: Admin
"""
import json
import scrapy


class IMDBCrawler(scrapy.Spider):
    name = "imdbCrawler"
    start_urls = ['https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/96.0.4664.45 Safari/537.36 '

    parseUrl = 'https://www.imdb.com'

    def parse(self, response):
        movieLinks = response.xpath('//table//tr[position()>1]/td[2]//@href').getall()
        for i in range(len(movieLinks)):
            yield scrapy.Request(self.parseUrl + movieLinks[i], callback=self.parseAMovie)
        paginationLink = response.xpath('//a[text()="Next page"]/@href').get()
        yield response.follow(paginationLink, self.parse)

    def parseAMovie(self, response):
        data = dict()
        y = json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
        # data['Movie_Title']=response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').get()
        data['Movie_Title'] = y['name']
        data['Budget'] = response.xpath(
            '//span[text()="Budget"]/..//span[@class="ipc-metadata-list-item__list-content-item"]/text()').re(
            '[$][0-9,]*')
        data['Cast'] = list(
            set(response.xpath('//*[text()="Stars"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()))
        director = list(set(response.xpath(
            '//*[text()="Director" or text()="Directors" ]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()))
        writer = list(set(response.xpath(
            '//*[text()="Writer" or text()="Writers"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()))
        data['Crew'] = list(set(director + writer))
        data['Studios'] = response.xpath(
            '//*[text()="Production company" or text()="Production companies"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()
        data['Genre'] = response.xpath('//*[text()="Genres"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()
        data['Keywords'] = response.xpath('//a[@class="ipc-chip ipc-chip--on-base"]//text()').getall()
        data['Languages'] = response.xpath(
            '//*[text()="Languages" or text()="Language"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()
        # Certificate After
        data['Countries'] = response.xpath(
            '//*[text()="Country of origin" or text()="Countries of origin"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()
        # Missing Production Method
        data['Filming_Location'] = response.xpath(
            '//*[text()="Filming locations" or text()="Filming location"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()
        # data['Release_Date']=response.xpath('//*[text()="Release date"]/..//li[@class="ipc-inline-list__item"]/a/text()').getall()
        data['Release_Data'] = y['datePublished']
        data['Runtime'] = str().join(response.xpath('//*[text()="Runtime"]/../div/text()').getall())
        data['Gross_worldwide'] = response.xpath('//*[text()="Gross worldwide"]/../div//text()').get()
        data['Rating'] = response.xpath('//*[@data-testid="hero-rating-bar__aggregate-rating__score"]//text()').get()
        data['Rating_Count'] = response.xpath(
            '//*[@data-testid="hero-rating-bar__aggregate-rating__score"]/../div[3]/text()').get()
        yield data
