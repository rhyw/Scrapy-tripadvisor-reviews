#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import collections
import scrapy
from myscraps.items import ReviewItem
from scrapy import Request
from scrapy.exceptions import CloseSpider


class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    start_urls = [
        #"https://www.tripadvisor.com/Attraction_Review-g60763-d136143-Reviews-or10-New_York_Historical_Society_Museum_Library-New_York_City_New_York.html"
        "https://www.tripadvisor.cn/Attraction_Review-g187497-d190166-Reviews-Basilica_of_the_Sagrada_Familia-Barcelona_Catalonia.html"
    ]
    num_pages = 0
    max_num_pages = 200000
    rating_pattern = re.compile(r'.*(\d{1})\d{1}')

    def parse(self, response):
        # each review corresponds to a separate page.
        urls = []
        for href in response.xpath('//div[@class="quote"]/a/@href').getall():
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback=self.parse_review)

        next_page = response.xpath('//div[@class="unified ui_pagination "]/a/@href').getall()
        if next_page:
            self.num_pages += 1
            if self.num_pages > self.max_num_pages:
                raise CloseSpider('Search Exceeded %d' % self.max_num_pages)
            # FIXME: use follow instead
            url = response.urljoin(next_page[-1])
            print url
            yield scrapy.Request(url, self.parse)

    def parse_review(self, response):

        item = ReviewItem()

        content = response.css('div.meta_inner')
        title = content.xpath('.//h1[@class="title"]/text()').get()
        author = content.css('div.info_text').css('div::text').get()
        review_text = content.css('span.fullText::text').get()
        rating_date = content.css('span.ratingDate::text').get()
        experience_date = content.css('div.prw_reviews_stay_date_hsx::text').get()
        ratings = content.css('span.ui_bubble_rating')[0].attrib['class']
        location = content.xpath('.//strong/text()').get()
        # ratings = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()
        item = collections.OrderedDict()
        item['title'] = title
        item['author'] = author
        item['review_text'] = review_text
        item['ratings'] = re.search(self.rating_pattern, ratings).group(1)
        item['experience_date'] = experience_date
        item['rating_date'] = rating_date
        item['location'] = location
        item['url'] = response.url

        yield item
