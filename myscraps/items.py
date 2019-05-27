# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class ReviewItem(scrapy.Item):
    # Items to get
    title = scrapy.Field()
    author = scrapy.Field()
    review_text = scrapy.Field()
    ratings = scrapy.Field()
    rating_date = scrapy.Field()
    experience_date = scrapy.Field()
    location = scrapy.Field()
    # url = scrapy.Field()
