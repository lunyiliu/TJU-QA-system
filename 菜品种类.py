import re
import sys
sys.path.append(r'G:\project QA\前期版本\识别正向、负向食物')
sys.path.append(r'G:\project QA\前期版本\食品')
print(sys.path)

from exmenu_ import food_taste_extract

from dishes_ import get_most_similar_categ_of_the_dish

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

fenlei_list = ['自助餐','其他','甜点饮品','火锅烤肉','日韩料理','西餐','面食粥点','地方菜系','小吃快餐','家常菜','汉堡披萨']
def analysis_type(groove, answer):
    slot_occasion = [-3 for i in range(len(fenlei_list)+1)]#最后一个是随意槽，如果用户说随意就致1.
    # 小吃快餐：
    type_9 = [fenlei_list[8],'饭', '炒饭', '蛋包饭', '米饭', '便当', '拌饭', '捞饭','小吃','快餐','炒菜','小炒','小食','便携','手上']
    # 面食粥点
    type_7 = [fenlei_list[6],'粥', '粥铺', '粥店', '米线', '沙县小吃', '包子', '锅贴', '煎饼', '馅饼', '粉']
    # 汉堡披萨：
    #hanbaopisa = ['汉堡', '披萨', '匹萨', '比萨', '炸鱼', '薯条', '炸鸡', '热狗', '鸡肉卷', '堡', '鸡腿', '鸡柳', '鸡翅', '鸡块', '蛋挞', '派']
    # hoguokaorou：
    type_4 = [fenlei_list[3],'香锅', '冒菜', '麻辣烫','烤鱼','海底捞','董家湾'
              ]
    # 小吃炸串：
    type_1 = ['自助餐','自助']
    type_2 = ['']
    type_3 = [fenlei_list[2],'甜点','饮品','饮料','甜品']
    type_5 = [fenlei_list[4],'料理','东南亚菜','日本','韩国','泰国','大和']
    type_6 = [fenlei_list[5],'西洋','美国','英国']
    type_8 = [fenlei_list[7],'地方','江西','徽','鲁','山东','湘','湖南','川','湖北','粤','广东','海南','东北','天津菜','地方菜','陕西','山西']
    type_10 = [fenlei_list[9],'家常']
    type_11 = [fenlei_list[10],'垃圾食品','炸的']

    add_list = [type_1,type_2,type_3,type_4,type_5,type_6,type_7,type_8,type_9,type_10,type_11]
    is_patterns = ['([\u4e00-\u9fa5g^不没非拒否]{,8})', '(在|到|就|是|想吃|想要|打算吃|来个|来份|来|吃)([\u4e00-\u9fa5g]{,8})',
                   '([\u4e00-\u9fa5g]{,6})(吧|还行|还可以|不错|挺好|来一个)', '([\u4e00-\u9fa5g]{1,6})(的)([\u4e00-\u9fa5g]{,6})']

    not_patterns = ["([\u4e00-\u9fa5g]{,4})(不好|不要|不喜欢|拒绝|木|不|不想吃|别|别去|别在)([\u4e00-\u9fa5g]{1,4})(要|需求|打算|计划|准备|问题)",
                    '([\u4e00-\u9fa5g]{1,4})(腻了|吃过|够了|多了|太)',
                    '(不|没|无|拒绝|木|不想|受够了|讨厌)([\u4e00-\u9fa5g]{,4})']

    both_patterns = ["(差不多|无所谓|通用|都可以|都行|不挑|都想|随便|无所谓|都还行|随意|都阔以)",
                     "(都|全|两|俩)([\u4e00-\u9fa5g^不]{,6})(吃|要|可以|需要|不好|不干净|用|合适|适合|不用|不在|不是)"]
    '''
    either_patterns = ["('要')([\u4e00-\u9fa5g]{1,8})(不好|不要|不喜欢|拒绝|木|不|不想吃|别|别去|别在)([\u4e00-\u9fa5g]{1,8})",
                       "('不要')([\u4e00-\u9fa5g]{1,8})(要)([\u4e00-\u9fa5g]{1,8})"] #不要不要 要不要
    
    double_not = ["('不要')([\u4e00-\u9fa5g]{1,8})(不要)([\u4e00-\u9fa5g]{1,8})"]
    '''

    office_home_both = ['(都|两者|两地)']

    special_patterns = ['(和|同|像)([\u4e00-\u9fa5g]{,4})(差不多|一样|类似)([\u4e00-\u9fa5g]{,2})(的)([\u4e00-\u9fa5g]{1,4})']

    positive = []
    negative = []
    #******************************************************************************************************************
    #利用模型
    words = food_taste_extract(answer)
    #print(words)
    positive_pinlei = []
    negative_pinlei = []

    if words[0] != '':
        positive = words[0].split(',')

        for positive_word in positive:
            if positive_word != '天塔':
                positive_pinlei.append(get_most_similar_categ_of_the_dish(positive_word))

    if words[2] !='':
        negative = words[2].split(',')
     #   print(negative)
        for negative_word in negative:
            if negative_word != '天塔':
                negative_pinlei.append(get_most_similar_categ_of_the_dish(negative_word))

    #print(positive_pinlei)
    #print(negative_pinlei)
    for i in positive_pinlei:
        for pinlei in i:
    #        print(pinlei)
    #        print(fenlei_list.index(pinlei))
            slot_occasion[fenlei_list.index(pinlei)] = 1
    for i in negative_pinlei:
        for pinlei in i:
    #        print(pinlei)
            slot_occasion[fenlei_list.index(pinlei)] = -1
    #print(slot_occasion)
    #******************************************************************************************************************
    choose_list = negative + positive
    print(choose_list)
    change_list = []
    for i in choose_list:
        # print(i)
        pinlei = get_most_similar_categ_of_the_dish(i)

        for pa in not_patterns:

            pa = re.compile(pa)
            # print(pa.findall(answer))
            match = add_str(pa.findall(answer))
            if have_word_in_specify_list([i], match):
                # print(match)
                for pin in pinlei:
                    slot_occasion[fenlei_list.index(pin)] = -1
                    change_list.append(fenlei_list.index(pin))


        for pa in is_patterns:
            pa = re.compile(pa)
            match = add_str(pa.findall(answer))
            for pin in pinlei:
                if have_word_in_specify_list([i], match) and fenlei_list.index(pin) not in change_list:
                    # print(match)
                    slot_occasion[fenlei_list.index(pin)] = 1
#***********************************************************************************************************************
    for pattern in is_patterns:
        pattern = re.compile(pattern)
        #print(pattern)
        answer = str(answer)
        match = add_str(pattern.findall(answer))
        for i in add_list:
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
                    slot_occasion[add_list.index(i)] = -1

            for pa in is_patterns:
                pa = re.compile(pa)
                match = add_str(pa.findall(answer))
                if have_word_in_specify_list(i, match) and slot_occasion[add_list.index(i)] != -1:
                    slot_occasion[add_list.index(i)] = 1
                    pass

    if judge_have_pattern(both_patterns, answer) and groove[3] == 0:
        slot_occasion[-1] = 1

    slot_occasion[1] = -3

    if slot_occasion == [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3] and groove[3] != 0 and groove[0] != []:
        print('groove:',groove[0])
        slot_occasion = groove[0]


    return slot_occasion

if __name__ == '__main__':
    result = analysis_type([[],[],[],0,0,0],'寝室')
    print(result)
