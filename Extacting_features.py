
import os
import glob
import re
import time
import spacy,pickle
import pandas as pd
from spacy_conll import Spacy2ConllParser
## READ ME
## this script need 5 to 25 min(depends on your laptop) because the CONLL file genarated contains over 4 million lines 
## it will genarate a conll file and a CSV one with features
## so you can either keep or remove (by uncommenting the 60th line) the conll file it's up to you 

nlp = spacy.load('fr_core_news_sm')


spacyconll = Spacy2ConllParser(nlp=nlp) 
start = time.time()


## Features extcated : (French Labguage)
## ROOT_dist_linked_words : the avrg distance between the ROOT and his linked words
##noun_presence : how many nouns devided by the number of words 
##simple_tense  : percentage of simple tenses 
##com_tense  : percentage of non-simple tenses 
##word_freq  

def Normlized_to_Conll(file,file_conll):
    # IN normilized file , name_of_conllfile
    #OUT conll_file

    with open(file, 'r',encoding="utf-8") as file:
        k = file.read()
    str_="".join([parsed_sent+"\n" for parsed_sent in spacyconll.parse(input_str=k,include_headers=True,is_tokenized=True)])
    with open (file_conll, "a", encoding="utf-8") as conll_file:
        conll_file.write("first\tsecond\tthird\tfourth\tfifth\tsixth\tseventh\teithth\tnineth\ttenth\n"+str_)



def extracting_features_from_conll(file_conll,out_file_ftr,_type_):
    # IN file_conll, name_of_file_with_extracted_features, classe_to_add_to_file
    #OUT CSV_with_feature_and_a_class

    try:
        os.mkdir("E:\\Project_OOP\\1_Data\\files_ft")
    except:
        pass 
    df = pd.read_csv(file_conll, sep="\t",encoding='utf-8')

    dfObj = pd.DataFrame(df, columns = ["first","fourth","fifth","seventh" ])  ## first column contains the words index, the 4th one contains the tag 

    dfObj.to_csv("data_conll_Off_Corpus.csv",sep="\t", encoding="utf-8",index=False,header=None) ## csv file with only words Indices and tags 


    feature="0.0"
    text_skiped=0
    text_ignored_small_len=0
    with open('E:\\Project_OOP\\data_conll_Off_Corpus.csv', 'r', encoding='utf-8') as f:
        txt=f.read()
    os.remove("data_conll_Off_Corpus.csv")
    # os.remove(file_conll) # you can remove or keep the conll file 
    list_txt=txt.split("# text =")
    os.chdir("E:\\Project_OOP\\1_Data\\files_ft")
    with open(out_file_ftr, 'a', encoding='utf-8') as fw:
        fw.write("Text,ROOT_dist_linked_words,noun_presence,simple_tense,com_tense,word_freq,text_type\n")  
        for sent in list_txt:
            valeur=0
            avrage_dis_root_from_words=0
            try:
                if len(sent)>15:
                    sentence=re.findall(r"\s(.+)\t+\n1",sent)             
                    if len(sentence[0].split())>2 :
                        n_words=len(sentence[0].split())
                        lis_index_root=re.findall(r"\n(\d+)\t.+\t0.0\n",sent)
                        list_f_vrb=re.findall(r"\tNOUN\t",sent)
                        pourcentage=round(len(list_f_vrb)/n_words,2)
                        words_linked_root=re.findall(r"\n(\d+)\t.+\t"+re.escape(lis_index_root[0]+".0")+r"\n+",sent)
                        list_v_simp=re.findall(r"\tVERB\t.+(VerbForm=Fin)",sent)
                        list_v_comp=re.findall(r"\tVERB\t.+(VerbForm=Part)",sent)
                        simp_score=round(len(list_v_simp)/n_words,2)
                        comp_score=round(len(list_v_comp)/n_words,2)
                        for e in words_linked_root:
                           valeur+=abs(int(lis_index_root[0])-int(e))
                        avrage_dis_root_from_words=round(valeur/len(words_linked_root)/n_words,2)
                
                        fw.write(sentence[0]+","+str(avrage_dis_root_from_words)+","+str(pourcentage)+","+str(simp_score) +"," + str(comp_score)+ ","+str(n_words)+","+_type_+"\n")
                    else:
                
                        text_ignored_small_len+=1
            except Exception as e:
                # print(e)
                text_skiped+=1
    os.chdir("E:\\Project_OOP\\")
        # print(text_skiped,text_ignored_small_len)





def merge(dir_,out):
    # Direcory_where the csv files are
    # name of the csv with merged files
    # "\\1_Data\\files_ft"
    os.chdir(dir_)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    combined_csv.to_csv( out, index=False, encoding='utf-8-sig')



end = time.time()
print("Processing time  in minutes : ",(end - start)/60)
 