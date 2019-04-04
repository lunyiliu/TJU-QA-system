import re
from judge_price import price
from pmjudge import pmjudgment
from sizeextraction import areajudgment


def judge_have_pattern(pattern_list, user_quesiton):
    for pa in pattern_list:
        pattern = re.compile(pa)
        if pattern.findall(user_quesiton):
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


def have_word_in_specify_list(word_list, str_temp):
    for word in word_list:
        if word in str_temp:
            return True
    return False


def analysis(answer, groove):
    """
    :param answer: user answer, str
    :param groove: groove,list
    :return: update groove list
    """

    assert len(groove) == 6
    assert len(answer) > 0
    groove_ori = [groove[i] for i in range(len(groove))]

    status = 0  # status  0:闲聊  1：相关
    slot_occasion = groove[0]  # slot_occasion 0:无关 1:office 2:home 3:all  “你在办公室用还是在家里用”
    slot_pm = groove[1]  # slot_pm #0: 无关 #1：yes #2: no #3: both #4：相关但不清楚
    slot_area = groove[2]  # slot_area #0: 无关 #1： <=50 #2: 50< <=100 #3: outofrange #4：矛盾 或者 确定不了，比如 大于50  小于 150
    question_type = groove[3]  # question_type 0:occasion 1:pm 2:area·

    answer = pre_process_question(answer)
    print(answer)


    slot_occasion = analysis_occasion(question_type, answer)
    slot_area = areajudgment(answer, question_type)
    slot_pm = pmjudgment(answer, question_type)
    print('occasion:', slot_occasion)
    print('area:', slot_area)
    print('need_pm:', slot_pm)

    # if slot_occasion == 0 and slot_area == 0 and slot_pm == 0:
    #     status = 0
    # else:
    #     status = 1

    # update
    temp_slot = [slot_occasion, slot_pm, slot_area]
    print(temp_slot)
    for i in range(3):
        if temp_slot[i] == 0:
            pass
        else:
            groove[i] = temp_slot[i]

    status = is_about(answer)
    # TODO: retain?
         
#    if price(answer):
#        groove[]
    if price(answer):
        return groove_ori, status
    return groove, status


def pre_process_question(user_question):
    user_question = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\d,，]', "", user_question)
    # normalize the question
    # user_question, version_words, type_words = normalize_entity(version_dic, type_dic, user_question)

    return user_question


def analysis_occasion(question_type, answer):
    slot_occasion = 0

    inner_school_words = ["校内", "学校里面", "食堂", "里面",'宿舍附近']

    out_school_words = ["校外", "外面", "四季村", "饭店", "小吃街",'八里台','鞍山西道']

    # is_patterns = ['(在|到|就|是)([\u4e00-\u9fa5g]{,8})', '([\u4e00-\u9fa5g,，]{,6})(需要|空气不好|不清新|不干净|洁净|不湿润|干燥|差)',
    #                '([\u4e00-\u9fa5g]{,6})(上|边|附近|旁|购|买|里)']

    is_patterns = ['([\u4e00-\u9fa5g^不没非拒否]{,8})', '(在|到|就|是)([\u4e00-\u9fa5g]{,8})',
                   '([\u4e00-\u9fa5g,，]{,6})(需要|空气不好|不清新|不干净|洁净|不湿润|干燥|差)',
                   '([\u4e00-\u9fa5g]{,6})(上|边|附近|旁|购|买|里|用)', '([\u4e00-\u9fa5g]{1,6})(的)([\u4e00-\u9fa5g]{,6})']

    not_patterns = ["([\u4e00-\u9fa5g]{,4})(不|没|无|拒绝|木)([\u4e00-\u9fa5g]{,4})(要|需求|打算|计划|准备|问题)",
                    ("(空气|呼吸)([\u4e00-\u9fa5g^不没非拒否]{,4})(不错|好|不差|接受|行)"),
                    '([\u4e00-\u9fa5g]{1,4})(有了|买过|有一台|买了|放了|已经有|已经买了)',
                    '(不|没|无|拒绝|木)([\u4e00-\u9fa5g]{,4})(在|是)([\u4e00-\u9fa5g]{1,4})']

    both_patterns = ["(差不多|无所谓|通用|都可以|都行|不挑|都想|随便|无所谓|都还行|随意|都阔以)",
                     "(都|全|两|俩)([\u4e00-\u9fa5g^不]{,6})(需要|不好|不干净|用|合适|适合|不用|不在|不是)"]

    office_home_both = ['(都|两者|两地)']

    special_patterns = ['(和|同|像)([\u4e00-\u9fa5g]{,4})(差不多|一样|类似)([\u4e00-\u9fa5g]{,2})(的)([\u4e00-\u9fa5g]{1,4})']

    match = ''
    if question_type in [1, 2]:
        is_patterns = is_patterns[1:]
    for pattern in is_patterns:
        pattern = re.compile(pattern)
        # print(pattern)
        answer = str(answer)
        match = add_str(pattern.findall(answer))
        if have_word_in_specify_list(inner_school_words, match) and not judge_have_pattern(not_patterns, answer):
            print('-')
            slot_occasion = 2
        if have_word_in_specify_list(out_school_words, match) and not judge_have_pattern(not_patterns, answer):
            print('--')
            slot_occasion = 1
        if judge_have_pattern(not_patterns, answer) and have_word_in_specify_list(out_school_words, answer):
            print('---')
            slot_occasion = 2
        if judge_have_pattern(not_patterns, answer) and have_word_in_specify_list(inner_school_words, answer):
            print('----')
            slot_occasion = 1

    if have_word_in_specify_list(inner_school_words, answer) and have_word_in_specify_list(out_school_words, answer):
        for pa in not_patterns:
            pa = re.compile(pa)
            match = add_str(pa.findall(answer))
            if have_word_in_specify_list(inner_school_words, match):
                slot_occasion = 1
            if have_word_in_specify_list(out_school_words, match):
                slot_occasion = 2

    if judge_have_pattern(both_patterns, answer) and question_type == 0:
        print('#')
        slot_occasion = 3

    if have_word_in_specify_list(out_school_words, answer) and have_word_in_specify_list(inner_school_words, answer):
        if not judge_have_pattern(not_patterns, answer):
            print('##')
            slot_occasion = 3

