import re
import sys

sys.path.append(r'G:\project QA\前期版本\地点')

from places_ import get_most_similar_area_of_the_place

def judge_have_pattern(pattern_list, user_quesiton):
    for pa in pattern_list:
        pattern = re.compile(pa)
        if pattern.findall(user_quesiton):
            return True
    return False

def have_word_in_specify_list(word_list, str_temp):
    for word in word_list:
        if word in str_temp:
            return True
    return False

def add_str(match_list):
    add_str = ''
    try:
        for touple in match_list:
            add_str += ''.join(touple)
    except:
        return ''
    return add_str

didian_list = ['白堤路/风荷园','海光寺/六里台','王顶堤/华苑','体院北','南开/天大校区','西康路沿线','鞍山西道','鞍山道沿线','水上/天塔','天拖地区']
def analysis_didian(groove, answer):
    slot_occasion = [-3 for i in range(len(didian_list)+1)]#最后一个是随意槽，如果用户说随意就致1.
    # 小吃快餐：
    type_9 = ['动物园','鲁能城','气象台路','水上','水上公园','天塔','天塔湖','卫津南路','周邓纪念馆','紫金山路','远']
    # 面食粥点
    type_7 = ['鞍山西道','赛博','时代数码','学校北边','学校北门附近','学校北面','一附属','天大北']
    # 汉堡披萨：
    #hanbaopisa = ['汉堡', '披萨', '匹萨', '比萨', '炸鱼', '薯条', '炸鸡', '热狗', '鸡肉卷', '堡', '鸡腿', '鸡柳', '鸡翅', '鸡块', '蛋挞', '派']
    # hoguokaorou：
    type_4 = ['气象台路','天塔东边','肿瘤医院','体院','体育中心','紫金山路']
    # 小吃炸串：
    type_1 = ['白堤路','百脑汇','风荷园','学校附近','西门外','学校西北边','一中心']
    type_2 = ['海光寺站','六里台','南开二中','二马路','眼科医院','学校东北边','远']
    type_3 = ['华苑','师大那边','水西公园','红旗南路','迎水','王顶堤','学校西南边','师大','远']
    type_5 = ['八里台','二食','二食堂','复康路','七里台','三食','三食堂','四季村','天津图书馆','卫津路','西南村','学三','学三食堂','学四','学四食堂','学五','学五食堂','五食堂','校内','天大','南开']
    type_6 = ['气象台路','五大道','西康路','学校东门','医科大学','第一中学','远']
    type_8 = ['总医院','营口道','鞍山道沿线','远']
    type_10 = ['红旗路','天拖','天拖大楼','人民法院','一中心','远']

    choose_list = [type_1,type_2,type_3,type_4,type_5,type_6,type_7,type_8,type_9,type_10]
    #'([\u4e00-\u9fa5g^不没非拒否]{,8})'
    is_patterns = [ '(在|到|就|是|想吃|要|打算吃|来个|来份|来|吃)([\u4e00-\u9fa5g]{,4})','()([\u4e00-\u9fa5g]{,4})',
                   '([\u4e00-\u9fa5g]{,4})(吧|还行|还可以|不错|挺好|来一个)', '([\u4e00-\u9fa5g]{1,4})(的)([\u4e00-\u9fa5g]{,4})']

    not_patterns = ["([\u4e00-\u9fa5g]{,4})(不好|不要|不喜欢|拒绝|木|不|不想吃|别|别去|别在)([\u4e00-\u9fa5g]{1,4})(要|需求|打算|计划|准备|问题)",
                    '([\u4e00-\u9fa5g]{1,4})(腻了|吃过|够了|多了|太)',
                    '(不|没|无|拒绝|木|不想|受够了|讨厌|去掉|不要|拒绝)([\u4e00-\u9fa5g]{,4})']

    both_patterns = ["(差不多|无所谓|通用|都可以|都行|不挑|都想|随便|无所谓|都还行|随意|都阔以)",
                     "(都|全|两|俩)([\u4e00-\u9fa5g^不]{,6})(吃|要|可以|需要|不好|不干净|用|合适|适合|不用|不在|不是)"]

    office_home_both = ['(都|两者|两地|的地方|距离不是问题)']

    index_word1 = ['去','就','想','那','就行','那边','吧'] #就和那都是可前可后的 。感觉可以通过前后词的长度来判断


    special_patterns = ['(和|同|像)([\u4e00-\u9fa5g]{,4})(差不多|一样|类似)([\u4e00-\u9fa5g]{,2})(的)([\u4e00-\u9fa5g]{1,4})']
    #special = ['远','附近']
    for pattern in is_patterns:
        pattern = re.compile(pattern)
        #print(pattern)
        answer = str(answer)
        match = add_str(pattern.findall(answer))
        for i in choose_list:
            #print(i)
            '''
            if have_word_in_specify_list(i, match) and not judge_have_pattern(not_patterns, answer):
                print('-')
                slot_occasion[choose_list.index(i)] = 1#填入正值代表需要什么

            if judge_have_pattern(not_patterns, answer) and have_word_in_specify_list(i, answer):
                print('---')
                slot_occasion[choose_list.index(i)] = -1
            '''
            for pa in not_patterns:
                pa = re.compile(pa)
                match = add_str(pa.findall(answer))
                if have_word_in_specify_list(i, match):
                    slot_occasion[choose_list.index(i)] = -1

            for pa in is_patterns:
                pa = re.compile(pa)
                match = add_str(pa.findall(answer))
                if have_word_in_specify_list(i, match) and slot_occasion[choose_list.index(i)] != -1:
                    slot_occasion[choose_list.index(i)] = 1
                    pass
                pa = re.compile(pa)

        if judge_have_pattern(both_patterns, answer) and groove[3] == 2:
            slot_occasion[-1] = 1
    if slot_occasion == [ -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3] and groove[3] != 1 and groove[1] != []:
        slot_occasion = groove[1]

    print(slot_occasion)
    print(groove[1])
    print(slot_occasion == groove[1])
    print(groove[1] == [])
    '''
    if '近' in answer and (slot_occasion == groove[1] or groove[1] == []) and groove[3] == 1:
        for i in range(len(slot_occasion)):
            if i in [0,4,6,3]:
                slot_occasion[i] = 1
                '''
    print('slot_occasion:',slot_occasion)
    #*******************************************************************************************************************
    #尝试用模型判断：
    answer_copt = answer
    if  (slot_occasion == groove[1] or groove[1] == []) and groove[3] == 1 :
        print('in')
        '''
        for a in index_word1:
            answer_copt = answer_copt.replace(a)
        print(answer_copt)
        
        pinlei = get_most_similar_area_of_the_place(answer_copt)
        '''
        not_pinlei = []
        is_pinlei = []
        for pa in not_patterns:
            pa = re.compile(pa)
            #print(pa.findall(answer))
            if pa.findall(answer) != []:
                for i in range(len(pa.findall(answer))):
                    match = add_str(pa.findall(answer)[i])

                    pin = get_most_similar_area_of_the_place(match)
                    #print(pin)
                    if pin not in not_pinlei:
                        not_pinlei.append(pin)
        print('break')
        for pa in is_patterns:
            pa = re.compile(pa)
            #print(pa.findall(answer))
            if pa.findall(answer) != []:
                for i in range(len(pa.findall(answer))):
                    match = add_str(pa.findall(answer)[i])
                    pin = get_most_similar_area_of_the_place(match)
                    #print(pin)
                    if pin not in is_pinlei:
                        is_pinlei.append(pin)
        pinlei_all =[get_most_similar_area_of_the_place(answer)]
        print(pinlei_all)
        print(is_pinlei)
        is_pinlei+=pinlei_all

        if is_pinlei != ["",''] and is_pinlei != [''] and is_pinlei !=[]:
            for k in is_pinlei:
                if k !='':
                    slot_occasion[didian_list.index(k)] = 1
        if not_pinlei != [""] and not_pinlei != [] and not_pinlei !=['','']:
            for k in not_pinlei:
                if k !='':
                    slot_occasion[didian_list.index(k)] = -1
        #for pin in pinlei:
        #    slot_occasion[didian_list.index(pin)] = 1
        #******************************************************************************************************************
        #在针对性地处理不要，要的问题
    if ('近' in answer or '公里' in answer or '千米' in answer) and (slot_occasion == groove[1] or groove[1] == []) and groove[3] == 1:
        for i in range(len(slot_occasion)):
            if i in [0,4,6,3]:
                slot_occasion[i] = 1

    return slot_occasion






    n

if __name__ == '__main__':
    result = analysis_didian([[-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3] , [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3] ,  [[],[],[],[]],1,0,0],'八里台')
    print(get_most_similar_area_of_the_place('2公里以内'))
    print(result)