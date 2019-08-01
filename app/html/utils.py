import html
import logging

logger = logging.getLogger(__name__)

class HtmlParser(html.parser.HTMLParser):

        def __init__(self):
                self.domIndex = 0
                self.DOM = []

        def handle_starttag(self, tag, attrs):
		logger.info('Html start tag: %s', tag)
		logger.info('Html attributes: %s', attrs)

	def handle_endtag(self, tag):
		logger.info('Html end tag: %s', tag)

	def handle_data(self, data):
		logger.info('Data text: %s', data)

