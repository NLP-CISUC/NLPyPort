# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 13:03:21 2018

@author: fabio
"""
import warnings
warnings.filterwarnings("ignore")
from collections import Counter
from itertools import chain
from sklearn.model_selection import *
from sklearn.metrics import *
from sklearn.preprocessing import LabelBinarizer,LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import re
import pandas as pd
from pandas import *
import numpy as np
import os
import itertools
import pickle
#import matplotlib.pyplot as plt
from sklearn_crfsuite import CRF
from sklearn_crfsuite import metrics
from sklearn_crfsuite import scorers
import random
from sklearn.model_selection import train_test_split
random.seed(1)

def print_transitions(trans_features):
	string = ""
	for (label_from, label_to), weight in trans_features:
		string += ("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))
		string+="\n"
	return string
def print_state_features(state_features):
	string = ""
	for (attr, label), weight in state_features:
		string+=("%0.6f %-8s %s" % (weight, label, attr))
		string+="\n"
	return string

class GenerateFeatures():
	def __init__(self):
		self.features={}
	def generateMorphologyFeatures(self,word,tag):
		self.features[tag+'contains_punct']=str(0)
		self.features[tag+'word_shape']=''
		for char in word:
			if str(char).isalpha():
				if str(char).islower():
					self.features[tag+'word_shape']+='a'
				else:
					self.features[tag+'word_shape']+='A'
			elif str(char).isdigit():
				self.features[tag+'word_shape']+='#'
			else:
				self.features[tag+'word_shape']+='-'
				self.features[tag+'contains_punct']=str(1)
		self.features[tag+'ends_in_s']=str(word[-1:]=='s')
		self.features[tag+'ends_in_a']=str(word[-1:]=='a')
		self.features[tag+'ascii']=str(len(word)==len(word.encode()))
		self.features[tag+'is_all_lowercase']=str(word.lower()==word and word.isdigit()==False)
		self.features[tag+'is_first_uppercase']=str(word.isupper())
		self.features[tag+'is_complete_uppercase']=str(word.upper()==word and word.isdigit()==False)
		self.features[tag+'is_numeric']=str(word.isdigit())
		self.features[tag+'is_alpha']=str(word.isalpha())
		self.features[tag+'is_alphanumeric']=str(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])',word))))
		self.features[tag+'length']=str(word)
		prefix_suffix_window=5
		for i in range(1,prefix_suffix_window+1):
			self.features[tag+'prefix_'+str(i)]=str(word[:i])
			self.features[tag+'suffix_'+str(i)]=str(word[-i:])
	def wordcontextFeatures(self,word,pos,lemma,tag):
		self.features[tag+'word']=str(word)
		self.features[tag+'pos']=pos
		self.features[tag+'lemma']=str(lemma)
			
def features(document,pos_list,lemma_list,index,useful_features):
	word=document[index]
	pos=pos_list[index]
	lemma=lemma_list[index]
	if index-1>0:
		prev_prev_word=document[index-2]
		prev_prev_pos=pos_list[index-2]
		prev_prev_lemma=lemma_list[index-2]
	else:
		prev_prev_word=''
		prev_prev_pos=''
		prev_prev_lemma=''
	if index>0:
		prev_word=document[index-1]
		prev_pos=pos_list[index-1]
		prev_lemma=lemma_list[index-1]
	else:
		prev_word=''
		prev_pos=''
		prev_lemma=''
	if index<len(document)-1:
		next_word=document[index+1]
		next_pos=pos_list[index+1]
		next_lemma=lemma_list[index+1]
	else:
		next_word=''
		next_pos=''
		next_lemma=''
	if index<len(document)-2:
		next_next_word=document[index+2]
		next_next_pos=pos_list[index+2]
		next_next_lemma=lemma_list[index+2]
	else:
		next_next_word=''
		next_next_pos=''
		next_next_lemma=''
	gen_features=GenerateFeatures()
	if useful_features[0]:
		gen_features.generateMorphologyFeatures(word,'')
		gen_features.generateMorphologyFeatures(prev_word,'prev_')
		gen_features.generateMorphologyFeatures(next_word,'next_')
		gen_features.generateMorphologyFeatures(prev_prev_word,'prev_prev_')
		gen_features.generateMorphologyFeatures(next_next_word,'next_next_')
	if useful_features[1]:
		gen_features.wordcontextFeatures(word,pos,lemma,'')
		gen_features.wordcontextFeatures(prev_word,prev_pos,prev_lemma,'prev_')
		gen_features.wordcontextFeatures(next_word,next_pos,next_lemma,'next_')
		gen_features.wordcontextFeatures(prev_prev_word,prev_prev_pos,prev_prev_lemma,'prev_prev_')
		gen_features.wordcontextFeatures(next_next_word,next_next_pos,next_next_lemma,'next_next_')
	return gen_features.features

def untag(document,option):
	#Passar de colunas para tuples
	if option!='predict':
		#return [str(word) for word,pos,tag in document],[pos for word,pos,tag in document],['' for word,pos,tag in document]
		return [str(word) for word,pos,lemma,tag in document],[pos for word,pos,lemma,tag in document],[lemma for word,pos,lemma,tag in document]
	else:
		#return [str(word) for word,pos in document],[pos for word,pos in document],['' for word,pos in document]
		return [str(word) for word,pos,lemma in document],[pos for word,pos,lemma in document],[lemma for word,pos,lemma in document]

def prepareData(tagged_documents,option,useful_features):
	#Construir o dataset a partir dos ficheiros -> Gerar features para usar no CRF
	X,y=[],[]
	for document in tagged_documents:
		words,postags,lemmas =untag(document,option)
		X.append([features(words,postags,lemmas,index,useful_features) for index in range(len(document))])
		if option!='predict':
			y.append([tag for word,pos,lemmas,tag in document])
	return X,y

def fromListToTuple(data):
	tuple_data=[]
	for l in data:
		tuple_data.append(tuple(l))
	return tuple_data

def fromTuplesToList(data,y):
	dataset=[]
	for i in range(len(data)):
		dataset.append([])
		for j in range(len(data[i])):
			list_j=list(data[i][j])
			list_j.append(y[i][j])
			dataset[i].append(list_j)
	return dataset

def save_model(nome,modelo):
	with open(nome,'wb') as f:
		pickle.dump(modelo,f,protocol=pickle.HIGHEST_PROTOCOL)

def load_model(nome):
	with open(nome,'rb') as f:
		 result = pickle.load(f)
	return result

def run_crf(data,load_file="harem.pickle"):
	useful_features=[True,True]
	X_test=fromListToTuple(data)
	X_teste,y_teste=prepareData([X_test],'predict',useful_features)
	crf = load_model(load_file)
	y_pred=crf.predict(X_teste)
	resultados = []
	for index,elem in enumerate(y_pred[0]):
		resultados.append(str(y_pred[0][index]))
	return resultados

def test_crf(train_file,test_file,model_name=""):
	l1 = [0.015625,0.03125,0.0625,0.125,0.25,0.5,1]
	l2 = [0.03125,0.0625,0.125,0.25,0.5,1,2,4,8,16]
	valores = []
	useful_features=[True,True]
	data=pandas.read_csv(train_file,sep="\t",header=None)
	X_dataset=fromListToTuple(data.iloc[:,[0,1,2,3]].values)
	X_teste,y_teste=prepareData([X_dataset],'test',useful_features)
	#X_teste, test = train_test_split(X_dataset, test_size=0.1)
	X_teste = pd.DataFrame(X_teste).transpose()
	y_teste = pd.DataFrame(y_teste).transpose()

	print(X_teste.shape)
	print(y_teste.shape)	
	X_teste_2 = X_teste
	y_teste_2 = y_teste
	crf = CRF(
		algorithm='lbfgs',
		#c1=0.0625,
		c1=1.0,
		#c2=0.5,
		c2=1.0,
		max_iterations=100,
		all_possible_transitions=False,
		all_possible_states=True,
		verbose=True
	)
	crf.fit(X_teste.values.tolist(), y_teste.values.tolist())
	y_pred=crf.predict(X_teste.values.tolist())
	labels=list(crf.classes_)
	save_model("NP_Final_Macro.pickle",crf)
	string = " "
	string += str(metrics.flat_classification_report(y_teste.values.tolist(), y_pred, labels=labels, digits=3))
	filename = "Results _.txt"
	print("$$$$$$$$$$$")
	print(filename)
	print("$$$$$$$$$$$")
	with open(filename,'a') as f:
		f.write(string)
	


if __name__ == '__main__':
	test_crf("prop_simplified.txt","prop_simplified.txt","")
