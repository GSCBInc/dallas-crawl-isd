from app.http.apis import RestClient
from app.html.utils import Parser

import logging

logger = logging.getLogger(__name__)


class CrawlBot:

	def __init__(self):
		self.index_status = None

	def index(self, url):
		self.index_status = None
		parser = Parser()

		html_text = RestClient.get_html(url.to_string())

		logger.info('Transforming html text to dom nodes')
		dom = parser.to_dom(html_text)
		logger.info('Finished dom transformation')
