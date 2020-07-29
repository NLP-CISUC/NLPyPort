
class word_ranking:
    def __init__(self):
        self.wordMap = {}

    def load(self,input_file):
        rank = 0
        frequency = 0
        word = 0
        lineNumber = 0
        with open(input_file,"r",encoding = 'utf-8') as f:
            for line in f:
                line = line.strip()
                if(len(line)>0 and not (line[0]=="#")):
                    if("\t" in line and (line.find("\t")+1<len(line))):
                        word = line[line.find("\t")+1:].replace("="," ")
                        frequency = line[0:line.find("\t")]
                        rank += 1
                        new_entry = word_list_entry(word,frequency,rank)
                        #new_entry.print_word_list_entry()
                        self.wordMap[word] = new_entry
                    else:
                        break
        #print(self.get_frequency("-"))
        #print(self.retrieve_top_word(["minsitro","mielóide"]))
        #print(self.retrieve_top_word(["mielóide","minsitro"]))

    def get_frequency(self , word):
        if( word in self.wordMap):
            return self.wordMap[word].frequency
        else:
            return -1

    def get_rank(self , word):
        if(word in self.wordMap):
            return self.wordMap[word].rank
        else:
            return -1

    def rank(self,words,limit=0):

        ranked_list = []
        for word in words:
            if(not(self.get_rank(word)==-1)):
                new_entry = word_list_entry(word,self.get_frequency(word),self.get_rank(word))
                ranked_list.append(new_entry)
            else:
                new_entry = word_list_entry(word, 9999999999, 9999999999)
                ranked_list.append(new_entry)
        ranked_list.sort(key=lambda x: x.rank)
        if(limit==0):
            limit = len(ranked_list)
        ranked_words=[None]*len(ranked_list)
        ranked_list = ranked_list[0:limit+1]
        for index,elem in enumerate(ranked_list):
            ranked_words[index]=elem.word
        return ranked_words

        
    def retrieve_top_word(self,words):
        top_word = None
        if(len(words)>0):
            result =self.rank(words,1)
            if(len(result)>0):
                top_word=result[0]
            else:
                top_word = None
        return top_word
        
####################    
class word_list_entry:
    def __init__(self,word=None,frequency=0,rank=0):
        self.word = word
        self.frequency = frequency
        self.rank = rank

    def compare_to(self,other):
        if(self.frequency < other.frequency):
            return 1
        elif (self.frequency > other.frequency):
            return -1
        else:
            if(self.rank < other.rank):
                return -1
            elif (self.rank > other.rank):
                return 1
            else:
                return 0
        
    def print_word_list_entry(self):
        to_string = str(self.rank) + "\t" + str(self.frequency) + "\t" + str(self.word)
        print(to_string)
        return(to_string)

if __name__ == "__main__":
    novo_rank = word_ranking()
    novo_rank.load("acdc/lemas.total.txt")
