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
import spacy
import xmltodict
from LemPyPort.LemFunctions import *
from LemPyPort.dictionary import *
from TokPyPort.Tokenizer import *
from TagPyPort.Tagger import *


global_porperties_file = "config/global.properties"

lexical_conversions="PRP:PREP;PRON:PRO;IN:INTERJ;ART:DET;"
floresta.tagged_words(tagset = "pt-bosque")
TokPort_config_file = ""
TagPort_config_file = ""
LemPort_config_file = ""

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
# """word tokenizer"""
def tokenize(fileinput):
	return nlpyport_tokenizer(fileinput,TokPort_config_file)

def tag(tokens):
	return nlpyport_pos(tokens,TagPort_config_file)


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
		with open("testes.txt",'a') as f:
			if(elem == "#"):
				f.write('\n')
			else:
				f.write(str(elem)+" ")

def write_simple_connl(tokens,tags,lems,file=""):
	linhas = 0
	if(file != ""):
		for index in range(len(tokens)):
			with open(file,'a') as f:
				if(tokens[index] == "#"):
					f.write("\n")
					linhas = 0
				else:
					linhas += 1
					f.write(str(linhas) + ", " + str(tokens[index] + ", " +str(lems[index] + ", " + str(tags[index]))+"\n"))
	else:
		for index in range(len(tokens)):
			if(tokens[index] == "#"):
				print("\n")
				linhas = 0
			else:
				linhas += 1
				print(str(linhas) + ", " + str(tokens[index] + ", " +str(lems[index] + ", " + str(tags[index]))))

if __name__ == "__main__":
	start_time = time.time()
	load_config()
	#############
	#Tokenize
	#############

	tokens = tokenize("TokPyPort/EntradaCadeiaTotal.txt")
	
	#############
	#Pos
	#############
	tags,result_tags = tag(tokens)
	
	#### Pre load a file with tokens and tags
	#tokens,tags = load_manual("TokPyPort/testesReduzidos.txt")


	#############
	#Lemmatizer
	#############
	lem = lematizador_normal(tokens,tags)
	#Re-write the file with the lemas
	write_lemmas_only_text(lem,"Results.txt")
	#Write all in connl format

	#write_simple_connl(tokens,tags,lem,"ResultConnl.txt")
	
	print("--- %s Seconds ---" % (time.time() - start_time))

