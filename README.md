#############
NLPy_Port
#############

The NLPy_Port is a pipeline assembled from the NLTK pipeline, adding and changing its elements for better processing the portuguese that were previouslly created for the NLPPort pipeline.
It suports at the moment the taks of Tokenization, PoS Tagging , Lemmatization and Named Entity Recognition

#############
Usage
#############

To process text into the Conll format simply call the function full_pipe(<input_file>,<output_file>) for your file.
This function will write to the file <output_file>. Aditionally it will return the obtain objects - tokens,tags,lemas,entidades.
If no <output_file> is given, the function will only print and return the results, but will not store them.

#############
Aditional options
#############

There are some other options available for convenience in the full_pipe function:
	-The load_manual(<input_file>) loads a file containing the token followed by a space and then its tag, one token per line
		This allows for loading resources that are already tagged.
	-The write_lemmas_only(lemas,<output_file>) function takes the lemmas and re-writes the file using these instead of the tokens


#############
Credits
#############

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
	
	
#############
Citations
#############

To cite and give credits to the pipeline please use the following BibText reference:

@inproceedings{ferreira_etal:slate2019,
	Author = {João Ferreira and Hugo {Gonçalo~Oliveira} and Ricardo Rodrigues},
	Booktitle = {Symposium on Languages, Applications and Technologies (SLATE 2019)},
	Month = {June},
	Note = {In press},
	Title = {Improving {NLTK} for Processing {P}ortuguese},
	Year = {2019}}
