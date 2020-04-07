#NLPyPort


The NLPy_Port is a pipeline assembled from the NLTK pipeline, adding and changing its elements for better processing the portuguese that were previouslly created for the NLPPort pipeline.
It suports at the moment the taks of Tokenization, PoS Tagging , Lemmatization and Named Entity Recognition


#Usage

In order to simplify the usage of the NLPyPort pipeline, some structural changes were made. The “exemplo.py” file shows exemples os several use cases.

##How to use the pipeline

Depending on the planed usage, the pipeline may be called in three different ways:

###1  - Default 

text = new_full_pipe( your_input_file )



###2 - Optional arguments

text = new_full_pipe( your_input_file , options = options )



###3 - Optional arguments and pre-load pipeline

config_list = load_congif_to_list() 		# Pre-load the pipeline
text=new_full_pipe( your_input_file , options = options , config_list = config_list)



##Available options

"tokenizer" : True   -> Perform Tokenization

"pos_tagger" : True -> Perform Pos Tagging

"lemmatizer" : True -> Perform Lemmatization

"entity_recognition" : True -> Perform NER

"np_chunking" : True -> Perform NP Chunking

"pre_load" : False -> Preload the pipeline, needs the additional argument “config_list”

"string_or_array" : True -> Set input as being an array or a string


##Returned text

In case of success, the pipeline will return an object of the “Text” class. The properties of this are as follow:
	text.tokens
	text.pos_tags
	text.lemas
	text.entities
	text.np_tags

Additionally, there is a method to return the pipeline in the CoNNL Format:
	text.print_conll()

To separate lines , at the end of each line the additional token EOS is added.


#Credits


Tokenizer and Lemmatizer resource files - Rodrigues, Ricardo, Hugo Gonçalo Oliveira, and Paulo Gomes. "NLPPort: A Pipeline for Portuguese NLP (Short Paper)." 7th Symposium on Languages, Applications and Technologies (SLATE 2018). Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2018.

Lemmatizer design -  Rodrigues, Ricardo, Hugo Gonçalo Oliveira, and Paulo Gomes. "LemPORT: a high-accuracy cross-platform lemmatizer for portuguese." 3rd Symposium on Languages, Applications and Technologies. Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2014.

PoS trainer (adapted from) - https://github.com/fmaruki/Nltk-Tagger-Portuguese

Named Entity Recognition  
	CRF suite - Naoaki Okazaki http://www.chokkan.org/software/crfsuite/
	sklearn-crfsuite wrapper - https://github.com/TeamHG-Memex/sklearn-crfsuite

Corpus
Corpus for PoS tagging training
	MacMorpho - http://nilc.icmc.usp.br/macmorpho/ 
	Floresta Sintá(c)tica - https://www.linguateca.pt/Floresta/corpus.html
	
	

#Citations

To cite and give credits to the pipeline please use the following BibText reference:

@inproceedings{ferreira_etal:slate2019,
	Author = {João Ferreira and Hugo {Gonçalo~Oliveira} and Ricardo Rodrigues},
	Booktitle = {Symposium on Languages, Applications and Technologies (SLATE 2019)},
	Month = {June},
	Note = {In press},
	Title = {Improving {NLTK} for Processing {P}ortuguese},
	Year = {2019}}