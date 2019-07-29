import logging
import re

logger = logging.getLogger(__name__)

class client:

	def __init__(self):
		self.request = None

	def send(self, request):
		self.response = None

class urlparse:

	@staticmethod
	def protocol(url):
		protocol = None
		try:
			protocol = 'https' if url.index('https://') == 0 else 'http'
		except ValueError:
			protocol = 'http'

		logger.info('Parsed url protocol: %s', protocol)
		return protocol

	@staticmethod
	def hostname(url):
		hostname = re.sub(r'https?:\/\/', '', url)
		hostname = re.sub(r'\/.*', '', hostname)

		logger.info('Parsed url hostname: %s', hostname)
		return hostname

	@staticmethod
	def pathname(url):
		pathname = re.sub(r'https:?:\/\/', '', url)
		pathname = re.sub(r'^.*?/', '', pathname)
		pathname = re.sub(r'\?.*', '', pathname)

		if len(pathname) == 0 or not pathname[0] == '/':
			pathname = '/' + pathname

		logger.info('Parsed url pathname: %s', pathname)
		return pathname

	@staticmethod
	def query(url):
		query = None
		try:
			index = url.index('?')
			query = url[index:len(url)]
		except ValueError:
			query = ''

		logger.info('Parsed url query: %s', query)
		return query

	@staticmethod
	def hash(url):
		hashstring = None
		try:
			index = url.index('#')
			hashstring = url[index:len(url)]
		except ValueError:
			hashstring = ''

		logger.info('Parsed url hash: %s', hashstring)
		return hashstring

	@staticmethod
	def queryToObject(query):
		obj = {}
		if len(query) > 0 and query[0] == '?':
			query = query[1:len(query)]
			tokens = query.split('&')

			for t in tokens:
				keyvaluepair = t.split('=')
				obj[keyvaluepair[0]] = keyvaluepair[1]

		logger.info('Parsed query object: %s', obj)
		return obj
