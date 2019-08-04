from app.crawler.core import CrawlBot
from app.http.entities import Url

import logging

logger = logging.getLogger(__name__)


class Application:

	def __init__(self):
		self.crawler = CrawlBot()
		self.url = None

	def seed(self):
		seed_file = open('./data/seed.txt', 'r')

		self.url = Url(seed_file.read())
		logger.info('Loading seed url from file: %s', self.url.to_string())

		seed_file.close()

	def start(self):
		logger.info('Application has started')
		is_running = True
		index = 0

		self.seed()

		while is_running:
			page_index = int(self.url.get_query_param('PageIndex'))

			self.crawler.crawl(self.url)
			self.url.set_query_param('PageIndex', page_index + 1)

			is_running = index < 10
			index += 1


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	app = Application()
	app.start()
