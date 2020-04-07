from NLPyPort.FullPipeline import *
import sys

#########################
#Example for a file input
#########################

options = {
			"tokenizer" : True,
			"pos_tagger" : True,
			"lemmatizer" : True,
			"entity_recognition" : True,
			"np_chunking" : True,
			"pre_load" : False,
			"string_or_array" : False
}

input_file="input_sample.txt"

text=new_full_pipe(input_file,options=options)
if(text!=0):
		text.print_conll()

'''
#########################
#Example for an array input
#########################

options = {
			"tokenizer" : True,
			"pos_tagger" : True,
			"lemmatizer" : True,
			"entity_recognition" : True,
			"np_chunking" : True,
			"pre_load" : False,
			"string_or_array" : True
}

input_array = ['Primeira frase', 'Segunda frase', 'Terceira frase']
text=new_full_pipe(input_array,options=options)
if(text!=0):
		text.print_conll()

#########################
#Example for an string input
#########################
options = {
			"tokenizer" : True,
			"pos_tagger" : True,
			"lemmatizer" : True,
			"entity_recognition" : True,
			"np_chunking" : True,
			"pre_load" : False,
			"string_or_array" : True
}

input_string = "String para teste"
text=new_full_pipe(input_string,options=options)

if(text!=0):
		text.print_conll()


#########################
#Pipeline with pre-load example 
#########################
options = {
			"tokenizer" : True,
			"pos_tagger" : True,
			"lemmatizer" : True,
			"entity_recognition" : True,
			"np_chunking" : True,
			"pre_load" : False,
			"string_or_array" : True
}
config_list = load_congif_to_list() #This pre-loads the program, makes the start slower but it's faster for larger text
input_string = "String para teste"
text=new_full_pipe(input_string,options=options,config_list=config_list)

if(text!=0):
		text.print_conll()
'''