#    if judge_have_pattern(office_home_both, answer) and judge_have_pattern(not_patterns, answer):
#        print('###')
#        slot_occasion = 4

    if slot_occasion == 3 and judge_have_pattern(special_patterns, answer):
        for pattern in special_patterns:
            pattern = re.compile(pattern)
            str_temp = pattern.findall(answer)[0][-1]
            print('str_temp', str_temp)
            if have_word_in_specify_list(inner_school_words, str_temp):
                print('*')
                slot_occasion = 2
            if have_word_in_specify_list(out_school_words, str_temp):
                print('**')
                slot_occasion = 1
    if slot_occasion == 4:
        slot_occasion = 3

    # qurey_patterns = ["是不是", "能不能", "行不行", '哪', '怎么', '什么', '多少', '([\u4e00-\u9fa5g]{,4})(吗|么)', "为毛", "谁", "如何", '啥',
    #                   "好不好", "何时", "何地", "多远", "多久", "多长", "可不可以", "是否", "能否", "请问", "提问", "求解", "问"]
    # if judge_have_pattern(qurey_patterns,answer):
    #     slot_occasion = 0

    return slot_occasion

	
def analysis_type(question_type, answer):
    slot_occasion = 0
    #面
    noodle_words = ["面", "拉面", "面条", "挂面"]
    #炒菜
    stir_fry_words = ["炒菜", "烧菜", "小炒", "点菜"]
    #盖饭
    cover_rice_words = ["盖饭", "炒饭", "盖浇", "饭"]	
    # is_patterns = ['(在|到|就|是)([\u4e00-\u9fa5g]{,8})', '([\u4e00-\u9fa5g,，]{,6})(需要|空气不好|不清新|不干净|洁净|不湿润|干燥|差)',
    #                '([\u4e00-\u9fa5g]{,6})(上|边|附近|旁|购|买|里)']

    is_patterns = ['([\u4e00-\u9fa5g^不没非拒否]{,8})', '(在|到|就|是|想吃|想要|打算吃|来个|来份|来|吃)([\u4e00-\u9fa5g]{,8})',
                   '([\u4e00-\u9fa5g]{,6})(吧|还行|还可以|不错|挺好|来一个)', '([\u4e00-\u9fa5g]{1,6})(的)([\u4e00-\u9fa5g]{,6})']

    not_patterns = ["([\u4e00-\u9fa5g]{,4})(不好|不要|不喜欢|拒绝|木|不)([\u4e00-\u9fa5g]{,4})(要|需求|打算|计划|准备|问题)",
                    '([\u4e00-\u9fa5g]{1,4})(腻了|吃过|够了|多了|太)',
                    '(不|没|无|拒绝|木|不想|受够了|讨厌)([\u4e00-\u9fa5g]{,4})']

    both_patterns = ["(差不多|无所谓|通用|都可以|都行|不挑|都想|随便|无所谓|都还行|随意|都阔以)",
                     "(都|全|两|俩)([\u4e00-\u9fa5g^不]{,6})(吃|要|可以|需要|不好|不干净|用|合适|适合|不用|不在|不是)"]

    office_home_both = ['(都|两者|两地)']

    special_patterns = ['(和|同|像)([\u4e00-\u9fa5g]{,4})(差不多|一样|类似)([\u4e00-\u9fa5g]{,2})(的)([\u4e00-\u9fa5g]{1,4})']

    match = ''
    if question_type in [1, 2]:
        is_patterns = is_patterns[1:]
    for pattern in is_patterns:
        pattern = re.compile(pattern)
        # print(pattern)
        answer = str(answer)
        match = add_str(pattern.findall(answer))
        if have_word_in_specify_list(inner_school_words, match) and not judge_have_pattern(not_patterns, answer):
            print('-')
            slot_occasion = 2
        if have_word_in_specify_list(out_school_words, match) and not judge_have_pattern(not_patterns, answer):
            print('--')
            slot_occasion = 1
        if judge_have_pattern(not_patterns, answer) and have_word_in_specify_list(out_school_words, answer):
            print('---')
            slot_occasion = 2
        if judge_have_pattern(not_patterns, answer) and have_word_in_specify_list(inner_school_words, answer):
            print('----')
            slot_occasion = 1

    if have_word_in_specify_list(inner_school_words, answer) and have_word_in_specify_list(out_school_words, answer):
        for pa in not_patterns:
            pa = re.compile(pa)
            match = add_str(pa.findall(answer))
            if have_word_in_specify_list(inner_school_words, match):
                slot_occasion = 1
            if have_word_in_specify_list(out_school_words, match):
                slot_occasion = 2

    if judge_have_pattern(both_patterns, answer) and question_type == 0:
        print('#')
        slot_occasion = 3

    if have_word_in_specify_list(out_school_words, answer) and have_word_in_specify_list(inner_school_words, answer):
        if not judge_have_pattern(not_patterns, answer):
            print('##')
            slot_occasion = 3

