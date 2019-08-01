import os
import random
import re

import pandas as pd
from gensim import corpora, similarities, models

import tuling
DATA_ROOT=r'G:\project QA\前期版本\gensim_食品_地点_店家归类\地点'
stop_words = DATA_ROOT+'\\data\\stop_words.txt'
with open(stop_words, 'r', encoding="ISO-8859-1") as infile:
    stop_words = infile.readline().split('，')
    stop_words.sort(key=lambda x: len(x), reverse=True)
def unique_list(list_):
    assert isinstance(list_, list)
    if list_ != []:
        return list(set(list_))
    return []


def have_word_in_specify_list(word_list, str_temp):
    for word in word_list:
        if word in str_temp:
            return True
    return False


def judge_have_pattern(pattern_list, user_quesiton):
    for pa in pattern_list:
        pattern = re.compile(pa)
        if pattern.findall(user_quesiton):
            return True
    return False


def pre_process_question(user_question, same_words_dic):
    user_question = same_word(same_words_dic, user_question)
    for word in stop_words:
        if word in user_question:
            user_question = user_question.replace(word, '')
    user_question = user_question.lower()
    user_question = user_question.replace('，', ',')
    user_question = user_question.replace('？', '?')
    user_question = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\d\-*,?]', "", user_question)
    # normalize the question
    #user_question, version_words, type_words = normalize_entity(version_dic, type_dic, user_question)

    return user_question


def pre_process_question_(user_question):
    for word in stop_words:
        if word in user_question:
            user_question = user_question.replace(word, '')
    user_question = user_question.lower()
    user_question = user_question.replace('，', ',')
    user_question = user_question.replace('？', '?')
    user_question = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\d\-*,?]', "", user_question)
    # normalize the question
    # user_question, version_words, type_words = normalize_entity(version_dic, type_dic, user_question)

    return user_question


def pre_process_question_1(user_question, version_dic, type_dic, same_words_dic):
    user_question = same_word(same_words_dic, user_question)
    for word in stop_words:
        if word in user_question:
            user_question = user_question.replace(word, '')
    user_question = user_question.lower()
    user_question = user_question.replace('，', ',')
    user_question = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\d\-*,?]', "", user_question)
    #user_question = user_question.replace('xx', '')
    #user_question = user_question.replace('yy', '')
    # normalize the question
    #user_question = normalize_entity_1(version_dic, type_dic, user_question)

    return user_question


def get_products(user_question, version_dic, type_dic, version_type_file):
    user_question, version_words, type_words = normalize_entity(version_dic, type_dic, user_question)
    products = get_product(user_question, version_type_file, version_words, type_words)
    return products


def normalize_entity(version_dic, type_dic, user_question):
    version_words = []
    type_words = []
    versions = list(version_dic.keys())
    versions.sort(key=lambda x: len(x), reverse=True)
    types = list(type_dic.keys())
    types.sort(key=lambda x: len(x), reverse=True)
    for version_word in versions:
        if ',' not in version_word and version_word in user_question:
            user_question = user_question.replace(version_word, version_dic[version_word])
            version_words.append(version_dic[version_word])
        elif ',' in version_word and have_list_in_sen(user_question, version_word.split(',')):
            user_question = remove_list_in_sen(user_question, version_word.split(','))
            user_question = user_question + version_dic[version_word]
            version_words.append(version_dic[version_word])
    for type_word in types:
        if ',' not in type_word and type_word in user_question:
            user_question = user_question.replace(type_word, type_dic[type_word])
            type_words.append(type_dic[type_word])
        elif ',' in type_word and have_list_in_sen(user_question, type_word.split(',')):
            user_question = remove_list_in_sen(user_question, type_word.split(','))
            user_question = user_question + type_dic[type_word]
            type_words.append(type_dic[type_word])
    svw = ['Air Touch', 'Aqua Touch', 'H950V', 'FC400新风系统电子式', 'H46C1166', 'h8908', 'MCV3000', 'MCV2000', 'MT4 小型直行程',
           'T6818DP200', 'TH228WPN数字式', 'HUM系列户用超声波式', 'HM系列地板辐射采暖用', 'O3彩色数字', 'o1数字', 'T6861系列数字', 'T6800系列数字',
           'T6820A2001数字', 'T6861-F系列数字', 'T6865', 'T6373', 'T4360/T6360', '霍尼韦尔境尚', '家装管', '银离子抗菌', '增强型银离子抗菌', '不锈钢',
           '紫铜', 'PE-RT', '阻氧型PE-RT', 'PE-Xb', '阻氧型PE-Rb', 'PB', '采暖用', 'PE经典', 'PE抗菌', 'PVC-U透明']
    stw = ['空气净化机', '水净', '萌宠口罩', '空气净化机', '湿度控制器', '湿度控制器', '执行器', '执行器', '热电执行器', '温控器', '温控器', '热量表', '分集水器', '温控器',
           '温控器', '温控器', '温控器', '温控器', '温控器', '温控器', '温控器', '温控器', '开关插座', 'PP-R管', 'PP-R管', 'PP-R管', '给水管', '给水管',
           '采暖管', '采暖管', '采暖管', '采暖管', '采暖管', '分集水器', '新风管', '新风管', '电工套管']
    assert len(svw) == len(stw)
    for i in range(len(svw)):
        if svw[i] in version_words and stw[i] not in type_words:
            type_words.append(stw[i])
            user_question = user_question + stw[i]
    return user_question, unique_list(version_words), unique_list(type_words)


