import re

mh1 = re.compile(u'(不)')
mh20 = re.compile(u'([想]*告诉|[想]*说)|[想]*[搭]*理|不讲')
mh21 = re.compile(u'(知道|知不道|一定|清楚|明白|了解|明了|理会)')
mh3 = re.compile(u'(没话说|没意思|没想法|没毛病|你猜)')
def fuzzy(answers):
    if re.search(mh1, answers) and re.search(mh20, answers):
        return 1,'客官，这样让我很为难呀！'
    if re.search(mh1, answers) and re.search(mh21, answers):
        return 1, '客官，这样让我很为难呀！'
    if re.search(mh3, answers):
        return 1, '客官，你说的什么我简直太难理解了！'
    return 0,''
