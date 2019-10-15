import os
import re
import time
import pandas as pd
import spacy
import pickle

nlp = spacy.load('fr_core_news_sm', disable=["ner","parser"])
nlp.max_length=2000000





### READ ME ###
"""
The csv file result.csv countains data from web and from the 1_data folder (folder that contains non normlized data),
it's a csv with comma (,) as a separator 

we choose to normlize data using two processing :
- Part_1 : keep only an uppercase letter if it's a PROPN, we choose to do this part first before spliting text and having a lot of sentences 
- Part_2 : Addind space after and before each punct and split the text, one sent by line, we choose that a sent ends with "?" or "!" or "." 



The process explained : 
______________________________________________________________
csv_to_dic(the_two_csv_merged) ---> OUTPUT : X = dictionary 
normlizing_part_1(X) ----->  OUTPUT : Y = dictionary with semi-normlized data 
dic_to_csv(Y,"name_of_the_genrated_csv") -----> OUTPUT :   Z= csv file with semi-normlized data 
making the 3_normlized_data directory 
csv_to_dic_2(Z)---> OUTPUT : Q = dictionary    # we didn't use the  csv_to_dic besause we don't need to generate ID for keys the each key is unique with an ID 
normlizing_part_2(Q) ----> OUTPUT   W = dictionary with the final normlized data ##we need to make text as key and author/path 
as a value because the author/path is not unique although the texts are unique 
dic_to_csv_2(W) ----> OUTPUT R = CSV with normlized data inside the 3_normlized_data directory  ## we didn't use dic_to_csv because we need to change 
the csv format from [key=text , value=author/path] to [value=author/path , key=text] 



"""



def csv_to_dic(csv_file_name):
   #IN :    csv file       #
   # OUT: dic{ Author/ path: text }  #
   # csv file contains two columns  Author or path and the text separated with a comma        #
   #  we needed to add the the author ID so we'll have a single dic.key, the ID = length of the text in the dic.value #
    with open(csv_file_name, 'r', encoding='utf-8') as f:
        dic={}
        c=0
        for line in f :
            
            if  line != "\n":
    
                part_1=line.split(",")
    
                dic[part_1[0]+"_id="+str(len(part_1[1]))]=part_1[1]
                part_1=[]

    return dic


def csv_to_dic_2(file_name):
	# Same as the first one we just skip adding ID part because we alreday did it#
    with open(file_name, 'r', encoding='utf-8') as f:
        dic={}
        for line in f :  
            part=line.split(",")
            dic[part[0]]=part[1]
            part=[]
    return dic




def normlizing_part_1(dic):
	## IN dic  
	## OUT dic with normlized data 
    new_dic={}
    for k,v in dic.items():
        doc=nlp(v)
        for tok in doc:
            if str(tok).isalpha() and not str(tok).islower() and tok.pos_!="PROPN": ## <--(1) 
            ## (1): ## only the words than cantains uppercase letter and this word is not a PROPN so we skip other cases
                n=str(tok)
                m=n.lower()
                v=v.replace(n,m)
        new_dic[k]=v
    return new_dic

def normlizing_part_2(dic):
    ## IN dic  
	## OUT dic with normlized data 
    new_dic={}
    new_vv=[]
    for k,v in dic.items():
        v=v.replace(":", " : ")
        v=v.replace(";", " ; ")
        v=v.replace(".", " .\n")
        v=v.replace("!", " !\n")
        v=v.replace("?", " ?\n")
        new_v=re.findall(r".*\n", v)
        for i in new_v:
            new_dic[i]=k
    with open('normlized_data.pickle', 'wb') as handle:
        pickle.dump(new_dic, handle, protocol=pickle.HIGHEST_PROTOCOL)   
    return new_dic


def dic_to_csv(dic,file_name):
	## IN  dic and the name of the genarted csv
	## OUT csv file with a comma as sep
    with open(file_name,"a",encoding="utf-8") as fw:
        for k,v in dic.items():
            fw.write(k+","+v)

def dic_to_csv_2(dic,file_name):
	## IN  dic and the name of the genarted csv
	## OUT csv file with a comma as sep
	## we start with dic value because it's the author/path and after that the key which is the text
    with open(file_name,"a",encoding="utf-8") as fw:
        for k,v in dic.items():
            if len(k)>15:
               fw.write(k)


def main(file1,file2):
## explained in the top of the script 
    df_1 = pd.read_csv("Your_CSV_file", sep=",",encoding='utf-8')  ## data from our folder 1_data_
    df_2 = pd.read_csv("Your_second_CSV_file", sep=",",encoding='utf-8') ## Web scraped DATA 
    out = df_1.append(df_2)
    with open('E:\\Project_OOP\\result_essai.csv', 'w', encoding='utf-8') as f:
        out.to_csv(f, index=False)
    start = time.time()
    dic_to_csv(normlizing_part_1(csv_to_dic(file1)),"data_norm_part_1.csv")

    end = time.time()
    print("1st Processing in minutes :",(end - start)/60)
    start = time.time()
    try:
        os.mkdir("E:\\Project_OOP\\1_Data\\3_normlized_data")
    except:
        pass 
    dic_to_csv_2(normlizing_part_2(csv_to_dic_2("data_norm_part_1.csv")),file2)
    os.remove("data_norm_part_1.csv")
    end = time.time()
    print("2nd Processing  in minutes : ",(end - start)/60)










if __name__ == '__main__':
    start = time.time()
    
    main(file1,file2)


    end = time.time()
    print("total time spent in processing in minutes : ",(end - start)/60)