import logging
import urllib

logger = logging.getLogger(__name__)
request = urllib.request

class crawlbot:

	def index(self, url):
		logger.info('Indexing url: %s', url.to_string())

		response = request.urlopen(url.to_string()).read()
		response_as_string = response.decode('utf-8')
		
