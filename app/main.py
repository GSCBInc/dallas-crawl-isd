from app.crawler.core import crawlbot
from app.http.entity import Url

import logging

logger = logging.getLogger(__name__)

class application:

	def __init__(self):
		self.crawlbot = crawlbot()
		self.url = None

	def seed(self):
		seed_file = open('.\\data\\seed.txt', 'r')
		seed_url = seed_file.read()

		logger.info('Loading seed url from file: %s', seed_url)
		self.url = Url(seed_url)

		seed_file.__exit__()

	def start(self):
		logger.info('Application has started')
		self.seed()

		logger.info(self.url.is_secure())

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	app = application()
	app.start()
