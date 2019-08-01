
class Element:
	
	def __init__(self, tag_name, parent=None, index=0):
		self.tag_name = tag_name
		self.parent = parent
		self.attributes = {}
		self.children = []
		self.index = 0

	def setAttribute(self, name, value):
		self.attributes[name] = value

	def getAttribute(self, name):
		return self.attributes[name]

	def setParent(self, parent):
		self.parent = parent

	def getParent(self):
		return self.parent

	def addChild(self, element):
		element.setIndex(len(self.children))
		self.children.append(element)

	def getChild(self, index):
		return self.children[index]

	def setIndex(self, index):
		self.index = index

class Text:

	def __init__(self, data, parent=None, index=0):
		self.parent = parent
		self.index = index
		self.data = data

	def setIndex(self, index):
		self.index = index

	def getData():
		return self.data

	def setParent(self, parent):
		self.parent = parent

	def getParent(self):
		return self.parent

class DOM:

	def __init__(self):
		self.children = []

	def addChild(self, element):
		element.setIndex(len(self.children))
		self.children.append(element)

	def getChild(self, index):
		return self.children[index]
