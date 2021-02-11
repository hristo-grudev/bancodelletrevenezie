import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import BancodelletrevenezieItem
from itemloaders.processors import TakeFirst


class BancodelletrevenezieSpider(scrapy.Spider):
	name = 'bancodelletrevenezie'
	start_urls = ['https://www.bancodelletrevenezie.it/it/comunicazioni']

	def parse(self, response):
		post_links = response.xpath('//tr[@class="cat-list-row1"]|//tr[@class="cat-list-row0"]')
		for post in post_links:
			date = post.xpath('.//td[@headers="categorylist_header_date"]//text()').get()
			link = post.xpath('.//td[@headers="categorylist_header_title"]/a/@href').get()
			yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

		next_page = response.xpath('//li[@class="pagination-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response, date):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="item-page"]//text()[normalize-space() and not(ancestor::h1 | ancestor::a[@class="hasTooltip"] | ancestor::h2 | ancestor::script)]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BancodelletrevenezieItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