def normalize_entity_1(version_dic, type_dic, user_question):
    versions = list(version_dic.keys())
    versions.sort(key=lambda x: len(x), reverse=True)
    types = list(type_dic.keys())
    types.sort(key=lambda x: len(x), reverse=True)
    for version_word in versions:
        if ',' not in version_word and version_word in user_question:
            user_question = user_question.replace(version_word, '')
        elif ',' in version_word and have_list_in_sen(user_question, version_word.split(',')):
            user_question = remove_list_in_sen(user_question, version_word.split(','))
    for type_word in types:
        if ',' not in type_word and type_word in user_question:
            user_question = user_question.replace(type_word, '')
        elif ',' in type_word and have_list_in_sen(user_question, type_word.split(',')):
            user_question = remove_list_in_sen(user_question, type_word.split(','))
    return user_question


def have_list_in_sen(user_question, list_):
    for word in list_:
        if word not in user_question:
            return False
    return True


def remove_list_in_sen(user_question, list_):
    for word in list_:
        user_question = user_question.replace(word, '')
    return user_question


def extract_word_in_specify_list(word_list, str_temp):
    words_own_list = []
    for word in word_list:
        if word in str_temp:
            words_own_list.append(word)
    return list(set(words_own_list))


def get_product(user_question, file_path, version_words, type_words):
    products = []
    root_dir, file = os.path.split(file_path)
    if "xlsx" in file or "xls" in file:
        data_frame = pd.read_excel(file_path)
    if "csv" in file:
        data_frame = pd.read_csv(file_path)
    type_words = [pre_process_question_(word) for word in type_words]
    version_words = [pre_process_question_(word) for word in version_words]
    print('version:', version_words)
    print('type:', type_words)
    for i in range(len(data_frame)):
        line = data_frame.iloc[i]
        tw = pre_process_question_(line[1])
        vw = pre_process_question_(line[2])
        if tw in type_words and vw in version_words:
            products.append(line[0])
        if tw in type_words and vw == '*':
            products.append(line[0])
    return products


def prepare_corpus_for_sen(user_question):
    # with open('data/stop_words.txt', 'r', encoding='utf-8') as infile:
    #     stop_words_list = infile.read().split('\n')
    # pro_word_in_sen = [word for word in jieba.lcut(user_question) \
    #                    if word in stop_words_list]
    # for word in pro_word_in_sen:
    #     user_question = user_question.replace(word, '')
    # if with_word:
    #     return [ch for ch in user_question] +
    return [ch for ch in user_question]


def read_file(file_path):
    que2id = {}
    id2type = {}
    if os.path.isfile(file_path):
        root_dir, file = os.path.split(file_path)
        try:
            if "xlsx" in file or "xls" in file:
                data_frame = pd.read_excel(file_path)
            if "csv" in file:
                data_frame = pd.read_csv(file_path)
        except (ValueError, TypeError):
            print("Please check file type")
        for index in range(len(data_frame)):
            que = pre_process_question_(data_frame.iloc[index][0])
            Type = data_frame.iloc[index][1]
            que2id.update({que: index})
            id2type.update({index: Type})
    return que2id, id2type


