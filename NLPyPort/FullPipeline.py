# -*- coding: utf-8 -*-
"""
@author: João Ferreira
"""
import nltk.data
import os
from nltk.corpus import floresta
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus.reader import TaggedCorpusReader
from nltk.tokenize import LineTokenizer
from nltk.corpus import treebank
from nltk.metrics import accuracy
from nltk.corpus import machado
import pickle
import nltk
import time
import xmltodict

from NLPyPort.LemPyPort.LemFunctions import *
from NLPyPort.LemPyPort.dictionary import *
from NLPyPort.TokPyPort.Tokenizer import *
from NLPyPort.TagPyPort.Tagger import *
from NLPyPort.CRF.CRF_Teste import *
from NLPyPort.text import *
from pathlib import Path


global_porperties_file = Path("NLPyPort/config/global.properties")

lexical_conversions="PRP:PREP;PRON:PRO;IN:INTERJ;ART:DET;"
floresta.tagged_words(tagset = "pt-bosque")
TokPort_config_file = ""
TagPort_config_file = ""
LemPort_config_file = ""
debug = False

def debug_print(string):
	global debug
	if(debug==True):
		print(string)

def load_congif_to_list():
	config_list=[]
	TokPort_config_file,TagPort_config_file,LemPort_config_file = load_and_return_config()
	config_list.append(TokPort_config_file)
	config_list.append(TagPort_config_file)
	config_list.append(LemPort_config_file)
	for elem in load_and_return_lemmatizer(LemPort_config_file):
		config_list.append(elem)
	
	return config_list


def unload_config_from_list(config_list):
	TokPort_config_file = config_list[0]
	TagPort_config_file = config_list[1]
	LemPort_config_file = config_list[2]
	adverb_norm = config_list[3]
	number_norm = config_list[4]
	superlative_norm = config_list[5]
	augmentative_norm = config_list[6]
	diminutive_norm = config_list[7]
	gender_norm = config_list[8]
	gender_name_norm = config_list[9]
	verb_norm = config_list[10]
	ranking = config_list[11]
	novo_dict = config_list[12]
	return TokPort_config_file,TagPort_config_file,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict



def load_config(config_file=Path("NLPyPort/config/global.properties")):
	global TokPort_config_file
	global TagPort_config_file
	global LemPort_config_file
	with open (config_file,'r') as f:
		for line in f:
			if(line[0]!="#"):
				if(line.split("=")[0]=="TokPort_config_file"):
					TokPort_config_file = Path("NLPyPort/"+line.split("=")[1].strip("\n"))
				elif(line.split("=")[0]=="TagPort_config_file"):
					TagPort_config_file = Path("NLPyPort/"+line.split("=")[1].strip("\n"))
				elif(line.split("=")[0]=="LemPort_config_file"):
					LemPort_config_file = Path("NLPyPort/"+line.split("=")[1].strip("\n"))

def load_and_return_config(config_file=Path("NLPyPort/config/global.properties")):
	with open (config_file,'r') as f:
		for line in f:
			if(line[0]!="#"):
				if(line.split("=")[0]=="TokPort_config_file"):
					TokPort_config_file = Path("NLPyPort/"+line.split("=")[1].strip("\n"))
				elif(line.split("=")[0]=="TagPort_config_file"):
					TagPort_config_file = Path("NLPyPort/"+line.split("=")[1].strip("\n"))
				elif(line.split("=")[0]=="LemPort_config_file"):
					LemPort_config_file = Path("NLPyPort/"+line.split("=")[1].strip("\n"))
	return TokPort_config_file,TagPort_config_file,LemPort_config_file


def load_and_return_lemmatizer(LemPort_config_file):
	adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict = nlpyport_lematizer_loader(LemPort_config_file)
	return [adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict]



# """word tokenizer"""
def tokenize(fileinput,tok_config=""):
	if(tok_config==""):
		tok_config = TokPort_config_file
	return nlpyport_tokenizer(fileinput,tok_config)

