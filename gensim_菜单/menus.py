
from gensim_menus import TfidfModel
from gensim_menus import get_dic_from_excel_file
from gensim_menus import pre_process_question
import pandas as pd
DATA_ROOT=r'G:\project QA\前期版本\gensim_菜单'
excel_file = DATA_ROOT+'\\data\\menus.xlsx'
same_words_file =DATA_ROOT +'\\data\\same_words.xlsx'
stop_words = DATA_ROOT+'\\data\\stop_words.txt'
with open(stop_words, 'r', encoding="ISO-8859-1") as infile:
    stop_words = infile.readline().split('，')
    stop_words.sort(key=lambda x: len(x), reverse=True)
same_words_dic = get_dic_from_excel_file(same_words_file)
tfidf = TfidfModel(do_update=False, excel_file=excel_file, high_threshold_value=0.8, low_threshold_value=0.5,
                   same_words_dic=same_words_dic)
#todo
#add filter to get out sentences without key words
'''
while 1:
    query_=input()
    match,similarity=tfidf.query(query_)
    print('match:')
    print(match)
    print('similarity:')
    print(similarity)
    #print(pre_process_question(query_,same_words_dic))
'''
def get_most_similar_stores_of_the_menus(input_str):
    #comments=pd.read_excel(excel_file)
    match,store_name_str=tfidf.query(input_str)
    return store_name_str