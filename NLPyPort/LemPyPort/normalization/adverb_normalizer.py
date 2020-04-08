import xmltodict
import re

class adverb_normalizer:
	def __init__(self):

		self.declesion_exceptions=[]
		self.declesion_targets = []
		self.declesion_tags = []
		self.declesion_replacement = []
		self.declesion_prefix = []
		self.declesion_re = []

	def compile_rules(self):
		lista = [None] * len(self.declesion_targets)
		for index,elem in enumerate(self.declesion_targets):
			li = re.compile(self.declesion_prefix+elem)
			lista[index] = li
		self.declesion_re=lista


	def adverb_normalizer_load(self, file_name):
		with open(file_name) as file:
			doc = xmltodict.parse( file.read())
			result = (doc["adverbdeclensions"]["replacement"])

			genderdeclensions_number_of_rules = len(result)
			self.declesion_exceptions = [None]*genderdeclensions_number_of_rules
			self.declesion_targets = [None]*genderdeclensions_number_of_rules
			self.declesion_tags = [None]*genderdeclensions_number_of_rules
			self.declesion_replacement = [None]*genderdeclensions_number_of_rules

			for index, elem in enumerate(result):
				if '@target' in elem.keys():
					self.declesion_targets[index] = elem["@target"]
				else:
					self.declesion_targets[index] = ""
				if '@exceptions' in elem.keys():
					self.declesion_exceptions[index] = elem["@exceptions"]
				else:
					self.declesion_exceptions[index] = ""
				if '@tag' in elem.keys():
					self.declesion_tags[index] = elem["@tag"]
				else:
					self.declesion_tags[index] = ""
				if '#text' in elem.keys():
					self.declesion_replacement[index] = elem["#text"]
				else:
					self.declesion_replacement[index] = ""
			self.declesion_prefix = (doc["adverbdeclensions"]["prefix"])					

	def print_adverb_normalizer(self):
		for i in range(len(self.declesion_targets)):
			print(i)
			print("---------\n")
			print("Target: " + self.declesion_targets[i])
			print("Tags: " + self.declesion_tags[i])
			print("Exceptions: " + self.declesion_exceptions[i])
			print("Replacement: " + self.declesion_replacement[i])

	def normalize_adverb(self,token, tag):
		bigget_rule_size = 0
		lemmatized_word = ""
		normalization = token.lower()
		for index,elem in enumerate(self.declesion_targets):
			if(self.declesion_re[index].match(normalization)
					and tag.lower() in self.declesion_tags[index].split("|")
						and not (normalization in self.declesion_exceptions[index].split("|"))):
					tamanho = len(self.declesion_targets[index])
					if(tamanho > bigget_rule_size):
						lemmatized_word = normalization[:(len(normalization) - len(self.declesion_targets[index]))] + self.declesion_replacement[index]
						bigget_rule_size = tamanho
						return(lemmatized_word)
		return(lemmatized_word)

