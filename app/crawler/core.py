from app.http.utils import client

class crawlbot:

	def __init__(self):
		self.id = None

	def set_id(self, id):
		self.id = id

	def get_id(self):
		return self.id

	def display_id(self):
		print(self.id)

	def crawl(self, url):
		print()