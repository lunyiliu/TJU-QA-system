from robot_for_qa import robot_qa
from robot import get_product
user_id = '123456'
answer = '123456'
groove0 = [[], [], [], 1, 1, 0]
record_times = [0,1,2]
user_id,reply,groove,record_times=robot_qa(user_id,answer,groove0,record_times)
print(reply)
while 1:
    answer=input()
    user_id,reply,groove,record_times=robot_qa(user_id,answer,groove,record_times)
    print(reply)
