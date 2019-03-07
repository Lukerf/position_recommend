
import re
import jieba
from mysql import mysql
class cibao(object):
    def __init__(self):
        sql = mysql()
        self.results = sql.get_describe("3-5年","本科",6000)
        self.s_path="cibao.txt"
    def cibao_w(self): #将技能描述转化位词包，并且写入txt文件
        stopwords = ['，', '于', '的', '是', '：', ':', '；', '、', '和', '有', '或', '等', '/', '.', '（', '）', '1', '2', '3', '4','5']  # 用来去除停用词
        file = open(self.s_path, 'w', encoding="utf-8")
        for row in self.results.values:
            describe = row
            s = re.split(r'资格.', describe)
            if (len(s) < 2):
                s = re.split(r'要求.', describe)
            if (len(s) < 2):
                # print(s[0])
                # t=t+1
                continue
            else:
                r = re.split(r'。', s[1])
                words = jieba.cut(r[0], cut_all=False)
                for word in words:
                    if word not in stopwords:
                        file.write(word + " ")

                file.write('\n')
        file.close()