def read_first_column(file_path):
    if os.path.isfile(file_path):
        root_dir, file = os.path.split(file_path)
        try:
            if "xlsx" in file or "xls" in file:
                data_frame = pd.read_excel(file_path)
            if "csv" in file:
                data_frame = pd.read_csv(file_path)
        except:
            return None
    return data_frame.ix[:, 0]


class TfidfModel():

    def __init__(self, do_update, excel_file, high_threshold_value, low_threshold_value, same_words_dic):
        assert high_threshold_value > low_threshold_value
        self.high_threshold_value = high_threshold_value
        self.low_threshold_value = low_threshold_value
        self.que2id, self.id2type = read_file(excel_file)
        self.same_words_dic = same_words_dic

        self.tfidf_corpus, self.corid2que = self.prepare_corpus_from_excel()
        if do_update:
            self.update()
        self.dictionary, self.tfidf_model, self.precessed_corpus, self.similarities_tfidf = self.load()

    def prepare_corpus_from_excel(self):
        all_que = [que for que in self.que2id.keys()]
        corpus = []
        cor_id = 0
        corid2que = {}
        for que in all_que:
            que_ori = que
            que = pre_process_question(que, self.same_words_dic)
            if que != '':
                corpus.append(prepare_corpus_for_sen(que))
                corid2que.update({cor_id: que_ori})
                cor_id += 1
        return corpus, corid2que

    def update(self):
        dictionary = corpora.Dictionary(self.tfidf_corpus)
        dictionary.save('tfidf-model-letter-words/deerwester.dict')
        processed_corpus = [dictionary.doc2bow(end_que) for end_que \
                            in self.tfidf_corpus]
        tfidf_model = models.TfidfModel(processed_corpus)
        corpora.MmCorpus.serialize('tfidf-model-letter-words/corpus.mm', processed_corpus)
        tfidf_model.save('tfidf-model-letter-words/mytfidfmodel.model')
        bow_tfidf = tfidf_model[processed_corpus]
        similarity_tfidf = similarities.Similarity \
            ('tfidf-model-letter-words/Similarity-tfidf.index', bow_tfidf, num_features=9999)
        similarity_tfidf.save('tfidf-model-letter-words/Similarity-tfidf.index')

    def load(self):
        print('--------load tfidf-------------')
        print('load dictionnary')
        dictionary = corpora.Dictionary.load \
            (DATA_ROOT+'\\tfidf-model-letter-words\\deerwester.dict')
        print('load tfidf_model')
        tfidf_model = models.TfidfModel.load \
            (DATA_ROOT+'\\tfidf-model-letter-words\\mytfidfmodel.model')
        print('load corpus')
        precessed_corpus = corpora.MmCorpus(DATA_ROOT+'\\tfidf-model-letter-words\\corpus.mm')
        print('load Similarity')
        similarities_tfidf = similarities.Similarity.load \
            (DATA_ROOT+'\\tfidf-model-letter-words\\Similarity-tfidf.index')
        similarities_tfidf.output_prefix=DATA_ROOT+'\\tfidf-model-letter-words\\'
        print('load done')
        return dictionary, tfidf_model, precessed_corpus, similarities_tfidf

    def query(self, user_question):
        user_question_str = pre_process_question(user_question, self.same_words_dic)
        user_cor = prepare_corpus_for_sen(user_question_str)
        print('user_cor:', user_question_str)
        user_question = self.dictionary.doc2bow(user_cor)
        self.similarities_tfidf.num_best = 5
        similarest_que_index = self.tfidf_model[user_question]
        cor_id = self.similarities_tfidf[similarest_que_index]
        match_que = [self.corid2que[cor_id_element[0]] for cor_id_element in cor_id]
        match_similarity = [cor_id_element[1] for cor_id_element in cor_id]
        #high_confidence = self.similarities_tfidf[similarest_que_index][0][1]
        #print('confidence_2:', high_confidence)
        type_ = self.id2type[self.que2id[match_que[0]]]
        return match_que[0],type_
        # TODO: add filters and expand logic
        # match_que = pre_process_question(match_que, self.version_dic, self.type_dic)
        # products_ = get_products(match_que, self.version_dic, self.type_dic, self.version_type_file)
        user_question_str = pre_process_question_(user_question_str)
        products = get_products(user_question_str, self.version_dic, self.type_dic, self.version_type_file)
        print('user_products:', products)
        # print('match_products:', products_)
        print('match_que:', match_que)
        # if high_confidence >= self.high_threshold_value and products == products_:
        if high_confidence >= self.high_threshold_value:
            return ans
        elif high_confidence < self.low_threshold_value:
            return tuling.get_response(user_question_str)[1]
            # soft_answers = ["很抱歉，这个问题我暂时回答不了。我会努力学习、天天成长的！",
            #                 "非常抱歉，我暂时回答不了这个问题，您换个问法试试看？",
            #                 "实在是很抱歉，没有帮助到您，我会努力的！"]
            # return soft_answers[random.randint(0, 2)]
        else:
            cor_ids = [self.similarities_tfidf[similarest_que_index][i][0] for i in
                       range(len(self.similarities_tfidf[similarest_que_index]))]
            return [self.corid2que[cor_id] for cor_id in cor_ids]


