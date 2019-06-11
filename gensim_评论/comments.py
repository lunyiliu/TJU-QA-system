
from gensim_comments import TfidfModel
from gensim_comments import get_dic_from_excel_file
from gensim_comments import pre_process_question
import pandas as pd
DATA_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_评论'
excel_file = DATA_ROOT+'\\data\\comments.xlsx'
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
def get_most_similar_comments_of_the_keyword(input_str):
    match,dish_str=tfidf.query(input_str)
    return match
def get_most_similar_stores_of_the_keyword(input_str):
    comments=pd.read_excel(excel_file)
    dish_strs=list(comments['详细菜品'])
    stores=list(comments['店名'])
    match,dish_str=tfidf.query(input_str)
    return stores[dish_strs.index(dish_str)]