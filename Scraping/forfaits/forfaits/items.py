# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ForfaitsItem(scrapy.Item):
	title = scrapy.Field()
	price_eur = scrapy.Field()
	price_cen = scrapy.Field()
	exclusive = scrapy.Field()
	pass
