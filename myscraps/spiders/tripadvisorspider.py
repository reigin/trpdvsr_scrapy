#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from myscraps.items import ReviewItem
from scrapy import Request
from bs4 import BeautifulSoup

class TripAdvisorReview(scrapy.Spider):
    globvar_title = ''
    name = "tripadvisor"
    # Cities: surabaya,bandung,jakarta,lombok,yogyakarta,flores,bali.
    start_urls = [
#                    "https://www.tripadvisor.com/Attractions-g294226-Activities-Bali.html",\
#                	 "https://www.tripadvisor.com/Attractions-g297704-Activities-Bandung_West_Java_Java.html",\
#                    "https://www.tripadvisor.com/Attractions-g294229-Activities-Jakarta_Java.html",\
#                    "https://www.tripadvisor.com/Attractions-g297733-Activities-Lombok_West_Nusa_Tenggara.html",\
#                    "https://www.tripadvisor.com/Attractions-g294230-Activities-Yogyakarta_Java.html",\
#                    "https://www.tripadvisor.com/Attractions-g297729-Activities-Flores_East_Nusa_Tenggara.html",\
#    				"https://www.tripadvisor.com/Attractions-g297715-Activities-Surabaya_East_Java_Java.html"

                	 "https://www.tripadvisor.com/Attractions-g297704-Activities-Bandung_West_Java_Java.html"

                    ]

    def parse(self, response):
        global globvar_title
        urls = []

        for href in response.xpath('//div[@class="listing_title"]/a/@href').extract():
			
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)

                titling = href.replace("/",'')
                globvar_title = titling.split('-')[-2];
                yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            titling = href.replace("/",'')
            globvar_title = titling.split('-')[-2];
            yield scrapy.Request(url, self.parse)

    def parse_page(self, response):
        review_page = response.xpath('//div[@class="wrap"]/div/a/@href').extract()
        if review_page:
            for i in range(len(review_page)):
                url = response.urljoin(review_page[i])
                yield scrapy.Request(url, self.parse_review)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            yield scrapy.Request(url, self.parse_page)

    def parse_review(self, response):

        item = ReviewItem()

        contents = response.xpath('//div[@class="entry"]/p').extract()
        content = contents[0].encode("utf-8")
        soup = BeautifulSoup(content, 'html.parser')
        
        print globvar_title
		
        item['ids'] = soup.p['id']
        item['titlen'] = globvar_title
        item['review'] = soup.get_text()
        yield item

