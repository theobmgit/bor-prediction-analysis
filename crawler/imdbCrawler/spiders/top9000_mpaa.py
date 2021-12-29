# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:46:40 2021

@author: TrungCT
"""

import scrapy


class IMDBCrawler(scrapy.Spider):
    name = "full2MpaaCrawler"
    start_urls = [
        'https://www.imdb.com/search/title/?title_type=movie&sort=boxoffice_gross_us,desc&explore=title_type,genres']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    parseUrl = 'https://www.imdb.com'
    mpaaPath = '/parentalguide'

    listOfCertificate=['G','PG','PG-13','R','NC-17','GP','M','M/PG','X']
    def parse(self, response):
        movie_links = response.xpath('//div[@class="lister-item-content"]/h3/a/@href').getall()
        for link in movie_links:
            link_page = "/".join(link.split("/")[0:-1])
            yield scrapy.Request(self.parseUrl + link_page + self.mpaaPath, callback=self.parseMPAA)
        pagination_link = response.xpath('//*[@class="lister-page-next next-page"]/@href').get()
        if pagination_link is not None:
            if "9901" not in pagination_link:
                yield response.follow(pagination_link, callback=self.parse)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

    def parseMPAA(self, response):
        data = dict()
        data['Movie_Title'] = response.xpath('//*[@class="subpage_title_block__right-column"]//a[@href]/text()').get()
        data['Movie_ID'] = int(response.url.split('/')[-2].replace("tt", ''))
        # data['MPAA']=response.xpath('//*[@id="mpaa-rating"]//td[2]/text()').re('[A-Z]{1,2}[- ]{1,2}[0-9]*\s')
        list_of_certificate = response.xpath('//*[text()="Certification"]/..//li/a/text()').getall()
        data['ListOfCertificate'] = []
        for certificate in list_of_certificate:
            if "United States" in certificate:
                if "NotRated" not in certificate:
                    if "Not Rated" not in certificate:
                        if "Unrated" not in certificate:
                            if "Approved" not in certificate:
                                if "Passed" not in certificate:
                                    certificate=certificate.replace("United States:", "")
                                    if certificate in self.listOfCertificate:
                                        data['ListOfCertificate'].append(certificate)
            # indexDel=certificate.index(':')
            # certificate=certificate[indexDel+1:None]
            # if certificate in self.listOfCertificate:
            #     data['ListOfCertificate'].append(certificate)
        data['ListOfCertificate'] = list(set(data['ListOfCertificate']))
        yield data
