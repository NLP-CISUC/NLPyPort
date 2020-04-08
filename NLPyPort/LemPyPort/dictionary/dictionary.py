from NLPyPort.LemPyPort.dictionary.dictionary_entry import *
class dictionary:
    def __init__(self):
        self.dictionary_list = {}

    def load(self,input_file):
        inflected_form = ""
        lemma = ""
        part_of_speech = ""
        subcategory = ""
        morph_attributes = ""
        with open(input_file,'r') as f:
            for line in f:
                if(len(line)>0 and not (line[0]=="#")):
                    if(("." in line and "," in line) \
                    and (line.find(".")>(line.find(",")+1)) \
                    and (line.find(".") +1<len(line)) \
                    and (not (line[line.find(".")+1] == ":") \
                        or (not line[line.find(".")+1] == "+"))):
                        #print(line)
                        inflected_form = line[0:line.find(",")]
                        #print("inflected:" + inflected_form)
                        lemma = line[line.find(",")+1:line.find(".")]
                        #print("lemma:" + lemma)

                        if("+" in line):
                            part_of_speech = line[line.find(".")+1:line.find("+")]
                            #print("Pos1: " + part_of_speech)
                        elif (":" in line):
                            part_of_speech = line[line.find(".")+1:line.find(":")]
                            #print("Pos2: " + part_of_speech)
                        else:
                            part_of_speech =  line[line.find(".")+1:]
                            #print("Pos3: " + part_of_speech)
                        if("+" in line):
                            if(":" in line):
                                subcategory = line[line.find("+")+1:line.find(":")]
                                #print("Subcat1: " + subcategory)
                            else :
                                subcategory = line[line.find("+"):]
                                #print("Subcat2: " + subcategory)
                        entry = dictionary_entry(inflected_form,lemma,part_of_speech,subcategory,morph_attributes)
                        #if(entry.inflected_form=="abelha" and entry.part_of_speech=="V"):
                        #    print("---Ok---")
                        self.add(entry)
                        #print(new_entry)
                        #entry.print_entry()
                        #self.print_dictionary_list()
                        #print(self.contains("murchos"))
                        #print(self.contains("murchos","V"))
                        #print(self.retrive_lemas("murchos","V"))
                        #print(self.retrive_entries("murchos"))
        #print(self.remove("murchos","V"))
        #print("------")
        #print(self.remove("murchos","p"))
        #print(self.remove("murchos"))

    def add(self,entry):
        entry_set = self.dictionary_list.get(entry.inflected_form)
        if (entry_set == None ):
            entry_set = []
        entry_set.append(entry)
        self.dictionary_list[entry.inflected_form] = entry_set

    def remove(self,inflected_form):
        removed_entries = self.dictionary_list.pop(inflected_form,None)
        if(removed_entries is not None):
            return removed_entries
        return None

    def remove(self,inflected_form,part_of_speech):
        entry_set = []
        entry_set.append(self.dictionary_list.pop(inflected_form,None))
        #print(entry_set[0].inflected_form)
        remaining_entries = []
        removed_entries = []
        if(entry_set[0] is not None):
            for elem in entry_set:
                if((elem.inflected_form == inflected_form)\
                and elem.part_of_speech == part_of_speech):
                    removed_entries.append(elem)
                else:
                    remaining_entries.append(elem)
            if(len(remaining_entries)>0):
                self.dictionary_list[inflected_form]=remaining_entries[0]
            if(len(removed_entries)>0):
                return removed_entries[0]
        else:
            return None



    def print_dictionary_list(self):
        for elem in self.dictionary_list:
            print(elem+ " " +str(self.dictionary_list[elem].print_entry()))
            

    def contains(self,inflected_form):
        return inflected_form in self.dictionary_list

    def contains(self,inflected_form,part_of_speech):
        if(inflected_form in self.dictionary_list):
            entry = self.dictionary_list[inflected_form]
            for elem in entry:
                if(part_of_speech in elem.part_of_speech):
                    return True
        return False
    
    def retrive_lemas(self,inflected_form,part_of_speech):
        lemas=[]
        if(inflected_form in self.dictionary_list):
            entry = self.dictionary_list[inflected_form]
            for elem in entry:
                if(part_of_speech in elem.part_of_speech):
                    lemas.append(elem.lemma)
        return lemas

    def retrive_entries(self,inflected_form):
        entries=[]
        if(inflected_form in self.dictionary_list):
            entry = self.dictionary_list[inflected_form]
            for elem in entry:
                if(not(elem == [])):
                    entries.append(elem.inflected_form)
        return entries

    '''
      public DictionaryEntry[] retrieveEntries(String inflectedForm) {
        HashSet<DictionaryEntry> entries = new HashSet<DictionaryEntry>();
        if (dictionary.containsKey(inflectedForm)) {
        entries = dictionary.get(inflectedForm);
        }
        return entries.toArray(new DictionaryEntry[entries.size()]);
    }
    '''
    #retrieve_all_entries

    # retrive_lexicon

if __name__ == "__main__":
    novo_dict = dictionary()
    novo_dict.load("Label-Delaf_pt_v4_1.dic")
    print(novo_dict.retrive_lemas("abelha","N"))
    print(novo_dict.contains("abelha","N"))
    print(novo_dict.retrive_lemas("abelha","V"))
    print(novo_dict.retrive_entries("abelha"))
    print(novo_dict.contains("abelha","V"))