class TfidfModel_template():

    def __init__(self, do_update, excel_file, threshold_value, version_dic, type_dic,
                 version_type_file, ans_file, high_threshold_value, add_corpus, same_words_dic):
        self.add_corpus = add_corpus
        self.threshold_value = threshold_value
        self.version_dic = version_dic
        self.type_dic = type_dic
        self.excel_file = excel_file
        self.version_type_file = version_type_file
        self.ans_file = ans_file
        self.same_words_dic = same_words_dic
        self.high_threshold_value = high_threshold_value
        self.tfidf_corpus, self.corid2quetype, self.corpus_all, self.cor_id2que, self.que2quetype = self.prepare_corpus_from_excel()
        if do_update:
            self.update()
        self.dictionary, self.tfidf_model, self.precessed_corpus, self.similarities_tfidf = self.load()

    def prepare_corpus_from_excel(self):
        corpus = []
        cor_id = 0
        corid2quetype = {}
        cor_id2que = {}
        que2quetype = {}

        root_dir, file = os.path.split(self.excel_file)
        try:
            if "xlsx" in file or "xls" in file:
                data_frame = pd.read_excel(self.excel_file)
            if "csv" in file:
                data_frame = pd.read_csv(self.excel_file)
        except (ValueError, TypeError):
            print("Please check file type")
        all_que = data_frame['问题内容']
        all_que_type = data_frame['问题类型']
        for que_index in range(len(all_que)):
            que = all_que[que_index]
            que_type = all_que_type[que_index]
            que = pre_process_question_1(que, self.version_dic, self.type_dic, self.same_words_dic)
            if que != '':
                corpus.append(prepare_corpus_for_sen(que))
                corid2quetype.update({cor_id: que_type})
                cor_id2que.update({cor_id: all_que[que_index]})
                que2quetype.update({all_que[que_index]: que_type})
                cor_id += 1
        corpus_all = corpus + self.add_corpus
        return corpus, corid2quetype, corpus_all, cor_id2que, que2quetype

    # save

    def update(self):
        dictionary = corpora.Dictionary(self.corpus_all)
        dictionary.save('tfidf-model-letter-words_1/deerwester.dict')
        processed_corpus_all = [dictionary.doc2bow(end_que) for end_que \
                                in self.corpus_all]
        processed_corpus = [dictionary.doc2bow(end_que) for end_que \
                            in self.tfidf_corpus]
        tfidf_model = models.TfidfModel(processed_corpus_all)
        corpora.MmCorpus.serialize('tfidf-model-letter-words_1/corpus.mm', processed_corpus_all)
        tfidf_model.save('tfidf-model-letter-words_1/mytfidfmodel.model')
        bow_tfidf = tfidf_model[processed_corpus]
        similarity_tfidf = similarities.Similarity \
            ('tfidf-model-letter-words_1/Similarity-tfidf.index', bow_tfidf, num_features=9999)
        similarity_tfidf.save('tfidf-model-letter-words_1/Similarity-tfidf.index')

    def load(self):
        print('--------load tfidf-------------')
        print('load dictionnary')
        dictionary = corpora.Dictionary.load \
            ('tfidf-model-letter-words_1/deerwester.dict')
        print('load tfidf_model')
        tfidf_model = models.TfidfModel.load \
            ('tfidf-model-letter-words_1/mytfidfmodel.model')
        print('load corpus')
        precessed_corpus = corpora.MmCorpus('tfidf-model-letter-words_1/corpus.mm')
        print('load Similarity')
        similarities_tfidf = similarities.Similarity.load \
            ('tfidf-model-letter-words_1/Similarity-tfidf.index')
        print('load done')
        return dictionary, tfidf_model, precessed_corpus, similarities_tfidf

    def query(self, user_question):
        _, version_words, type_words = normalize_entity(self.version_dic, self.type_dic, user_question)
        user_question_ori = pre_process_question_(user_question)

        have_pattern = ['(有没有|卖不卖|买不买|是否有|有卖)', '(可以|能)[\u4e00-\u9fa5a-z\d]{,5}买到',
                        '(需要|想要|想买)[\u4e00-\u9fa5a-z\d]{2,5}']
        price_pattern = ['(价格|多少钱|价位|折扣|批发价|怎么卖|价钱|优惠|活动|打折|促销)']
        person_words = ['人', '喘气', '活的', '折扣', '优惠', '活动', '促销', '打折']

        # judge is-have type
        if judge_have_pattern(pattern_list=have_pattern,
                              user_quesiton=user_question_ori) and not have_word_in_specify_list(person_words,
                                                                                                 user_question_ori):
            if len(version_words) == 0 and len(type_words) == 0:
                print(have_word_in_specify_list(person_words, user_question_ori))
                soft_answers = ["很抱歉，还没有您想要的产品，请期待我们的好消息",
                                "没有相关产品，您可以看看其他产品",
                                "没有为您找到相关产品的信息，您再看看其他产品"]
                return soft_answers[random.randint(0, 2)]

        if judge_have_pattern(pattern_list=price_pattern, user_quesiton=user_question_ori):
            soft_answers = ["关乎钱的事情比较重要，您还是问问人工客服吧",
                            "很抱歉，这种事情没有办法帮助到您，您可以咨询人工",
                            "价格的事情，您还是问问人工吧"]
            return soft_answers[random.randint(0, 2)]
        user_question_str = pre_process_question_1(user_question, self.version_dic, self.type_dic, self.same_words_dic)
        if user_question_str != '':
            print('1,que', user_question_str)
            user_cor = prepare_corpus_for_sen(user_question_str)
            user_question = self.dictionary.doc2bow(user_cor)
            similarest_que_index = self.tfidf_model[user_question]
            print('similarest_que_index:', similarest_que_index)
            self.similarities_tfidf.num_best = 1
            print('sim_tfidf:', list(self.similarities_tfidf))
            cor_id = self.similarities_tfidf[similarest_que_index][0][0]
            que = self.cor_id2que[cor_id]
            print('match_1 que:', que)
            que_type = self.que2quetype[que]
            print(que_type)
            high_confidence = self.similarities_tfidf[similarest_que_index][0][1]
            print('confidence_template:', high_confidence)
            if high_confidence > self.threshold_value:
                return self.get_answer(que_type, user_question_ori, self.version_dic, self.type_dic, high_confidence)
        elif user_question_str == '' and len(type_words) > 0:
            return self.get_answer('Temp2', user_question_ori, self.version_dic, self.type_dic, 0.1)
        else:
            return None

    def get_answer(self, que_type, user_question, version_dic, type_dic, high_confidence):
        data_frame = pd.read_excel(self.ans_file)
        user_question = pre_process_question_(user_question)
        user_question, version_words, type_words = normalize_entity(version_dic, type_dic, user_question)
        products = get_product(user_question, version_type_file, version_words, type_words)
        if '_1' in que_type and len(version_words) == 0:
            que_type = que_type[:5]
            print('turn que_type:', que_type)
        if len(que_type) == 5 and len(version_words) > 0 and len(type_words) > 0:
            que_type = que_type + '_1'
            print('turn que_type:', que_type)
        if len(version_words) > 0 and len(type_words) > 0:
            version_word = version_words[0]
            type_word = type_words[0]
            guide = pre_process_question_(type_word) + '+' + pre_process_question_(version_word)
            print("guide:", guide)
            return self.extract_ans(data_frame, guide, que_type, high_confidence)
        elif len(type_words) > 0 and len(version_words) == 0:
            type_word = type_words[0]
            guide = pre_process_question_(type_word) + '+null'
            print("guide:", guide)
            return self.extract_ans(data_frame, guide, que_type, high_confidence)
        else:
            print("guide:None")
            return self.extract_ans(data_frame, '', que_type, high_confidence)

    def extract_ans(self, df, guide, que_type, high_confidence):
        que_type = pre_process_question_(que_type)
        for i in range(len(df)):
            if pre_process_question_(guide) == pre_process_question_(
                    str(df.iloc[i][2])) and que_type == pre_process_question_(df.iloc[i][1]):
                print('id:', df.iloc[i][0])
                return df.iloc[i][3]
        if self.high_threshold_value < high_confidence:
            que_type = que_type[:5]
            ans_dic = {'temp1': '没有为您找到您想要的', 'temp2': '详细的产品介绍，您可以咨询人工的哦', 'temp3': '您可以向客服咨询有没有想要的产品哦',
                       'temp4': '具体的产品功能和设计特色，您可以查看相关页面的', 'temp5': '对于产品使用的限制，您可以咨询下人工客服的'}
            return ans_dic[que_type]
        return None


