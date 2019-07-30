from app.crawler.core import crawlbot
from app.http.entity import Url

import logging

logger = logging.getLogger(__name__)

class application:

	def __init__(self):
		self.crawlbot = crawlbot()
		self.url = None

	def seed(self):
		seed_file = open('./data/seed.txt', 'r')

		self.url = Url(seed_file.read())
		logger.info('Loading seed url from file: %s', self.url.to_string())

		seed_file.__exit__()

	def start(self):
		logger.info('Application has started')
		is_running = True
		page_index = 1
		index = 0

		self.seed()

		while is_running:
			page_index = int(self.url.getQueryParam('PageIndex'))

			self.crawlbot.index(self.url)
			self.url.setQueryParam('PageIndex', page_index + 1)

			is_running = index < 10
			index += 1

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	app = application()
	app.start()
