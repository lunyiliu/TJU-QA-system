NER模型使用说明：

1.本次训练所使用的主要工具包版本：Keras（2.1.2），gensim（3.2.0），TensorFlow（1.4.0）

2.使用方法：

调用foodtaste_extract函数，之后直接测试即可：

from exMenu import foodtaste_extract

string_1='我很喜欢小鸡炖蘑菇'

food,taste,food_n,taste_n=foodtaste_extract.foodtaste_extract(string_1)