def list2file(list_, file):
    df = pd.DataFrame(list_)
    df.to_excel(file)


def get_dic_from_excel_file(file_path):
    root_dir, file = os.path.split(file_path)
    if "xlsx" in file or "xls" in file:
        data_frame = pd.read_excel(file_path)
    if "csv" in file:
        data_frame = pd.read_csv(file_path)
    dict_temp = {}
    for index in range(len(data_frame)):
        line = data_frame.iloc[index]
        for i in range(len(line)):
            if len(str(data_frame.iloc[index][i])) >= 2:
                dict_temp.update(
                    {pre_process_question_(str(data_frame.iloc[index][i])): str(data_frame.iloc[index][0])})
    return dict_temp


def query(user_question):
    user_question_ = user_question
    try:
        if len(user_question_) <= 3:
            return turn_result(tuling.get_response(user_question_)[1], user_question_)
        if tfidf_1.query(user_question):
            return turn_result(tfidf_1.query(user_question), user_question)
        else:
            return turn_result(tfidf.query(user_question_), user_question)
    except:
        soft_answers = ["很抱歉，这个问题我暂时回答不了。我会努力学习、天天成长的！",
                        "非常抱歉，我暂时回答不了这个问题，您换个问法试试看？",
                        "实在是很抱歉，没有帮助到您，我会努力的！"]
        return turn_result(soft_answers[random.randint(0, 2)], user_question)


