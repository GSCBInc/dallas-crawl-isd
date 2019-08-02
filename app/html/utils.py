from .dom import Element
from .dom import Text

from abc import ABC
from html.parser import HTMLParser

import logging

logger = logging.getLogger(__name__)

ATTR_NAME = 0
ATTR_VALUE = 1


class Parser(HTMLParser, ABC):

	def __init__(self):
		super(Parser, self).__init__()
		self.depth_index = 0
		self.depth_tree = []

		self.current_node = None
		self.root_node = None
		self.nodes = []

		self.ignore_after_tag = {
			'id': 'ui-paging-container'
		}

		self.ignore_all = False

	def to_dom(self, html_text):
		super(Parser, self).feed(html_text)
		return self.nodes

	def ignore_rest(self, attrs):
		ignore = False
		for attr in attrs:
			ignore = ignore or (self.ignore_after_tag.get(attr[ATTR_NAME]) == attr[ATTR_VALUE])

		return ignore

	def handle_starttag(self, tag, attributes):
		# self.ignore_all = self.ignore_all or self.ignore_rest(attributes)
		element = Element(tag)
		if self.ignore_all:
			return
		elif len(self.depth_tree) is not 0:
			self.current_node.add_child(element)
		else:
			if self.current_node is not None:
				logger.info('Creating new node object')
				self.nodes.append(self.root_node)
				self.root_node = element
			else:
				self.root_node = element

		for attr in attributes:
			element.set_attribute(attr[ATTR_NAME], attr[ATTR_VALUE])

		logger.info('Html start tag: %s', tag)
		logger.info('Html attributes: %s', attributes)

		self.current_node = element
		self.depth_tree.append(tag)

	def handle_endtag(self, tag):
		if self.ignore_all:
			return
		elif len(self.depth_tree) is not 0:
			if self.depth_tree[len(self.depth_tree) - 1] == tag:
				logger.info('Html end tag: %s', tag)
				self.depth_tree.pop()
				logger.info('Start tags left to resolve: (%s)', len(self.depth_tree))
				if len(self.depth_tree) == 1:
					logger.info('Last tag left to resolve: (%s)', tag)

			else:
				logger.info('End tag mismatch [ expected %s and got %s ]', self.depth_tree[len(self.depth_tree) - 1], tag)
				logger.info('Going further up the depth tree')
				self.handle_endtag(self.depth_tree[len(self.depth_tree) - 1])
		else:
			logging.info('At End Tag %s There seems to be malformed html', tag)
			logger.info('SOMETHING HAS WENT HORRIBLY WRONG WITH THE PARSING')

	def handle_data(self, data):
		if self.current_node is not None and not self.ignore_all:
			self.current_node.add_child(Text(data, self.current_node))
			# logger.info('Data text: %s', data)


if __name__ == '__main__':
	parser = Parser()
