from app.http.apis import RestClient
from app.html.utils import Parser
from app.html.utils import Query

import logging

logger = logging.getLogger(__name__)

DATA_QUERY_PATHS = {
	'School Name:': '[1] > span > a > strong[0]',
	'Phone:': '[1] > span[0]',
	'Address:': '[1] > span[0]'
}


class CrawlBot:

	def __init__(self):
		self.dom_tree = None

	def index(self):
		schools = []
		if self.dom_tree is not None:
			school_table_list = Query.get_children(self.dom_tree, 'div')
			school = None
			for dom_element in school_table_list:
				table_data_rows = Query.get_children(dom_element, 'table > tbody > tr[1] > table > tbody')
				if table_data_rows is not None:
					for data_row in table_data_rows:
						data_column = Query.get_element(data_row, '[0] > span > strong[0]')
						if data_column is not None and DATA_QUERY_PATHS.__contains__(data_column.get_data()):
							data_column_value = Query.get_element(data_row, DATA_QUERY_PATHS[data_column.get_data()])
							logger.info('Extracted data column [%s]', data_column.get_data())
							logger.info('Extracted data column value [%s]', data_column_value.get_data())
							continue

						data_column = Query.get_element(data_row, '[0] > span[0]')
						if data_column is not None and DATA_QUERY_PATHS.__contains__(data_column.get_data()):
							data_column_value = Query.get_element(data_row, DATA_QUERY_PATHS[data_column.get_data()])
							logger.info('Extracted data column [%s]', data_column.get_data())
							logger.info('Extracted data column value [%s]', data_column_value.get_data())
							continue

	def crawl(self, url):
		parser = Parser()

		html_text = RestClient.get_html(url.to_string())

		logger.info('Transforming html text to dom nodes')
		self.dom_tree = parser.to_dom(html_text)
		logger.info('Finished dom transformation')

		self.index()