#    if judge_have_pattern(office_home_both, answer) and judge_have_pattern(not_patterns, answer):
#        print('###')
#        slot_occasion = 4

    if slot_occasion == 3 and judge_have_pattern(special_patterns, answer):
        for pattern in special_patterns:
            pattern = re.compile(pattern)
            str_temp = pattern.findall(answer)[0][-1]
            print('str_temp', str_temp)
            if have_word_in_specify_list(inner_school_words, str_temp):
                print('*')
                slot_occasion = 2
            if have_word_in_specify_list(out_school_words, str_temp):
                print('**')
                slot_occasion = 1
    if slot_occasion == 4:
        slot_occasion = 3

    # qurey_patterns = ["是不是", "能不能", "行不行", '哪', '怎么', '什么', '多少', '([\u4e00-\u9fa5g]{,4})(吗|么)', "为毛", "谁", "如何", '啥',
    #                   "好不好", "何时", "何地", "多远", "多久", "多长", "可不可以", "是否", "能否", "请问", "提问", "求解", "问"]
    # if judge_have_pattern(qurey_patterns,answer):
    #     slot_occasion = 0

    return slot_occasion

def is_about(answer):
    qurey_patterns = ["是不是", "能不能", "行不行", '哪', '怎么', '什么', '多少', '([\u4e00-\u9fa5g]{,4})(吗|么)', "为毛", "谁", "如何", '啥',
                      "好不好", "何时", "何地", "多远", "多久", "多长", "可不可以", "是否", "能否", "请问", "提问", "求解", "问"]

    key_words = ['空气', '净化', '霾', '这款', '产品', '性能', '效果', '提升', "作用", '对比', '介绍', '价格', '价位', '优惠', "活动", "机器", "机子",
                 '特点', '特性', '功能', '体验', "作用", '功效', '卖点', '类似', '相同', '相比', '合算', '型号', '说明', '配套', '场合',
                 '范围', '场景', '污染', '甲醛', '装修', '呼吸', '便宜', '推荐', '适合', '操作', "打开", '睡眠', '静音', '提示', '自动',
                 '关机', '开机', '保修', "维修", "质保", '降价', "售后", "说明", "折扣", '这台', '功率', '电压', '外观', "区别", '不同', '通用', '适合',
                 '能用']

    if judge_have_pattern(qurey_patterns, answer) and have_word_in_specify_list(key_words, answer):
        return 1
    return 0
