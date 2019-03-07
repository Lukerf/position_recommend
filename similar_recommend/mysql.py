import pymysql
import re

def tuple2str(results):
    i = 0
    str = "("
    for r in results:
        i = i + 1
        for R in r:
            tem = '%d' % R
            str = str + "'" + tem + "'" + ","
    str = str + ")"
    return str
class mysql(object):
    def __init__(self):
        db = pymysql.connect("localhost","root","root","postmatch")
        self.cursor =db.cursor()

    def get_describe(self,work_experience,edu_background,salary_min):#返回的是字典，station_id:describes
        sql = "select station_id,describes from companyinfo where station_id in"+self.work_experience_require(work_experience)+"and station_id in"+self.edu_background_require(edu_background)+"and station_id in"+self.salary_require(salary_min)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        des={}
        for r in results:
            des[r[0]]=r[1]
        return des
    def work_experience_require(self,work_experience):
        if(work_experience=="5-10年"):
            sql = "(select station_id from companyinfo)"
        elif(work_experience=="3-5年"):
            sql = "(select station_id from companyinfo where work_experience!='5-10年')"
        elif(work_experience=="1-3年"):
            sql = "(select station_id from companyinfo where work_experience!='5-10年'and work_experience!='3-5年')"
        else:
            sql = "(select station_id from companyinfo where work_experience!='5-10年'and work_experience!='3-5年'and work_experience!='1-3年')"
        return sql
    def edu_background_require(self,edu_background):
        if(edu_background=="博士"):
            sql = "(select station_id from companyinfo)"
        elif(edu_background=="硕士"):
            sql = "(select station_id from companyinfo where edu_background!='博士')"
        elif(edu_background=="本科"):
            sql = "(select station_id from companyinfo where edu_background!='博士'and edu_background!='硕士')"
        elif(edu_background=="大专"):
            sql = "(select station_id from companyinfo where edu_background!='博士'and edu_background!='硕士'and edu_background!='本科')"
        elif(edu_background=="中专"):
            sql = "(select station_id from companyinfo where edu_background!='博士'and edu_background!='硕士'and edu_background!='本科'and edu_background!='大专')"
        else:
            sql = "select station_id from companyinfo where edu_background!='博士'and edu_background!='硕士'and edu_background!='本科'and edu_background!='大专'and edu_background!='中专'"
        return sql
    def salary_require(self,salary):
        sql = "select salary from companyinfo"
        flag=0
        id = 1
        str="("
        self.cursor.execute(sql)
        results=self.cursor.fetchall()
        for r in results:
            for R in r:
                if(R=='面议'):
                    flag=1
                elif (re.match('.*\-.*',R)):
                    s = R.split("-")
                    if(int(s[0])>salary):
                        flag=1
                    else:
                        flag=0
                else:
                    flag=0
                if(flag==1):
                    tem = '%d' % id
                    str = str + "'" + tem + "'" + ","
                id=id+1
        str=str+"'0')"
        return str
    def test(self):
        #sql = "select station_id from companyinfo where station_id in "+self.edu_background_require("本科")+"and station_id in"+self.work_experience_require("3-5年")+"and station_id in"+self.salary_require(6000)
        # sql = "select station_id from companyinfo where station_id in ('1','2','3')"
        sql = "select station_id,describes from companyinfo"
        self.cursor.execute(sql)
        results=self.cursor.fetchall()
        des={}
        for r in results:
            des[r[0]]=r[1]
        return des #select station_id from companyinfo where station_id in (work.....)and station_id in (edu..)and station_id in (salary..)