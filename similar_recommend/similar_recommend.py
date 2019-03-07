import re
import jieba
from mysql import mysql
import logging
from gensim import corpora, models, similarities
class similar_recommend(object):
    def __init__(self,work_experience,edu_background,ex_salary,describe):
        self.describe = describe
        sql = mysql()
        self.cibao = sql.get_describe(work_experience,edu_background,ex_salary)
        self.cibao_w()
        self.sim_num = self.similarity()  #字典，station_id:匹配度
        self.sim_sort = sorted(self.sim_num.items(),key=lambda item:item[1],reverse=True)
        # self.results = sort_(sim_num)
    def similarity(self):
        logging.basicConfig(format='%(asctime)s  : %(levelname)s : %(message)s', level=logging.INFO)

        class MyCorpus(object):
            def __iter__(self):
                for line in open("cibao.txt",'r',encoding = 'utf-8'):
                    yield line.split()

    # 以下是把职位要求通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
        Corp = MyCorpus()
        dictionary = corpora.Dictionary(Corp)#把所有职位要求转化为词包（bag of words）
        corpus = [dictionary.doc2bow(text) for text in Corp]

        tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该职位要求集的tf-idf 模型

        corpus_tfidf = tfidf[corpus]#此处已经计算得出所有职位要求的tf-idf 值

    # q_file = open(querypath, 'r',encoding="utf-8")
    # query = q_file.readline()
    # q_file.close()
        query = self.describe
        vec_bow = dictionary.doc2bow(query.split())#把个人技能描述转为词包
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出个人技能描述的tf-idf 值

        index = similarities.MatrixSimilarity(corpus_tfidf)#把所有职位要求做成索引
        sims = index[vec_tfidf]#利用索引计算每一条职位要求和个人技能描述之间的相似度

        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档

        #sim_file = open(storepath, 'w')
        sim_num = {}
        i=0
        for id in self.cibao.keys():
            sim_num[id] = similarity[i]
            i=i+1
        return sim_num
        #for i in similarity:

           # sim_file.write(str(i)+'\n')
        #sim_file.close()



    def cibao_w(self): #将技能描述转化位词包，并且写入txt文件
        stopwords = ['，', '于', '的', '是', '：', ':', '；', '、', '和', '有', '或', '等', '/', '.', '（', '）', '1', '2', '3', '4','5']  # 用来去除停用词
        file = open("cibao.txt", 'w', encoding="utf-8")
        Flag = 0
        for row in self.cibao.values():
            describe = row
            s = re.split(r'资格.', describe)
            if (len(s) < 2):
                s = re.split(r'要求.', describe)
            if (len(s) < 2):
                Flag = 1
            #     # print(s[0])
            #     # t=t+1
            #     continue
            if(Flag==0):
                r = re.split(r'。', s[1])
            else:
                r = re.split(r'。',s[0])
            words = jieba.cut(r[0], cut_all=False)
            for word in words:
                if word not in stopwords:
                    file.write(word + " ")
            file.write('\n')
        file.close()