def tokenize_from_string(stringinput,tok_config=""):
	if(tok_config==""):
		tok_config = TokPort_config_file
	return nlpyport_tokenize_from_string(stringinput,tok_config)

def tag(tokens,tag_config=""):
	if(tag_config==""):
		tag_config = TagPort_config_file
	return nlpyport_pos(tokens,tag_config)


def lematizador_preloaded(tokens,tags):
	global LemPort_config_file
	mesmas = 0
	alteradas = 0
	resultado = nlpyport_lematizer(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
	return resultado

def lematizador_normal(tokens,tags):
	global LemPort_config_file
	mesmas = 0
	alteradas = 0
	resultado = nlpyport_lematizer(tokens,tags,LemPort_config_file)
	return resultado

def load_manual(file):
	tokens = []
	tags = []
	f =  open(file,'r')
	alteradas = 0
	mesmas = 0
	for line in f:
		res = line.split(" ")
		if(len(res)>1):
			tokens.append(res[0])
			tags.append(res[1].split('\n')[0])
	return tokens,tags

def write_lemmas_only_text(lem,file="testes.txt"):
	for elem in lem:
		with open(file,'a') as f:
			if(elem == '\n'):
				f.write('\n')
			else:
				f.write(str(elem)+" ")

def write_simple_connl(tokens,tags,lems,ents,nps,file=""):
	linhas = 0
	if(file != ""):
		for index in range(len(tokens)):
			with open(file,'a') as f:
				if(tokens[index] == "\n"):
					f.write("\n")
					linhas = 0
				else:
					linhas += 1
					f.write(str(linhas) + ", " + str(tokens[index] + ", " +str(lems[index]) + ", " + str(tags[index])+", "+str(ents[index]) + ", " + str(nps[index])+"\n"))
	else:
		for index in range(len(tokens)):
			if(tokens[index] == "\n"):
				print("\n")
				linhas = 0
			else:
				linhas += 1
				print(str(linhas) + ", " + str(tokens[index]) + ", " +str(lems[index]) + ", " + str(tags[index]) + ", " + str(nps[index]))

def lem_file(out,token,tag):
	lem = []
	ent = []
	lem = lematizador_normal(token,tag)
	with open(out,"wb") as f:
		for i in range(len(token)):
			line = token[i] +"\t" +tag[i] + "\t" + lem[i]  + "\n"
			f.write((line).encode('utf8'))
	return lem

def join_data(tokens,tags,lem):
	data = []
	for i in range(len(tokens)):
		dados = []
		dados.append(tokens[i]) 
		dados.append(tags[i]) 
		dados.append(lem[i]) 
		data.append(dados)
	return data

def full_pipe(input_file,out_file=""):

	#load the pipeline configurations
	load_config()
	
	#############
	#Tokenize
	#############
	
	tokens = tokenize(input_file)


	#############
	#Replace the privious line by these lines if you want to tokenize
	#from a string or from a list of strings rather than a file
	#############
	#string_input = input_file  # this should be either a list or a string
	#tokens = tokenize_from_string(string_input)

	
	#############
	#Pos
	#############
	tags,result_tags = tag(tokens)
	
	#### optional - use a file with tokens and tags as input
	#tokens,tags = load_manual(input_file)
	#tokens,tags = load_manual("TokPyPort/conll_tagged_text_all.txt")

	#############
	#Lemmatizer
	#############
	lemas = lematizador_normal(tokens,tags)
	#Re-write the file with the lemas
	#write_lemmas_only_text(lemas,"File.txt")

	###################
	#Entity recognizer
	###################

	entidades = []
	joined_data = join_data(tokens,tags,lemas)
	trained_model = "CRF/trainedModels/harem.pickle"
	entidades = run_crf(joined_data,trained_model)


	###################
	#NP chunking
	###################

	np_tags = []
	joined_data = join_data(tokens,tags,lemas)
	np_model = "CRF/NP_Final.pickle"
	#Alternative model macro optimized
	#np_model = "CRF/NP_Final_Macro.pickle"

	np_tags = run_crf(joined_data,np_model)
	


	write_simple_connl(tokens,tags,lemas,entidades,np_tags,out_file)

	return tokens,tags,lemas,entidades,np_tags

def new_full_pipe(input_file,options=[],config_list=[]):
	text = Text()
	if(options==[]):
		options = {
			"tokenizer" : True,
			"pos_tagger" : True,
			"lemmatizer" : True,
			"entity_recognition" : True,
			"np_chunking" : True,
			"pre_load" : False,
			"string_or_array" : False
		}

	###########################
	#Acrescentar a forma de fazer so load de cada parte da pipeline?
	#Acrescentar excepção se ficheiro nao exisitr
	###########################

	if("pre-load" in options):
		if(options["pre-load"]==True):
			if(config_list!=[]):
				TokPort_config_file,TagPort_config_file,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict = unload_config_from_list(config_list)
				debug_print("Pipeline using pre-loaded models.")
			else:
				print("To use the pre-load option a list of loaded configurations must be passed.")
				return 0
		elif(options["pre-load"]==False):
			load_config()
			debug_print("Pre-load set to false, configurations loaded")
	else:
		options["pre-load"] = False
		load_config()
		debug_print("No pre-load choosen, pre-load set to default (false), configurations loaded")

	if(not("pos_tagger" in options) and not("lemmatizer" in options) and not("entity_recognition" in options) and not("np_chunking") in options):
		print("No text processing option given, performing the full pipeline processement.")
		options["tokenizer"] = True
		options["pos_tagger"] = True
		options["lemmatizer"] = True
		options["entity_recognition"] = True
		options["np_chunking"] = True
		options["pre-load"] = False

	if("tokenizer" in options):
		if(options["tokenizer"]==True):
			debug_print("Tokenizer is True")
			if("string_or_array" in options):
				if(options["string_or_array"]==False):
					if(options["pre-load"]==False):
						tokens = tokenize(input_file)
						text.set_tokens(tokens)
						debug_print("Pre-load option set to False, tokens gotten")
					else:
						tokens = tokenize(input_file,TokPort_config_file)
						text.set_tokens(tokens)
						debug_print("Pre-load option set to True, Tokens gotten")
				else:
					if(options["pre-load"]==False):
						debug_print("Pre-load is False")
						tokens = tokenize_from_string(input_file)
						text.set_tokens(tokens)
					else:
						debug_print("Pre-load is True")
						tokens = tokenize_from_string(input_file,TokPort_config_file)
						text.set_tokens(tokens)
			else:
				if(options["pre-load"]==False):
						tokens = tokenize(input_file)
						text.set_tokens(tokens)
						debug_print("Pre-load option set to False, tokens gotten")
				else:
					tokens = tokenize(input_file,TokPort_config_file)
					text.set_tokens(tokens)
					debug_print("Pre-load option set to True, Tokens gotten")
		else:
			##########################
			#Alterar, no caso se não haver tokenizer necessário passar uma list
			##########################
			if("string_or_array" in options):
				if(options["string_or_array"]==True):
					print("If no tokenization is needed please give the input as an array os tring and set 'string_or_array' to False")
					return 0
			#If no data given assume its a file
				else:
					tokens = tokenize_from_string(input_file,TokPort_config_file)
					text.set_tokens(tokens)
	if("pos_tagger" in options):
		if(options["pos_tagger"] == True):
				debug_print("Pos_tagger is True")
				if(options["pre-load"]==False):
					tags,result_tags = tag(text.tokens)
					text.set_pos_tags(tags)
					debug_print("Pre-load option set to False, Pos-tags gotten")
				else:
					tags,result_tags = tag(text.tokens,TagPort_config_file)
					text.set_pos_tags(tags)
					debug_print("Pre-load option set to True, Pos-tags gotten")
		else:
			make_pos = False
			if( "lemmatizer" in options):
				if(options["lemmatizer"]==True):
					if(options["pre-load"]==False):
						tags,result_tags = tag(text.tokens)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					else:
						tags,result_tags = tag(text.tokens,TagPort_config_file)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					make_pos = True
			if( "entity_recognition" in options and make_pos==False):
				if(options["entity_recognition"]==True):
					if(options["pre-load"]==False):
						tags,result_tags = tag(text.tokens)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					else:
						tags,result_tags = tag(text.tokens,TagPort_config_file)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					make_pos = True
			if( "np_chunking" in options and make_pos==False):
				if(options["np_chunking"]==True):
					if(options["pre-load"]==False):
						tags,result_tags = tag(text.tokens)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					else:
						tags,result_tags = tag(text.tokens,TagPort_config_file)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					make_pos = True
	else:
			make_pos = False
			if( "lemmatizer" in options):
				if(options["lemmatizer"]==True):
					if(options["pre-load"]==False):
						tags,result_tags = tag(text.tokens)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					else:
						tags,result_tags = tag(text.tokens,TagPort_config_file)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					make_pos = True
			if( "entity_recognition" in options and make_pos==False):
				if(options["entity_recognition"]==True):
					if(options["pre-load"]==False):
						tags,result_tags = tag(text.tokens)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					else:
						tags,result_tags = tag(text.tokens,TagPort_config_file)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					make_pos = True
			if( "np_chunking" in options and make_pos==False):
				if(options["np_chunking"]==True):
					if(options["pre-load"]==False):
						tags,result_tags = tag(text.tokens)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					else:
						tags,result_tags = tag(text.tokens,TagPort_config_file)
						text.set_pos_tags(tags)
						debug_print("Pos tagging was made since it's needed for other elements of the pipeline.")
					make_pos = True

	if("lemmatizer" in options):
		if(options["lemmatizer"] == True):
				debug_print("Lemmatizer is True")
				if(options["pre-load"]==False):
					lemas = lematizador_normal(tokens,tags)
					text.set_lemas(lemas)
					debug_print("Pre-load option set to False, Lemmas gotten")
				else:
					lemas = nlpyport_lematizer_preload(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
					text.set_lemas(lemas)
					debug_print("Pre-load option set to True, Lemmas gotten")
		else:
			make_lem = False
			if( "entity_recognition" in options and make_lem==False):
					if(options["entity_recognition"]==True):
						if(options["pre-load"]==False):
							lemas = lematizador_normal(tokens,tags)
							text.set_lemas(lemas)
							debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
						else:
							lemas = nlpyport_lematizer_preload(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
							text.set_lemas(lemas)
							debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
						make_lem = True
			if( "np_chunking" in options and make_lem==False):
				if(options["np_chunking"]==True):
					if(options["pre-load"]==False):
						lemas = lematizador_normal(tokens,tags)
						text.set_lemas(lemas)
						debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
					else:
						lemas = nlpyport_lematizer_preload(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
						text.set_lemas(lemas)
						debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
					make_lem = True
	else:
		make_lem = False
		if( "entity_recognition" in options and make_lem==False):
				if(options["entity_recognition"]==True):
					if(options["pre-load"]==False):
						lemas = lematizador_normal(tokens,tags)
						text.set_lemas(lemas)
						debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
					else:
						lemas = nlpyport_lematizer_preload(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
						text.set_lemas(lemas)
						debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
					make_lem = True
		if( "np_chunking" in options and make_lem==False):
			if(options["np_chunking"]==True):
				if(options["pre-load"]==False):
					lemas = lematizador_normal(tokens,tags)
					text.set_lemas(lemas)
					debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
				else:
					lemas = nlpyport_lematizer_preload(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
					text.set_lemas(lemas)
					debug_print("Lemmatization was made since it's needed for other elements of the pipeline.")
				make_lem = True

	if("entity_recognition" in options):
		if(options["entity_recognition"] == True):
				debug_print("Entity_recognition is True")
				joined_data = join_data(text.tokens,text.pos_tags,text.lemas)
				trained_model = "NLPyPort/CRF/trainedModels/harem.pickle"
				entidades = run_crf(joined_data,trained_model)
				text.set_entities(entidades)
				debug_print("Entities gotten")

	if("np_chunking" in options):
		if(options["np_chunking"] == True):
				debug_print("Np_chunking is True")
				np_tags = []
				joined_data = join_data(tokens,tags,lemas)
				np_model = "NLPyPort/CRF/NP_Final.pickle"
				np_tags = run_crf(joined_data,np_model)
				text.set_np_tags(np_tags)
				debug_print("NP-Chunks gotten")
	
	return text




def full_pipe_preload(input_file,config_list,out_file=""):
	TokPort_config_file,TagPort_config_file,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict = unload_config_from_list(config_list)
	
	
	#############
	#Tokenize
	#############

	tokens = tokenize(input_file,TokPort_config_file)

	#############
	#Replace the privious line by these lines if you want to tokenize
	#from a string or from a list of strings rather than a file
	#############
	#string_input = input_file  # this should be either a list or a string
	#tokens = tokenize_from_string(string_input,TokPort_config_file)

	
	#############
	#Pos
	#############
	tags,result_tags = tag(tokens,TagPort_config_file)

	#############
	#Lemmatizer
	#############
	lemas = nlpyport_lematizer_preload(tokens,tags,LemPort_config_file,adverb_norm,number_norm,superlative_norm,augmentative_norm,diminutive_norm,gender_norm,gender_name_norm,verb_norm,ranking,novo_dict)
	#Re-write the file with the lemas only
	#write_lemmas_only_text(lemas,"File.txt")

	###################
	#Entity recognition
	###################
	entidades = []
	joined_data = join_data(tokens,tags,lemas)
	trained_model = "NLPyPort/CRF/trainedModels/trainedModels/harem.pickle"
	entidades = run_crf(joined_data,trained_model)

	np_tags = []
	joined_data = join_data(tokens,tags,lemas)
	np_model = "NLPyPort/CRF/trainedModels/NP_Final.pickle"
	#Alternative model macro optimized
	#np_model = "CRF/NP_Final_Macro.pickle"
	np_tags = run_crf(joined_data,np_model)
	

	write_simple_connl(tokens,tags,lemas,entidades,np_tags,out_file)
	
	return tokens,tags,lemas,entidades,np_tags

####################
#Alterar NER e NP para nao devolver nada em casos em que esta vazio
#Colocar togas tags NP em maiúscula
####################


if __name__ == "__main__":
	input_file = "SampleInput/Sample.txt"
	out_file = "SampleOut.txt"
	out_file_2 = "SampleOut2.txt"
	frase_input = "Sou uma frase de input!"
	array_input = ["Sou uma frase de input!","Mas faço parte de um array"]
	#################################
	#Run the full pipeline for a file
	#################################
	options = {"string_or_array":True,"pre-load":True,"tokenizer":True,"lemmatizer":True,"entity_recognition":True,"np_chunking":True}
	config_list = load_congif_to_list()
	#text = new_full_pipe("SampleInput/Sample.txt",{"string_or_array":False,"pre-load":True,"tokenizer":False,"pos_tagger":True,"lemmatizer":True,"entity_recognition":False,"np_chunking":True},config_list)
	text = new_full_pipe(input_file=array_input,options={"string_or_array":True})
	if(text!=0):
		text.print_connl()
	#print(text.tokens)


	#######################################################################
	#Optional pre-load
	#######################################################################
	####
	#Pre-load the configurations
	####
	#config_list = load_congif_to_list()

	####
	#Run the pipeline
	####
	#full_pipe_preload(input_file,config_list,out_file_2)
