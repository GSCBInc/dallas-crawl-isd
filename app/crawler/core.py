from app.csv.utils import CsvWriter
from app.http.apis import RestClient
from app.html.utils import Parser
from app.html.utils import Query

import logging

logger = logging.getLogger(__name__)


class CrawlBot:

	def __init__(self):
		self.data_query_paths = {
			'School Name:': '[1] > span > a > strong[0]',
			'Phone:': '[1] > span[0]',
			'Address:': ['[1] > span[0]', '[1] > span[2]']
		}
		self.data_keys = {
			'School Name:': 'Name',
			'Address:': 'Address',
			'Phone:': 'Phone'
		}
		self.dom_tree = None

	def extract_value(self, data_row, data_column):
		data_column_value = ''
		query_path = self.data_query_paths[data_column.get_data()]
		if type(query_path) == list:
			for query_item in query_path:
				data_column_value += Query.get_element(data_row, query_item).get_data()
		elif type(query_path) == str:
			data_column_value = Query.get_element(data_row, query_path).get_data()

		return data_column_value

	def index(self):
		schools = []
		if self.dom_tree is not None:
			school_table_list = Query.get_children(self.dom_tree, 'div')
			for dom_element in school_table_list:
				table_data_rows = Query.get_children(dom_element, 'table > tbody > tr[1] > table > tbody')
				if table_data_rows is not None:
					school = {}
					for data_row in table_data_rows:
						data_column = Query.get_element(data_row, '[0] > span > strong[0]')
						if data_column is not None and self.data_query_paths.__contains__(data_column.get_data()):
							data_column_value = self.extract_value(data_row, data_column)
							school_key = self.data_keys[data_column.get_data()]
							school[school_key] = data_column_value
							continue

						data_column = Query.get_element(data_row, '[0] > span[0]')
						if data_column is not None and self.data_query_paths.__contains__(data_column.get_data()):
							data_column_value = self.extract_value(data_row, data_column)
							school_key = self.data_keys[data_column.get_data()]
							school[school_key] = data_column_value
							continue

					logger.info('Constructed school object: %s', school)
					schools.append(school)

			CsvWriter.from_list(data=schools)

	def crawl(self, url):
		parser = Parser()

		html_text = RestClient.get_html(url.to_string())

		logger.info('Transforming html text to dom nodes')
		self.dom_tree = parser.to_dom(html_text)
		logger.info('Finished dom transformation')

		self.index()
