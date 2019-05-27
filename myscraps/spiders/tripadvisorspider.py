#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from myscraps.items import ReviewItem
from scrapy import Request
from scrapy.exceptions import CloseSpider


class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    start_urls = [
        "https://www.tripadvisor.com/Attraction_Review-g60763-d136143-Reviews-or10-New_York_Historical_Society_Museum_Library-New_York_City_New_York.html"
    ]
    num_pages = 0
    max_num_pages = 5

    def parse(self, response):
        # each review corresponds to a separate page.
        urls = []
        for href in response.xpath('//div[@class="quote"]/a/@href').getall():
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback=self.parse_review_page)

        next_page = response.xpath('//div[@class="unified ui_pagination "]/a/@href').getall()
        if next_page:
            self.num_pages += 1
            if self.num_pages > self.max_num_pages:
                raise CloseSpider('Search Exceeded %d' % self.max_num_pages)
            # FIXME: use follow instead
            url = response.urljoin(next_page[-1])
            print url
            yield scrapy.Request(url, self.parse)

    def parse_review_page(self, response):

        review_page = response.xpath('//div[@class="wrap"]/div/a/@href').extract()

        if review_page:
            for i in range(len(review_page)):
                url = response.urljoin(review_page[i])
                yield scrapy.Request(url, self.parse_review)

        next_page = response.xpath('//div[@class="unified ui_pagination "]/a/@href').getall()
        if next_page:
            url = response.urljoin(next_page[-1])
            yield scrapy.Request(url, self.parse_review_page)

    def parse_review(self, response):

        item = ReviewItem()

        contents = response.xpath('//div[@class="entry"]/p').extract()
        content = contents[0].encode("utf-8")

        ratings = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()
        rating = ratings[0][0]

        item['rating'] = rating
        item['review'] = content
        yield item
