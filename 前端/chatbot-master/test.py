import sys
import os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
sys.path.append(r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\前期版本')
from robot import robot_airclean
from robot import get_product
#print(1)
blockPrint()
groove0=[int(element) for element in sys.argv[1].split(',')]
#print(groove0)
user_id = 123456
#answer = 123456
#groove0 = [0, 0, 0, 1, 1, 0]
answer=sys.argv[2]

user_id,reply,groove=robot_airclean(user_id,answer,groove0)
groove=[str(g)+',' for g in groove]
enablePrint()
#print('lll')
print("".join(groove).strip(","))
print(reply)
