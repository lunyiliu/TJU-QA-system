from robot import robot_airclean
from robot import get_product
user_id = 123456
answer = 123456
groove0 = [0, 0, 0, 1, 1, 0]
user_id,reply,groove=robot_airclean(user_id,answer,groove0)
print(reply)
while 1:
    answer=input()
    user_id,reply,groove=robot_airclean(user_id,answer,groove)
    print(reply)
