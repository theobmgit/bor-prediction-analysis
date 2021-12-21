# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:46:40 2021

@author: Admin
"""

import scrapy


class IMDBCrawler(scrapy.Spider):
    name = "mpaaCrawler"
    start_urls =['https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/']
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    parseUrl='https://www.imdb.com'
    mpaaPath='/parentalguide'
    def parse(self,response):
        movieLinks=response.xpath('//table//tr[position()>1]/td[2]//@href').getall()
        for i in range(len(movieLinks)):
            linkPage="/".join(movieLinks[i].split("/")[0:-1])
            yield scrapy.Request(self.parseUrl+linkPage+self.mpaaPath,callback=self.parseMPAA)
        paginationLink=response.xpath('//a[text()="Next page"]/@href').get()
        yield response.follow(paginationLink,self.parse)
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
        yield data
        
        
        
    