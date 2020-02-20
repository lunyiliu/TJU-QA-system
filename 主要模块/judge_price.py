import re

def judge_have_pattern(pattern_list, user_quesiton):
    for pa in pattern_list:
        pattern = re.compile(pa)
        if pattern.findall(user_quesiton):
            return True
    return False

def price(answer):
    price_patterns = ['(价格|多少钱|价位|折扣|批发价|怎么卖|价钱|贵多少|便宜|性价比|会不会贵|是不是贵|贵吗)']
    if judge_have_pattern(price_patterns, answer):
        return True
    else:
        return False