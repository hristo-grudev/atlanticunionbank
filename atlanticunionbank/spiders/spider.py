import scrapy

from scrapy.loader import ItemLoader

from ..items import AtlanticunionbankItem
from itemloaders.processors import TakeFirst


class AtlanticunionbankSpider(scrapy.Spider):
	name = 'atlanticunionbank'
	start_urls = ['https://www.atlanticunionbank.com/bank-better']

	def parse(self, response):
		post_links = response.xpath('//article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article[not(@class="blog-post")]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="blog-post__date"]/text()').get()

		item = ItemLoader(item=AtlanticunionbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
