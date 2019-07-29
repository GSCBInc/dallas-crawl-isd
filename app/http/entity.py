from app.http.utils import urlparse

import logging
import re

logger = logging.getLogger(__name__)

class Request:

	def __init__(self):
		self.method = None
		self.body = None
		self.url = None

	def get_method(self):
		return self.method

	def get_url(self):
		return self.url

class Response:

	def __init__(self):
		self.status = None

class Url:

	def __init__(self, urlstring=''):
		self.urlstring = urlstring
		self.hostname = None
		self.protocol = None
		self.pathname = None
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
			self.hash = urlparse.hash(self.urlstring)

	def to_string(self):
		return self.protocol + '://' + self.hostname + self.pathname + self.query + self.hash
