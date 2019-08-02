import logging
import re

logger = logging.getLogger(__name__)


class UrlParse:

	@staticmethod
	def protocol(url):

		try:
			protocol = 'https' if url.index('https://') == 0 else 'http'
		except ValueError:
			protocol = 'http'

		logger.info('Parsed url protocol: %s', protocol)
		return protocol

	@staticmethod
	def hostname(url):
		hostname = re.sub(r'https?://', '', url)
		hostname = re.sub(r'/.*', '', hostname)

		logger.info('Parsed url hostname: %s', hostname)
		return hostname

	@staticmethod
	def pathname(url):
		pathname = re.sub(r'https:?://', '', url)
		pathname = re.sub(r'^.*?/', '', pathname)
		pathname = re.sub(r'\?.*', '', pathname)

		if len(pathname) == 0 or not pathname[0] == '/':
			pathname = '/' + pathname

		logger.info('Parsed url pathname: %s', pathname)
		return pathname

	@staticmethod
	def query(url):

		try:
			index = url.index('?')
			query = url[index:len(url)]
		except ValueError:
			query = ''

		logger.info('Parsed url query: %s', query)
		return query

	@staticmethod
	def hash(url):

		try:
			index = url.index('#')
			hash_string = url[index:len(url)]
		except ValueError:
			hash_string = ''

		logger.info('Parsed url hash: %s', hash_string)
		return hash_string

	@staticmethod
	def to_object(query):
		obj = {}
		if len(query) > 0 and query[0] == '?':
			query = query[1:len(query)]
			tokens = query.split('&')

			for t in tokens:
				key_value_pair = t.split('=')
				obj[key_value_pair[0]] = key_value_pair[1]

		logger.info('Parsed query object: %s', obj)
		return obj

	@staticmethod
	def to_query(obj):
		query = '?'
		delimiter = ''
		for key in obj:
			query += (delimiter + key + '=' + str(obj[key]))
			delimiter = '&'

		return query
