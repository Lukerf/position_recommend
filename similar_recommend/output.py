from mysql import mysql
from similar_recommend import similar_recommend
import re
import jieba
import logging
from gensim import corpora, models, similarities
# sql = mysql()
#str = ""
# results = sql .work_experience_require("3-5年")
# results1 = sql.edu_background_require("博士",results)
#
# for r in results1:
#     print(r)

# describe = sql.get_describe("3-5年","本科",8000)
# for value in describe.keys():
#     print(value)
sr = similar_recommend("3-5年","本科",8000,"计算机 大学 相关 专业 毕业 年 及 以上 asp net c# 开发 经验")
for i in sr.sim_sort:
    print(i[0])
