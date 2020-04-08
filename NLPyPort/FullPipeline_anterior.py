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
from LemPyPort.LemFunctions import *
from LemPyPort.dictionary import *
from TokPyPort.Tokenizer import *
from TagPyPort.Tagger import *
from CRF.CRF_Teste import *


global_porperties_file = "config/global.properties"

lexical_conversions="PRP:PREP;PRON:PRO;IN:INTERJ;ART:DET;"
floresta.tagged_words(tagset = "pt-bosque")
TokPort_config_file = ""
TagPort_config_file = ""
LemPort_config_file = ""


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



def load_config(config_file="config/global.properties"):
	global TokPort_config_file
	global TagPort_config_file
	global LemPort_config_file
	with open (config_file,'r') as f:
		for line in f:
			if(line[0]!="#"):
				if(line.split("=")[0]=="TokPort_config_file"):
					TokPort_config_file = line.split("=")[1].strip("\n")
				elif(line.split("=")[0]=="TagPort_config_file"):
					TagPort_config_file = line.split("=")[1].strip("\n")
				elif(line.split("=")[0]=="LemPort_config_file"):
					LemPort_config_file = line.split("=")[1].strip("\n")

def load_and_return_config(config_file="config/global.properties"):
	with open (config_file,'r') as f:
		for line in f:
			if(line[0]!="#"):
				if(line.split("=")[0]=="TokPort_config_file"):
					TokPort_config_file = line.split("=")[1].strip("\n")
				elif(line.split("=")[0]=="TagPort_config_file"):
					TagPort_config_file = line.split("=")[1].strip("\n")
				elif(line.split("=")[0]=="LemPort_config_file"):
					LemPort_config_file = line.split("=")[1].strip("\n")
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
	trained_model = "CRF/trainedModels/harem.pickle"
	entidades = run_crf(joined_data,trained_model)

	np_tags = []
	joined_data = join_data(tokens,tags,lemas)
	np_model = "CRF/NP_Final.pickle"
	#Alternative model macro optimized
	#np_model = "CRF/NP_Final_Macro.pickle"
	np_tags = run_crf(joined_data,np_model)
	

	write_simple_connl(tokens,tags,lemas,entidades,np_tags,out_file)
	
	return tokens,tags,lemas,entidades,np_tags



if __name__ == "__main__":
	input_file = "SampleInput/Sample.txt"
	out_file = "SampleOut.txt"
	out_file_2 = "SampleOut2.txt"

	#################################
	#Run the full pipeline for a file
	#################################
	tokens,tags,lemas,entidades,np_tags = full_pipe(input_file,out_file)


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
