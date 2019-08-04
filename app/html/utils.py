from .dom import Element
from .dom import Text

from abc import ABC
from html.parser import HTMLParser

import logging
import re

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

	def to_dom(self, html_text):
		super(Parser, self).feed(html_text)
		root_dom = Element(tag_name='html')
		for node in self.nodes:
			root_dom.add_child(node)

		return root_dom

	def handle_starttag(self, tag, attributes):
		element = Element(tag)

		if len(self.depth_tree) is not 0:
			element.set_parent(self.current_node)
			self.current_node.add_child(element)
		else:
			if self.root_node is None:
				self.root_node = element
			else:
				self.nodes.append(self.root_node)
				self.root_node = element

		for attr in attributes:
			element.set_attribute(attr[ATTR_NAME], attr[ATTR_VALUE])

		self.current_node = element
		self.depth_tree.append(tag)

	def handle_endtag(self, tag):
		if len(self.depth_tree) is not 0:
			if (self.depth_tree[len(self.depth_tree) - 1]) != tag:
				self.handle_endtag(self.depth_tree[len(self.depth_tree) - 1])

			self.current_node = self.current_node.get_parent()
			self.depth_tree.pop()

		else:
			logging.info('At End Tag %s There seems to be malformed html', tag)
			logger.info('SOMETHING HAS WENT HORRIBLY WRONG WITH THE PARSING')

	def handle_data(self, data):
		data = data.strip()
		if self.current_node is not None and len(data) is not 0:
			self.current_node.add_child(Text(data, self.current_node))


class Query:

	"""
	This class takes parses a query path string and returns the dom object
	that corresponds with the expression. If no dom object matches the
	query then NoneType is returned

	Expression Syntax:
		tag - alpha numeric string with no symbols
		class - alpha numeric string beginning with a '.' symbol
		id - alpha numeric string beginning with a '#' symbol
		attributes - name and value string of the attribute separated by an equal sign enclosed by brackets [name=value]
		children - navigate to the children elements by using the '>' symbol
		nth child - get the nth child of an element by specifying a numerical value within brackets [n]

		You can chain expressions together to create a dom query selector path
		Example table[2] - gets the child at index 2 of the first occurrence of a table tag
	"""

	@staticmethod
	def get_children(element, path):
		selected_element = Query.get_element(element, path)
		return selected_element.children if selected_element is not None else selected_element

	@staticmethod
	def get_element(element, query):

		query_path = query.split('>')
		selector = query_path.pop(0).strip()
		selected_element = element

		while len(selector) is not 0:
			# Break from loop if selected_element is of type TEXT
			if selected_element is None or selected_element.type == 'TEXT':
				selected_element = None
				break

			parsed = Query.parse_tag(selector)
			if parsed is not None:
				selected_element = Query.get_by_tag(selected_element, parsed)
				selector = selector.replace(parsed, '')
				continue

			parsed = Query.parse_id(selector)
			if parsed is not None:
				selected_element = Query.get_by_id(selected_element, parsed)
				selector = selector.replace(parsed, '')
				continue

			parsed = Query.parse_classname(selector)
			if parsed is not None:
				selected_element = Query.get_by_class(selected_element, parsed)
				selector = selector.replace(parsed, '')
				continue

			parsed = Query.parse_index(selector)
			if parsed is not None:
				selected_element = Query.get_by_index(selected_element, parsed)
				selector = selector.replace(parsed, '')
				continue

			if parsed is None:
				break

		if len(selector) is 0 and len(query_path) is not 0 and selected_element is not None:
			selected_element = Query.get_element(selected_element, '>'.join(query_path))

		return selected_element

	@staticmethod
	def get_by_tag(element, tag_name):
		selected_element = None
		for child in element.children:
			if child.type == 'HTML' and child.tag_name == tag_name:
				selected_element = child
				break

		return selected_element

	@staticmethod
	def get_by_class(element, class_name):
		selected_element = None
		for child in element.children:
			if child.type == 'HTML' and child.attributes['class'] == class_name:
				selected_element = child
				break

		return selected_element

	@staticmethod
	def get_by_id(element, id_value):
		selected_element = None
		for child in element.children:
			if child.type == 'HTML' and child.attributes['id'] == id_value:
				selected_element = child
				break

		return selected_element

	@staticmethod
	def get_by_index(element, index_value):
		index = int(re.sub(r'[\[\]]', '', index_value))
		return None if len(element.children) <= index else element.children[index]

	@staticmethod
	def parse_tag(query):
		match = re.match('[a-zA-Z]+', query)
		return match if match is None else match.group()

	@staticmethod
	def parse_classname(query):
		match = re.match('\\.\\w+', query)
		return match if match is None else match.group()

	@staticmethod
	def parse_id(query):
		match = re.match('#\\w+', query)
		return match if match is None else match.group()

	@staticmethod
	def parse_attributes(query):
		if re.match('\\[\\w=.*?\\]', query):
			logger.info('Matched an html attribute expression')

	@staticmethod
	def parse_index(query):
		match = re.match('\\[\\d+?\\]', query)
		return match if match is None else match.group()


if __name__ == '__main__':
	parser = Parser()
