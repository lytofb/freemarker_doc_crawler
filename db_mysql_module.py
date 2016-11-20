__author__ = 'root'
import pymysql;
import sqlalchemy;
import threading;
from time import clock;
class SQLiteWraper(object):
    def __init__(self,username,password,host,dbname):
        # self.lock = threading.RLock()
        self.engine = sqlalchemy.create_engine('mysql+pymysql://'+username+':'+password+'@'+host+'/'+dbname+'?charset=utf8')

    def get_conn(self):
        conn = self.engine.connect();
        return conn

    def conn_close(self,conn=None):
        conn.close()

    def time_counter(func):
        def count_second(self,*args,**kwargs):
            start=clock()
            rs = func(self,*args,**kwargs)
            finish=clock()
            print("%.2f" % (finish-start))
            return rs
        return count_second

    def conn_trans(func):
        def connection(self,*args,**kwargs):
            # self.lock.acquire()
            conn = self.get_conn()
            kwargs['conn'] = conn
            rs = func(self,*args,**kwargs)
            self.conn_close(conn)
            # self.lock.release()
            return rs
        return connection

    @time_counter
    @conn_trans
    def batch(self,sqllist,conn=None):
        trans = conn.begin()
        try:
            for sql in sqllist:
                print("executing ..."+sql)
                conn.execute(sql)
            trans.commit()
        except pymysql.IntegrityError as e:
            #print e
            return -1
        except Exception as e:
            print (e)
            return -2
        return 0

    @time_counter
    @conn_trans
    def tplbatch(self,sqltpl,*params,conn=None):
        trans = conn.begin()
        try:
            for param in params:
                conn.execute(sqltpl,param)
            trans.commit()
        except pymysql.IntegrityError as e:
            #print e
            return -1
        except Exception as e:
            print (e)
            return -2
        return 0

    @conn_trans
    def select(self,sql,*param,conn=None):
        resultdictlist = []
        trans = conn.begin()
        try:
            if param:
                result = conn.execute(sql,param)
            else:
                result = conn.execute(sql)
            for row in result:
                resultdict={};
                for t in row.items():
                    resultdict[t[0]] = t[1]
                resultdictlist.append(resultdict)
            trans.commit()
        except pymysql.IntegrityError as e:
            #print e
            return -1
        except Exception as e:
            print (e)
            return -2
        return resultdictlist

    @conn_trans
    def execute(self,sql,*param,conn=None):
        if param is not tuple:
            param = param,
        trans = conn.begin()
        try:
            if param:
                result = conn.execute(sql,param)
            else:
                result = conn.execute(sql)
            trans.commit()
        except pymysql.IntegrityError as e:
            #print e
            return -1
        except Exception as e:
            print (e)
            return -2
        return result

    def isunique(self,tablename,colulmnname,columnvalue):
        if columnvalue is not tuple:
            params = columnvalue,
        selectsql = "select count(1) as record_count from "+tablename+" where "+colulmnname+" =%s"
        result = self.select(selectsql,*params)
        if (type(result) is int):
            print("error in check unique")
        elif result[0]["record_count"]>0:
            return False;
        else:
            return True;

    @time_counter
    def sqrt(self,a, eps=1e-10):
        if a == 0.0 or a == 1.0:
            return a
        x = 1.0
        y = x - (x*x-a)/(2*x)
        while not (-eps < y-x < eps):
            x = y
            y = x - (x*x-a)/(2*x)
        return x
if __name__=='__main__':
    param = ('1',8385707)
    db = SQLiteWraper('developer','developer','172.28.217.66','xixiche');
    ##################check unique#########
    check_result = db.isunique("data_user","user_name","qgy")
    print(check_result);exit(0)
    ##################select,select with params##############################
    # data_merchant = db.select("select * from data_merchant")
    # data_merchant = db.select("select * from data_merchant where enabled = %s and tel_num = %s",*param)
    # for row in data_merchant:
    #     print(row.items())
    ##################batch,batch with params##############################
    sqltpl = "insert into test (name,test_bigint) values (%s,%s)"
    params = [('1',8385707),('2',8385707)]
    db.tplbatch(sqltpl,*params)
    # testsql = [];
    # for i in range(1,10):
    #     testsql.append("insert into test (name,test_bigint) values ('hehe','"+str(i)+"')")
    # db.batch(testsql)