def turn_result(result_ori, user_question):
    if isinstance(result_ori, str):
        return [{'describe': user_question, 'answer': result_ori}]
    else:
        assert isinstance(result_ori, list)
        result = []
        for que in result_ori:
            result.append({'describe': que, 'answer': tfidf.query(que)})
        return result


def same_word(same_words_dic, user_question):
    versions = list(same_words_dic.keys())
    versions.sort(key=lambda x: len(x), reverse=True)
    for version_word in versions:
        if version_word in user_question:
            user_question = user_question.replace(version_word, same_words_dic[version_word])
    return user_question

'''
excel_file = 'data/task_2.xlsx'
version_file = 'data/model.xlsx'
type_file = 'data/category.xlsx'
version_type_file = 'data/model+type.xlsx'
ans_file = 'data/template_ans_2.xlsx'
excel_1_file = 'data/questiontemp_new_2.xlsx'
same_words_file = 'data/same_words.xlsx'
stop_words = 'data/stop_words.txt'
with open(stop_words, 'r', encoding="ISO-8859-1") as infile:
    stop_words = infile.readline().split('，')
    stop_words.sort(key=lambda x: len(x), reverse=True)
version_dic = get_dic_from_excel_file(version_file)
type_dic = get_dic_from_excel_file(type_file)
same_words_dic = get_dic_from_excel_file(same_words_file)
tfidf = TfidfModel(do_update=True, excel_file=excel_file, high_threshold_value=0.8, low_threshold_value=0.5,
                   version_dic=version_dic, type_dic=type_dic, version_type_file=version_type_file,
                   same_words_dic=same_words_dic)
tfidf_1 = TfidfModel_template(do_update=True, excel_file=excel_1_file, threshold_value=0.5, version_dic=version_dic,
                              type_dic=type_dic, version_type_file=version_type_file, ans_file=ans_file,
                              high_threshold_value=0.80, add_corpus=tfidf.tfidf_corpus, same_words_dic=same_words_dic)
while 1:
    query_=input()
    reply=query(query_)
    print(reply)
'''