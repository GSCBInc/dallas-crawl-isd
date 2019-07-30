from app.http.utils import client

import logging

logger = logging.getLogger(__name__)

class crawlbot:

	def __init__(self):
		self.id = None

	def set_id(self, id):
		self.id = id

	def get_id(self):
		return self.id

	def display_id(self):
		print(self.id)

	def index(self, url):
		logger.info('Indexing url: %s', url.to_string())