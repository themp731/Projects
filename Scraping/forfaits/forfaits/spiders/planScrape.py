import scrapy
from forfaits.items import ForfaitsItem

class BouySpider(scrapy.Spider):
	name = "planScrape"
	allowed_domains = ["bouyguestelecom.fr"]
	start_urls = [
		"https://www.bouyguestelecom.fr/forfaits-mobiles/forfaits-sans-engagement",
		"https://www.bouyguestelecom.fr/forfaits-mobiles/forfaits-avec-telephone",
		"https://www.bouyguestelecom.fr/carte-prepayee"
	]

	def parse(self, response):
		for sel in response.xpath('//div[@class="plan-type col-xs-12"]'):
			item = ForfaitsItem()
			item['title'] = sel.xpath('//h3[@class="offer"]/text()').extract()
			item['price_eur'] = sel.xpath('//div[@class="prices"]/div[@class="price xlg"]/div[2]/span/text()').extract()
			item['price_cen'] = sel.xpath('//div[@class="prices"]/div[@class="price xlg"]/div[2]/sup/text()').extract()
			a = sel.xpath('//span[@id="exclu"]/text()').extract() 
			if len(a) != 0:
				item["exclusive"] = "Yes"
			else:
				item["exclusive"] = "No" 
			yield item