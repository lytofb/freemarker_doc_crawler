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

    @conn_trans
    def select(self,sql,conn=None):
        resultdictlist = []
        trans = conn.begin()
        try:
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
    def execute(self,sql,conn=None):
        trans = conn.begin()
        try:
            result = conn.execute(sql)
            trans.commit()
        except pymysql.IntegrityError as e:
            #print e
            return -1
        except Exception as e:
            print (e)
            return -2
        return result

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
    db = SQLiteWraper('developer','developer','172.28.217.66','xixiche');
    data_merchant = db.select("select * from data_merchant")
    for row in data_merchant:
        print(row.items())
    # print(db.sqrt(100))
    # testsql = [];
    # for i in range(1,10):
    #     testsql.append("insert into test (name,test_bigint) values ('hehe','"+str(i)+"')")
    # print("sqllist prepared")
    # db.batch(testsql)
