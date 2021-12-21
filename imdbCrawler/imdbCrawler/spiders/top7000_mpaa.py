# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:46:40 2021

@author: Admin
"""

import scrapy


class IMDBCrawler(scrapy.Spider):
    name = "fullMpaaCrawler"
    start_urls =['https://www.imdb.com/search/title/?title_type=movie&genres=action&sort=num_votes,desc&explore=title_type,genres']
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    parseUrl='https://www.imdb.com'
    mpaaPath='/parentalguide'
    def parse(self,response):
        movieLinks=response.xpath('//div[@class="lister-item-content"]/h3/a/@href').getall()
        for link in movieLinks:
            linkPage="/".join(link.split("/")[0:-1])
            yield scrapy.Request(self.parseUrl+linkPage+self.mpaaPath,callback=self.parseMPAA)
        paginationLink=response.xpath('//*[@class="lister-page-next next-page"]/@href').get()
        if paginationLink!=None:
            if "7001" not in paginationLink:
                yield response.follow(paginationLink,callback=self.parse)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        
    def parseMPAA(self,response):
        data=dict()
        data['Movie_Title']=response.xpath('//*[@class="subpage_title_block__right-column"]//a[@href]/text()').get()
        #data['MPAA']=response.xpath('//*[@id="mpaa-rating"]//td[2]/text()').re('[A-Z]{1,2}[- ]{1,2}[0-9]*\s')
        listOfCertificate=response.xpath('//*[text()="Certification"]/..//li/a/text()').getall()
        data['ListOfCertificate']=[]
        for certificate in listOfCertificate:
            if "United States" in certificate:
                if "NotRated" not in certificate:
                    if "Not Rated" not in certificate:
                        if "Unrated" not in certificate:
                            data['ListOfCertificate'].append(certificate.replace("United States:",""))
        data['ListOfCertificate']=list(set(data['ListOfCertificate']))
        yield data
        
        
        
    