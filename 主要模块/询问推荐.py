import re

def judge_have_pattern(pattern_list, user_quesiton):
    for pa in pattern_list:
        pattern = re.compile(pa)
        if pattern.findall(user_quesiton):
            return True
    return False

def recommand(answer):
    price_patterns = ['(价格|多少钱|价位|折扣|批发价|怎么卖|价钱|贵多少|便宜|性价比|会不会贵|是不是贵|贵吗)']
    recommand_patterns = ['(推荐|安利|安排)']
    if judge_have_pattern(recommand_patterns, answer):
        return True
    else:
        return False