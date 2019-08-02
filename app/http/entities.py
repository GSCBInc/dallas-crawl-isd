from app.http.utils import UrlParse

from urllib import request

import logging

logger = logging.getLogger(__name__)


class Request(request.Request):

	def send(self):
		return request.urlopen(self)


class Response:

	def __init__(self):
		self.status = None

	def get_status(self):
		return self.status


class Url:

	def __init__(self, url_string=''):
		self.url_string = url_string

		self.hostname = None
		self.protocol = None
		self.pathname = None
		self.query_object = {}
		self.query = None
		self.hash = None

		if len(self.url_string) > 0:
			self.parse()

	def is_secure(self):
		return self.protocol == 'https'

	def parse_host(self):
		self.hostname = None

	def parse(self):

		if len(self.url_string) > 0:
			self.protocol = UrlParse.protocol(self.url_string)
			self.hostname = UrlParse.hostname(self.url_string)
			self.pathname = UrlParse.pathname(self.url_string)
			self.query = UrlParse.query(self.url_string)
			self.query_object = UrlParse.to_object(self.query)
			self.hash = UrlParse.hash(self.url_string)

	def set_query_param(self, key, value):
		self.query_object[key] = value

	def get_query_param(self, key):
		return self.query_object[key]

	def to_string(self):
		return self.protocol + '://' + self.hostname + self.pathname + UrlParse.to_query(self.query_object) + self.hash

