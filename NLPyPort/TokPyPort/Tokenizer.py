# -*- coding: utf-8 -*-
"""
@author: João Ferreira
"""
import nltk.data
import os
from nltk.corpus import floresta
import nltk
import xmltodict
from pathlib import Path

def load_token_configurations(config_file):
	contractions_path = ""
	clitics_path = ""
	with open(config_file) as g:
		for line in g:
			if(line[0]!="#"):
				if(line.split("=")[0]=="contractions"):
					contractions_path = Path("NLPyPort/"+line.split("=")[1].strip('\n'))
				elif(line.split("=")[0]=="clitics"):
					clitics_path = Path("NLPyPort/"+line.split("=")[1].strip('\n'))
	return contractions_path,clitics_path

def get_input_from_file(fileinput):
	text = []
	with open(fileinput,'r') as f:
		for line in f:
			text .append(line)
	return text

def replace_contrations(contractions_path,tokens):
	tokens_after_contractions = []
	encontrou = 0

	#Check if tokens contain contractions
	#If so, change them to the most extended form
	with open(contractions_path) as fd:
		doc = xmltodict.parse(fd.read())
		result = (doc["contractions"]["replacement"])
		for tok in tokens:
			encontrou = 0
			token2 = tok
			for elem in result:
				if(tok==elem['@target']):
					encontrou=1
					subs = elem['#text'].split(" ")
					for part in subs:
						tokens_after_contractions.append(part)
			#if word in not contration add it as it was
			if(encontrou==0):
				tokens_after_contractions.append(token2)
	return tokens_after_contractions

def replace_clitics(clitics_path,tokens):
	tokens_after_clitics =[]
	with open(clitics_path) as fd:
		doc2 = xmltodict.parse(fd.read())
		result2 = (doc2["clitics"]["replacement"])
		for tok2 in tokens:
			if(len(tokens)>0):
				encontrou = 0
				token2 = tok2
				for elem2 in result2:
					if(tok2==elem2['@target']):
						encontrou=1
						subs = elem2['#text'].split(" ")
						for part in subs:
							tokens_after_clitics.append(part)
				if(encontrou==0):
					withslash = tok2.split("-")
					if(len(withslash)>1):
						nova_palavra = ""
						for parte in withslash:
							if(parte!=withslash[0]):
								nova_palavra +="-" + parte
						encontrou = 0
						token2 = tok2
						for elem2 in result2:
							if(nova_palavra==elem2['@target']):
								encontrou=1
								subs = elem2['#text'].split(" ")
								for part in subs:
									tokens_after_clitics.append(part)
						#if word in not contration add it as it was
						if(encontrou==1):
							tokens_after_clitics.append(withslash[0]+"-")
				if(encontrou==0):
					tokens_after_clitics.append(token2)
			else:
				tokens_after_clitics.append(tokens)
	return tokens_after_clitics	

def nltk_tokenize(text):
	result = []
	for line in text:
		tok=(nltk.word_tokenize(line))
		for elem in tok:
			result.append(elem)
		result.append("EOS")
	return result

def nlpyport_tokenize_from_string(text,TokPort_config_file):
	#define the tagset being used
	#print(text)
	floresta.tagged_words(tagset = "pt-bosque")
	contractions_path = ""
	clitics_path = ""
	tokens=[]
	tokens_after_contractions = []
	tokens_after_clitics = []
	#get the directory of the resources
	contractions_path,clitics_path = load_token_configurations(TokPort_config_file)
	text_list = []
	if(isinstance(text, str)):
		text = text.replace("\n"," EOS")
		if("EOS" not in text):
			text+=" EOS"
		text_list = [text]

		#print(text)
	else:
		current_text = ""
		for elem in text:
			elem = elem.replace("\n"," EOS\n")
			has_eof = 0
			if("EOS" not in elem):
				elem+=" EOS\n"
			if elem != '\n':
				current_text += elem
		if(current_text!=""):
			text_list.append(current_text)
	
	text = text_list
	#Do the actual tokenization
	#print(str(text_list))
	tokens = nltk_tokenize(text)

	#print(tokens)
	novos_tokens = []
	for i in range(len(tokens)):
		if(tokens[i]!="\n"):
			novos_tokens.append(tokens[i])
	tokens = novos_tokens
	tokens_after_contractions = replace_contrations(contractions_path,tokens)

	#Check if tokens contain clitics
	#If so, change them to the most extended form
	tokens_after_clitics =replace_clitics(clitics_path,tokens_after_contractions)
	final_tokens =[]
	if not(isinstance(text, str)):
		for tok in tokens_after_clitics[:-1]:
			final_tokens.append(tok)
	else:
		for tok in tokens_after_clitics:
			final_tokens.append(tok)
	return final_tokens

def nlpyport_tokenizer(fileinput,TokPort_config_file):
	#define the tagset being used
	floresta.tagged_words(tagset = "pt-bosque")
	contractions_path = ""
	clitics_path = ""
	text = " "
	tokens=[]
	tokens_after_contractions = []
	tokens_after_clitics = []
	#get the directory of the resources
	contractions_path,clitics_path = load_token_configurations(TokPort_config_file)

	#Get tokens from input file, one by line
	text = get_input_from_file(fileinput)

	#Do thea actual tokenization
	tokens = nltk_tokenize(text)
	#for i in range(len(tokens)):
	#	if(tokens[i])=="#":
	#		tokens[i] = "\n"
	tokens_after_contractions = replace_contrations(contractions_path,tokens)

	#Check if tokens contain clitics
	#If so, change them to the most extended form
	tokens_after_clitics =replace_clitics(clitics_path,tokens_after_contractions)
	final_tokens =[]
	for tok in tokens_after_clitics:
		final_tokens.append(tok)
	return final_tokens

'''
if __name__ == '__main__':
	print(nlpyport_tokenizer("EntradaCadeiaTotal.txt"))
'''
