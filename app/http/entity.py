from app.http.constants import METHOD_NAMES
from app.http.utils import urlparse

import logging
import re

logger = logging.getLogger(__name__)

class Request:

	def __init__(self, method=Method.GET, url):
		self.method = method
		self.body = None
		self.url = url

	def getMethod(self):
		return self.method

	def getUrl(self):
		return self.url

class Response:

	def __init__(self):
		self.status = None

class Method:

	GET = METHOD_NAMES.GET
	PUT = METHOD_NAMES.PUT
	POST = METHOD_NAMES.POST
	DELETE = METHOD_NAMES.DELETE

class Url:

	def __init__(self, urlstring=''):
		self.urlstring = urlstring

		self.hostname = None
		self.protocol = None
		self.pathname = None
		self.queryObj = {}
		self.query = None
		self.hash = None

		if len(urlstring) > 0:
			self.parse()

	def is_secure(self):
		return self.protocol == 'https'

	def parsehost(self):
		self.hostname = None

	def parse(self):

		if len(self.urlstring) > 0:
			self.protocol = urlparse.protocol(self.urlstring)
			self.hostname = urlparse.hostname(self.urlstring)
			self.pathname = urlparse.pathname(self.urlstring)
			self.query = urlparse.query(self.urlstring)
			self.queryObj = urlparse.queryToObject(self.query)
			self.hash = urlparse.hash(self.urlstring)

	def setQueryParam(self, key, value):
		self.queryObj[key] = value

	def getQueryParam(self, key):
		return self.queryObj[key]

	def to_string(self):
		return self.protocol + '://' + self.hostname + self.pathname + urlparse.objectToQuery(self.queryObj) + self.hash

