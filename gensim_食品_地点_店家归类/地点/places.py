from gensim_地点 import TfidfModel
from gensim_地点 import get_dic_from_excel_file
from gensim_地点 import pre_process_question
DATA_ROOT=r'G:\project QA\前期版本\gensim_食品_地点_店家归类\地点'
excel_file = DATA_ROOT+'\\data\\places.xlsx'
same_words_file = DATA_ROOT+'\\data\\same_words.xlsx'
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

def get_most_similar_area_of_the_place(input_str):
    match,type_=tfidf.query(input_str)
    return type_