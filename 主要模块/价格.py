import re
import string

s = '38x1x234x35x612x3yxxx'

CN_NUM = {
    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9}
CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}
def have_word_in_specify_list(word_list, str_temp):
    for word in word_list:
        if word in str_temp:
            return True


def chinese_to_arabic(cn: str) -> int:
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val

def delete_substr_method2(in_str, in_substr):
  start_loc = in_str.find(in_substr)
  len_substr = len(in_substr)
  res_str = in_str[:start_loc] + in_str[start_loc + len_substr:]
  return res_str


def numberdetection(answer,groove):
    #    patternnumber = re.compile('([一二三四五六七八九零十百千万亿]+|[0-9]+[]*[0-9])')
    patternnumber = re.compile('[一二三四五六七八九零十百千万亿0-9]*')
    lesspattern = re.compile('不到|不足|差点|差点儿|欠点|差一点|差一点儿|欠一点|欠点儿|欠一点儿|没有')
    largerpattern1 = re.compile('超过|超了|上')
    largerpattern2 = re.compile('超|多|大')

    unitpattern1 = re.compile('元|块')  # xx块豆腐难以处理
    unitpattern2 = re.compile('价格|价钱')
    disturbpattern1 = re.compile('瓶|杯|箱|米|步|碗|个|只|串|盘')
    disturbpattern2 = re.compile('面积|占地|空间|大小')
    disturbpattern3 = re.compile('里台|维路')
    abstract_pattern = re.compile('几十|几百|钱不是问题|价格不是问题')
    cheap_words = ['便宜', '物美价廉', '价格低', '打折', '优惠', '低价', '甩卖', '折扣', '划算', '实惠']
    expensive_words = ['贵', '高价', '天价', '收费高', '奢侈', '奢华']

    numbers = []
    lesslarger = []
    isdistrub = []
    isarea = []
    userstr = answer
    result = abstract_pattern.findall(userstr)
    if len(result):
        if '几十' in answer:
            userstr = delete_substr_method2(userstr,'几十')
        if '几百' in answer:
            userstr = delete_substr_method2(userstr,'几百')
        numbers.append(100)
        lesslarger.append(0)
        isarea.append(0)
        isdistrub.append(0)
    print(result)
    print(userstr)
    allr_past = patternnumber.findall(userstr)

    allr = [lr for lr in allr_past if lr != '']

    prePos = 0
    print(allr)
    for i in allr:
        # print(i)
        if i == '一':
            continue
        # print('*')
        nPos = allr_past.index(i)
        # print(nPos)

        # 根据数字前后信息判断是小于，大于，还是约等于
        r = 0
        result = lesspattern.findall(userstr, nPos - 4, nPos + 6)
        if len(result):
            r = r - 1
            # print(result)
        result = largerpattern1.findall(userstr, nPos - 5, nPos + 6)
        if len(result):
            r = r + 1
            # print(result)
        result = largerpattern2.findall(userstr, nPos - 1, nPos + len(i) + 1)
        if len(result):
            r = r + 1
            # print('here')
        lesslarger.append(r)

        # 根据数字前后信息判断是否为干扰类
        r = 0;
        result = disturbpattern1.findall(userstr, nPos, nPos + 6)

        if len(result):
            r = 1
        result = disturbpattern2.findall(userstr, nPos - 4, nPos)
        if len(result):
            r = 1
        result= disturbpattern3.findall(userstr, nPos - 4, nPos+4)
        if len(result):
            r = 1
        isdistrub.append(r)

        # 根据数字前后信息判断是否为价格类
        r = 0;
        result = unitpattern1.findall(userstr, nPos, nPos + 6)
        if len(result):
            r = 1
        result = unitpattern2.findall(userstr, nPos - 4, nPos)
        if len(result):
            r = 1
        isarea.append(r)

        if i.isdigit():
            numbers.append(i)
        else:
            numbers.append(chinese_to_arabic(i))

        # print(i)
        # print(nPos)
        delete_record = []
        for i in isdistrub:
            if i == 1:
                index = isdistrub.index(i)
                del numbers[index]
                del lesslarger[index]
                del isarea[index]
                del isdistrub[index]
    result = [numbers, lesslarger, isdistrub, isarea]

    if  result== [[],[],[],[]] and groove[3] != 2 and groove[2] !=[]:
        result = groove[2]
    #print(numbers, lesslarger, isdistrub, isarea)
    if result == [[],[],[],[]]:
        if have_word_in_specify_list(cheap_words,answer):
            numbers.append(20)
            lesslarger.append(0)
            isarea.append(0)
            isdistrub.append(0)
            result = [numbers, lesslarger, isdistrub, isarea]

    if result == [[],[],[],[]]:
        if have_word_in_specify_list(expensive_words,answer):
            numbers.append(100)
            lesslarger.append(0)
            isarea.append(0)
            isdistrub.append(0)

            numbers.append(40)
            lesslarger.append(0)
            isarea.append(0)
            isdistrub.append(0)
    return result


if __name__=='__main__':
    teststr = '价格不是问题' \
              ''
    print(teststr)
    #[numbers, lesslarger, isdisturb, isarea] = numberdetection(teststr)
    result = numberdetection(teststr,[[],[],[],2,0,0])
    print(result)