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

def load_tag_configurations(config_file):
	model_path = ""
	with open(config_file) as g:
		for line in g:
			if(line[0]!="#"):
				if(line.split("=")[0]=="model"):
					model_path = line.split("=")[1].strip('\n')
	return model_path

def load_tagger(model_path):
	f = open(model_path, 'rb')
	return (pickle.load(f))


def nlpyport_pos(token,config_file):
	model_path = ""
	model_path = load_tag_configurations(config_file)
	tagger = load_tagger(model_path)
	tags = [tagger.tag(token)]
	i = 0
	result_tags = [None] * len(token)
	result_toks = [None] * len(token)
	for tag in tags:
		for elem in tag:
			result_tags[i] = elem[1]
			i += 1
	return result_tags, tags


if __name__ == "__main__":
	start_time = time.time()
