
class Element:
	
	def __init__(self, tag_name, parent=None, index=0):
		self.tag_name = tag_name
		self.parent = parent
		self.attributes = {}
		self.children = []
		self.index = index
		self.type = 'HTML'

	def set_attribute(self, name, value):
		self.attributes[name] = value

	def get_attribute(self, name):
		return self.attributes[name]

	def set_parent(self, parent):
		self.parent = parent

	def get_parent(self):
		return self.parent

	def add_child(self, child):
		child.set_index(len(self.children))
		self.children.append(child)

	def get_child(self, index):
		return self.children[index]

	def set_index(self, index):
		self.index = index


class Text:

	def __init__(self, data, parent=None, index=0):
		self.parent = parent
		self.index = index
		self.data = data
		self.type = 'TEXT'

	def set_index(self, index):
		self.index = index

	def get_data(self):
		return self.data

	def set_parent(self, parent):
		self.parent = parent

	def get_parent(self):
		return self.parent
