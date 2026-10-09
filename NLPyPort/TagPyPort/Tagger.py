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
from pathlib import Path
from NLPyPort._paths import resource

def load_tag_configurations(config_file):
	model_path = ""
	with open(config_file, encoding='utf-8') as g:
		for line in g:
			if(line[0]!="#"):
				if(line.split("=")[0]=="model"):
					model_path = resource(line.split("=")[1].strip('\n'))
	return model_path

def _upgrade_legacy_regexp_tagger(tagger):
	"""Make RegexpTaggers pickled with NLTK <= 3.4 usable on newer NLTK.

	NLTK 3.4 stored the patterns in ``_regexs``; NLTK >= 3.4.5 reads
	``_regexps`` instead, which caused "'RegexpTagger' object has no
	attribute '_regexps'" (issue #7). Rebuild the attribute from the old one
	using the installed NLTK's own constructor so its current pattern type
	is used.
	"""
	from nltk.tag.sequential import RegexpTagger
	if isinstance(tagger, RegexpTagger) and not hasattr(tagger, "_regexps") and hasattr(tagger, "_regexs"):
		patterns = [(getattr(regexp, "pattern", regexp), tag) for regexp, tag in tagger._regexs]
		tagger._regexps = RegexpTagger(patterns)._regexps


def _walk_taggers(tagger, seen=None):
	"""Yield every tagger reachable through Brill initial taggers and backoff chains."""
	if seen is None:
		seen = set()
	if tagger is None or id(tagger) in seen:
		return
	seen.add(id(tagger))
	yield tagger
	yield from _walk_taggers(getattr(tagger, "_initial_tagger", None), seen)
	for sub in getattr(tagger, "_taggers", [])[1:]:
		yield from _walk_taggers(sub, seen)


def load_tagger(model_path):
	# NOTE: the bundled models are pickles shipped with this package; only load trusted files.
	with open(model_path, 'rb') as f:
		tagger = pickle.load(f)
	for sub in _walk_taggers(tagger):
		_upgrade_legacy_regexp_tagger(sub)
	return tagger


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
			if(len(elem[1].split(":"))>1):
				result_tags[i] = elem[1].split(":")[1]
			else:
				result_tags[i] = elem[1]
			i += 1
	return result_tags, tags


if __name__ == "__main__":
	start_time = time.time()
