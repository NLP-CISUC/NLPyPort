import xmltodict
import re

class verb_normalizer:
	def __init__(self):

		self.declesion_exceptions=[]
		self.declesion_targets = []
		self.declesion_tags = []
		self.declesion_replacement = []
		self.declesion_suffix = ""
		self.declesion_prefix = ""
		self.declesion_re = []


		self.lexeme_exceptions=[]
		self.lexeme_targets = []
		self.lexeme_tags = []
		self.lexeme_replacement = []
		self.lexeme_rule_list=[]
		self.lexeme_suffix = ""
		self.lexeme_prefix = ""
		self.lexeme_re = []
		self.lexeme_re_normal = []


		self.conjugation_exceptions=[]
		self.conjugation_targets = []
		self.conjugation_tags = []
		self.conjugation_replacement = []
		self.conjugation_suffix = ""
		self.conjugation_prefix = ""
		self.conjugation_re = []
		self.conjugation_re_normal = []

	def compile_rules(self):
		self.compile_rules_declesions()
		self.compile_rules_lexemes()
		self.compile_rules_conjugation()

	def compile_rules_declesions(self):
		lista = [None] * len(self.declesion_targets)
		for index,elem in enumerate(self.declesion_targets):
			li = re.compile(self.declesion_prefix+elem+self.declesion_suffix)
			lista[index] = li
		self.declesion_re=lista

	def compile_rules_lexemes(self):
		lista = [None] * len(self.lexeme_targets)
		lista_normal = [None] * len(self.lexeme_targets)
		for index,elem in enumerate(self.lexeme_targets):
			li_normal = re.compile(elem+self.lexeme_suffix)
			li = re.compile(self.lexeme_prefix+elem+self.lexeme_suffix)
			lista[index] = li
			lista_normal[index] = li_normal
		self.lexeme_re=lista
		self.lexeme_re_normal = lista_normal

	def compile_rules_conjugation(self):
		lista = [None] * len(self.conjugation_targets)
		lista_normal = [None] * len(self.conjugation_targets)
		for index,elem in enumerate(self.conjugation_targets):
			li_normal = re.compile(elem+self.conjugation_suffix)
			li = re.compile(self.conjugation_prefix+elem)
			lista[index] = li
			lista_normal[index] = li_normal
		self.conjugation_re=lista
		self.conjugation_re_normal = lista_normal


	def verb_normalizer_load(self,file_name_conjugation,file_name_lexemes,file_name_declensions):
		#-----------------
		#Load regular declensions
		#-----------------
		with open(file_name_conjugation) as file:
			doc = xmltodict.parse( file.read())
			result = (doc["irregularverbconjugations"]["replacement"])
			
			'''
			Get the number of rules and set the size of the class variables
			'''
			verbconjugation_number_of_rules = len(result)
			self.conjugation_exceptions=[None]*verbconjugation_number_of_rules
			self.conjugation_targets = [None]*verbconjugation_number_of_rules
			self.conjugation_tags = [None]*verbconjugation_number_of_rules
			self.conjugation_replacement = [None]*verbconjugation_number_of_rules
			'''
			Check if the rule has any of the elements 
			'''
			for index,elem in enumerate(result):
				if '@target' in elem.keys():
					self.conjugation_targets[index] = elem["@target"]
				else:
					self.conjugation_targets[index] = ""
				if '@exceptions' in elem.keys():
					self.conjugation_exceptions[index] = elem["@exceptions"]
				else:
					self.conjugation_exceptions[index] = ""
				if '@tag' in elem.keys():
					self.conjugation_tags[index] = elem["@tag"]
				else:
					self.conjugation_tags[index] = ""
				if '#text' in elem.keys():
					self.conjugation_replacement[index] = elem["#text"]
				else:
					self.conjugation_replacement[index] = ""
			
			self.conjugation_suffix = (doc["irregularverbconjugations"]["suffix"])
			self.conjugation_prefix = (doc["irregularverbconjugations"]["prefix"])

		#-----------------
		#Load lexeme declensions
		#-----------------
		with open(file_name_lexemes) as file:
			doc = xmltodict.parse( file.read())
			result = (doc["regularverblexemes"]["replacement"])
			'''
			Get the number of rules and set the size of the class variables
			'''
			lexemedeclensions_number_of_rules = len(result)
			self.lexeme_exceptions=[None]*lexemedeclensions_number_of_rules
			self.lexeme_targets = [None]*lexemedeclensions_number_of_rules
			self.lexeme_tags = [None]*lexemedeclensions_number_of_rules
			self.lexeme_replacement = [None]*lexemedeclensions_number_of_rules
			'''
			Check if the rule has any of the elements 
			'''
			for index,elem in enumerate(result):
				if '@target' in elem.keys():
					self.lexeme_targets[index] = elem["@target"]
				else:
					self.lexeme_targets[index] = ""
				if '@exceptions' in elem.keys():
					self.lexeme_exceptions[index] = elem["@exceptions"]
				else:
					self.lexeme_exceptions[index] = ""
				if '@tag' in elem.keys():
					self.lexeme_tags[index] = elem["@tag"]
				else:
					self.lexeme_tags[index] = ""
				if '#text' in elem.keys():
					self.lexeme_replacement[index] = elem["#text"]
				else:
					self.lexeme_replacement[index] = ""
			self.lexeme_suffix = (doc["regularverblexemes"]["suffix"])
			self.lexeme_prefix = (doc["regularverblexemes"]["prefix"])

		#-----------------
		#Load conjugation declensions
		#-----------------
		with open(file_name_declensions) as file:
			doc = xmltodict.parse( file.read())
			result = (doc["regularverbdeclensions"]["replacement"])
			'''
			Get the number of rules and set the size of the class variables
			'''
			declensionsdeclensions_number_of_rules = len(result)
			self.declensions_exceptions=[None]*declensionsdeclensions_number_of_rules
			self.declensions_targets = [None]*declensionsdeclensions_number_of_rules
			self.declensions_tags = [None]*declensionsdeclensions_number_of_rules
			self.declensions_replacement = [None]*declensionsdeclensions_number_of_rules
			'''
			Check if the rule has any of the elements 
			'''
			for index,elem in enumerate(result):
				if '@target' in elem.keys():
					self.declensions_targets[index] = elem["@target"]
				else:
					self.declensions_targets[index] = ""
				if '@exceptions' in elem.keys():
					self.declensions_exceptions[index] = elem["@exceptions"]
				else:
					self.declensions_exceptions[index] = ""
				if '@tag' in elem.keys():
					self.declensions_tags[index] = elem["@tag"]
				else:
					self.declensions_tags[index] = ""
				if '#text' in elem.keys():
					self.declensions_replacement[index] = elem["#text"]
				else:
					self.declensions_replacement[index] = ""

			self.declesion_prefix = (doc["regularverbdeclensions"]["prefix"])


				
	def print_verb_normalizer(self):
		for i in range(len(self.declesion_targets)):
			print(i)
			print("---------\n")
			print("Target: " + self.declesion_targets[i])
			print("Tags: " + self.declesion_tags[i])
			print("Exceptions: " + self.declesion_exceptions[i])
			print("Replacement: " + self.declesion_replacement[i])
		print("---------------")
		print("---------------")
		print("---------------")
		print("---------------")

		for i in range(len(self.lexeme_targets)):
			print(i)
			print("---------\n")
			print("Target: " + self.lexeme_targets[i])
			print("Tags: " + self.lexeme_tags[i])
			print("Exceptions: " + self.lexeme_exceptions[i])
			print("Replacement: " + self.lexeme_replacement[i])
		print("---------------")
		print("---------------")
		print("---------------")
		print("---------------")

		for i in range(len(self.conjugation_targets)):
			print(i)
			print("---------\n")
			print("Target: " + self.conjugation_targets[i])
			print("Tags: " + self.conjugation_tags[i])
			print("Exceptions: " + self.conjugation_exceptions[i])
			print("Replacement: " + self.conjugation_replacement[i])


	def normalize_verb(self,token, tag):
		#print("Token de entrada: " + token)
		#choose biggest rule
		bigget_rule_size = 0
		#lemmatized_word = token.lower()
		lemmatized_word = ""
		'''
		Token to lowercase to match the rules
		'''
		normalization = token.lower()
		'''
		Check for every rule it the element matches the target,
		if the tags match and if the element is not an exception

		'''
		'''
		Conjugations (without  prefixes)
		'''

		traco = token[-1]
		if not(traco == "-"):
			traco = ""
		for index,elem in enumerate(self.conjugation_targets):
			desconta_valores=0
			desconta_valores2=0
			res = re.findall(r"\[(?:\w|àáãâéêíóõôúç\-)*\]",self.conjugation_targets[index])
			tem_s = 1
			if(token[-1]=="s"):
				tem_s=0
			if(len(res)>0):
				for elem in res:
					desconta_valores += len(elem)-2
					desconta_valores2 += 2
			desconta_valores=len(self.conjugation_targets[index])-(desconta_valores+desconta_valores2+tem_s)
			word = normalization[:-desconta_valores]

			if( self.conjugation_re_normal[index].fullmatch(normalization)
				and tag.lower() in self.conjugation_tags[index].split("|")
				and not (normalization in self.conjugation_exceptions[index].split("|"))):
					
					'''
					Verificar se a regra a ser aplicada é a regra mais especifica para o caso 
					'''
					lemmatized_word = word + self.conjugation_replacement[index] + traco
					return(lemmatized_word)
					#print("RULE 1")

		'''
		Conjugations (with  prefixes)
		'''

		for index,elem in enumerate(self.conjugation_targets):
			#print("---"+token)
			desconta_valores = 0
			desconta_valores2 = 0
			#print(self.conjugation_targets[index])
			res = re.findall(r"\[(?:\w|àáãâéêíóõôúç\-)*\]",self.conjugation_targets[index])
			tem_s = 1
			if(token[-1]=="s"):
				tem_s=0
			if(len(res)>0):
				for elem in res:
					desconta_valores += len(elem)-2
					desconta_valores2 += 2
			desconta_valores=len(self.conjugation_targets[index])-(desconta_valores+desconta_valores2+tem_s)
			word = normalization[:-desconta_valores]
			

			if( self.conjugation_re[index].fullmatch(normalization)
				and tag.lower() in self.conjugation_tags[index].split("|")
				and not (normalization in self.conjugation_exceptions[index].split("|"))):

					'''
					Verificar se a regra a ser aplicada é a regra mais especifica para o caso 
					'''

					lemmatized_word = word + self.conjugation_replacement[index] + traco
					return(lemmatized_word)
					#print("RULE 1")
		'''
		Regular ver lexemes (without prefixes)
		'''
		for index,elem in enumerate(self.lexeme_targets):
			desconta_valores = 0
			desconta_valores2 = 0
			#print(self.lexeme_targets[index])
			res = re.findall(r"\[(?:\w|àáãâéêíóõôúç\-)*\]",self.lexeme_targets[index])
			tem_s = 1
			if(token[-1]=="s"):
				tem_s=0
			if(len(res)>0):
				for elem in res:
					desconta_valores += len(elem)-2
					desconta_valores2 += 2
			desconta_valores=len(self.lexeme_targets[index])-(desconta_valores+desconta_valores2+tem_s)
			word = normalization[:-desconta_valores]
			#print("-----"+elem+"----"+word)
			if( self.lexeme_re_normal[index].fullmatch(normalization)
				and tag.lower() in self.lexeme_tags[index].split("|")
				and not (normalization in self.lexeme_exceptions[index].split("|"))):

					
					'''
					Verificar se a regra a ser aplicada é a regra mais especifica para o caso 
					'''

					lemmatized_word = self.lexeme_replacement[index] + traco
					return(lemmatized_word)
		'''
		Regular ver lexemes (with prefixes)
		'''
		for index,elem in enumerate(self.lexeme_targets):
			desconta_valores = 0
			desconta_valores2 = 0
			#print(self.lexeme_targets[index])
			res = re.findall(r"\[(?:\w|àáãâéêíóõôúç\-)*\]",self.lexeme_targets[index])
			tem_s = 1
			if(token[-1]=="s"):
				tem_s=0
			if(len(res)>0):
				for elem in res:
					desconta_valores += len(elem)-2
					desconta_valores2 += 2
			desconta_valores=len(self.lexeme_targets[index])-(desconta_valores+desconta_valores2+tem_s)
			word = normalization[:-desconta_valores]
			#print("-----"+elem+"----"+word)
			if( self.lexeme_re[index].fullmatch(normalization)
				and tag.lower() in self.lexeme_tags[index].split("|")
				and not (normalization in self.lexeme_exceptions[index].split("|"))):

					
					'''
					Verificar se a regra a ser aplicada é a regra mais especifica para o caso 
					'''
					lemmatized_word = word + self.lexeme_replacement[index] + traco
					return(lemmatized_word)

		for index,elem in enumerate(self.declesion_targets):
			desconta_valores = 0
			desconta_valores2 = 0
			res = re.findall(r"\[(?:\w|àáãâéêíóõôúç\-)*\]",self.declesion_targets[index])
			tem_s = 1
			if(token[-1]=="s"):
				tem_s=0
			if(len(res)>0):
				for elem in res:
					desconta_valores += len(elem)-2
					desconta_valores2 += 2
			desconta_valores=len(self.declesion_targets[index])-(desconta_valores+desconta_valores2+tem_s)
			word = normalization[:-desconta_valores]
			if( self.declesion_re[index].fullmatch(normalization)
				and tag.lower() in self.declesion_tags[index].split("|")
				and not (normalization in self.declesion_exceptions[index].split("|"))):

					'''
					Verificar se a regra a ser aplicada é a regra mais especifica para o caso 
					'''
					lemmatized_word = word+ self.declesion_replacement[index] + traco
					return(lemmatized_word)
		return(lemmatized_word)

	
	def lexemes_sufixos(self):
		teste = "agigant[eiao]"
		prog = re.compile(teste)
		result = prog.match("agigantaaaaa")
		return result

