class Text:
	def __init__(self):
		self.tokens = []
		self.pos_tags = []
		self.lemas = []
		self.entities = []
		self.np_tags = []

	def set_tokens(self,tokens):
		self.tokens = tokens


	def set_pos_tags(self,pos_tags):
		self.pos_tags = pos_tags
		for index,elem in enumerate(self.tokens):
			if(elem=="\n"):
				self.pos_tags[index] = ""
			if(elem=="EOS"):
				self.pos_tags[index] = "EOS"

	def set_lemas(self,lemas):
		self.lemas = lemas
		for index,elem in enumerate(self.tokens):
			if(elem=="\n"):
				self.lemas[index] = ""
			if(elem=="EOS"):
				self.lemas[index] = "EOS"

	def set_entities(self,entities):
		self.entities = entities
		for index,elem in enumerate(self.tokens):
			if(elem=="\n"):
				self.entities[index] = ""
			if(elem=="EOS"):
				self.entities[index] = "EOS"

	def set_np_tags(self,np_tags):
		self.np_tags = np_tags
		for index,elem in enumerate(self.tokens):
			if(elem=="\n"):
				self.np_tags[index] = ""
			if(elem=="EOS"):
				self.np_tags[index] = "EOS"

	def print_text_order(self,lista):
		for elem in lista:
			print(elem)

	def print_conll(self):
		current_line = ""
		for index in range(len(self.tokens)):
			if(self.tokens!=[]):
				current_line += self.tokens[index]
			if(self.pos_tags!=[]):
				current_line += " " + self.pos_tags[index]
			if(self.lemas!=[]):
				current_line += " " + self.lemas[index]
			if(self.entities!=[]):
				current_line += " " + self.entities[index]
			if(self.np_tags!=[]):
				current_line += " " + self.np_tags[index]
			print(current_line)
			current_line=""