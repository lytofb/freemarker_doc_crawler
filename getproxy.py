__author__ = 'root'
import request_class;
from db_mysql_module import SQLiteWraper;
import traceback;
import random;
import time;
import math;
import threading;
import concurrent.futures.thread as thread

class proxypool(object):
    def __init__(self,username,password,host,dbname,loadpool=True,harfile=None):
        self.testurl = "http://www.kuaidaili.com/free/inha/";
        self.pool = [];
        self.availablepool=[];
        self.copiedpool=[];
        self.harfile = harfile;
        self.session = request_class.getsession(harfile=harfile);
        # self.proxypool=[];
        self.db = SQLiteWraper(username,password,host,dbname);
        if loadpool:
            self.loadpooltomem();

    def loadpooltomem(self):
        try:
            availableresult = self.db.select("select * from proxylist where enabled = 1 and costtime <4");
            result = self.db.select("select * from proxylist");
            for record in result:
                self.pool.append({"http":"http://"+record["ip"]+":"+record["port"],"id":record["id"],"costtime":record["costtime"]})
                # thistuple = {"http":"http://"+record["ip"]+":"+record["port"],"id":record["id"]},
                # self.proxypool.append(thistuple)
            for record in availableresult:
                self.availablepool.append({"http":"http://"+record["ip"]+":"+record["port"],"id":record["id"],"costtime":record["costtime"]})
                self.copyavailablepool()
        except Exception as e:
            traceback.print_stack()


    def buildpool(self,url):
        # soup = self.loopretryurl(url)
        # if not soup:
        #     soup = request_class.getsoup_by_url(url)
        soup = self.retryurl(6,url)
        return soup;

    def loopretryurl(self,url):
        for proxyobj in self.copiedpool:
            try:
                soup = request_class.getsoup_by_url(url,proxy=proxyobj["http"],timeout=proxyobj["costtime"]+2,harfile=self.harfile)
                print("+++++++++++++++++++++++++++++++++++++++++++++++")
                print("using proxy http ip=============="+proxyobj["http"])
                print("+++++++++++++++++++++++++++++++++++++++++++++++")
                return soup;
            except Exception as e:
                continue
        return None;

    def retryurl(self,times,url):
        if times>0:
            times = times -1;
            try:
                if len(self.copiedpool)>0:
                    proxyobj = self.copiedpool.pop()
                    # proxyobj = random.choice(self.copiedpool)
                    soup = request_class.getsoup_by_url(url,proxy=proxyobj,timeout=proxyobj["costtime"]+2,harfile=self.harfile)
                elif len(self.availablepool)>0:
                    self.copyavailablepool()
                else:
                    print("no proxy using")
                    soup = request_class.getsoup_by_url(url,harfile=self.harfile)
                return soup;
            except Exception as e:
                return self.retryurl(times,url)
        else:
            print("no proxy using")
            return request_class.getsoup_by_url(url,harfile=self.harfile);

    def copyavailablepool(self):
        self.copiedpool=[ap for ap in self.availablepool]
        timestamp = gettimestamp();
        for copied in self.copiedpool:
            copied["timestamp"] = timestamp;

    def crawlproxypage(self,targeturl):
        # targeturl = "http://www.kuaidaili.com/free/inha/";
        print("starting crwaling page "+targeturl)
        pagesoup = self.buildpool(targeturl)
        trlist = pagesoup.select("#list tbody tr");
        proxyinserttpl = "insert into proxylist (ip,port,type,createtime) values (%s,%s,%s,%s)";
        proxyparamlist=[];
        print("this page has "+str(len(trlist)))
        for tr in trlist:
            timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
            tdlist = tr.select("td")
            ip = tdlist[0].text
            port = tdlist[1].text
            type = tdlist[3].text
            self.pool.append({"http":"http://"+ip+":"+port})
            if self.db.isunique("proxylist","ip",ip):
                proxyparamlist.append((ip,port,type,timenow))
            else:
                print(ip+" not unique")
        self.db.tplbatch(proxyinserttpl,*proxyparamlist)
        print("insert record num "+str(len(proxyparamlist)))
        print("finished crwaling page "+targeturl)

    def testproxy(self,p,mosttimeout=10):
        # for p in self.pool:
        id = p["id"];
        httpproxy = p["http"]
        maxcosttime = p["costtime"]
        try:
            starttime = math.floor(time.time());
            resp = request_class.getresponse_by_url(self.testurl,proxy=p,timeout=mosttimeout,harfile=self.harfile)
            if str(resp.status_code)!='200':
                raise Exception
            endtime = math.ceil(time.time());
            costtime = endtime-starttime;
            print(resp.status_code,"using time:",endtime-starttime)
            print("available id======>"+str(id))
            self.updatestatus(id,1,costtime)
        except Exception as e:
            # print("unavailable id===>"+str(id))
            self.updatestatus(id,0)

    def runMulti(self,foo,argslist):
        for arg in argslist:
            t = threading.Thread(target=foo,args=arg)
            t.start()

    def updatestatus(self,id,status,costtime = None):
        param = (status,id)
        if costtime:
            updatesql = "update proxylist set costtime = %s, enabled = %s where id = %s"
            param = (costtime,status,id)
        else:
            updatesql = "update proxylist set enabled = %s where id = %s"
        self.db.execute(updatesql,*param)

    def multi_test_proxy(self):
        self.run_thread_by_pool(self.testproxy,self.pool)

    def crawl_proxyurl_inorder(self,targetpls,start=1,end=20):
        for targetpl in targetpls:
            for i in range(start,end):
                # time.sleep(5)
                if i ==1:
                    targeturl = targetpl
                else:
                    targeturl = targetpl+str(i)
                self.crawlproxypage(targeturl)

    def run_thread_by_pool(self,foo,argslist):
        executor = thread.ThreadPoolExecutor(max_workers=1000)
        for arg in argslist:
            executor.submit(foo,arg)

    def retrieveproxy(self,apiurl):
        resp = request_class.getresponse_by_url(apiurl,harfile=self.harfile)
        resp_text = resp.text;
        ipproxylist = resp.text.split("\r\n");
        paramslist = [tuple(k.split(":")) for k in ipproxylist if self.db.isunique("proxylist","ip",k.split(":")[0])]
        self.db.tplbatch("insert into proxylist (ip,port,type,proxy_source) values (%s,%s,'HTTP','daxiang')",paramslist)
        self.loadpooltomem();

    def importproxy(self,filepath):
        f = open(filepath)
        paramslist = [];
        for line in f:
            if self.db.isunique("proxylist","ip",line.split(":")[0]):
                paramslist.append(tuple(line.split(":")))
        self.db.tplbatch("insert into proxylist (ip,port,type,proxy_source) values (%s,%s,'HTTP','daxiang')",paramslist)
        self.loadpooltomem();


def gettimestamp():
    return math.floor(time.time())

def run_thread_by_pool(foo,argslist):
    executor = thread.ThreadPoolExecutor(max_workers=100)
    for arg in argslist[0:1]:
        executor.submit(foo,arg)


def toptestproxy(p,db):

    def updatestatus(id,status):
        param = (status,id)
        updatesql = "update proxylist set enabled = %s where id = %s"
        db.execute(updatesql,*param)
    # for p in self.pool:
    print(p)
    id = p["id"];
    httpproxy = p["http"]
    try:
        resp = request_class.getresponse_by_url("http://www.kuaidaili.com/free/inha/",proxy=p,harfile=None)
        if str(resp.status_code)!='200':
            raise Exception
        print(resp.status_code)
        print("available id======>"+str(id))
        updatestatus(id,1)
    except Exception as e:
        print("unavailable id===>"+str(id))
        updatestatus(id,0)

if __name__=="__main__":
    px = proxypool('developer','developer','172.28.217.66','smzdmcrawl',False)
    targetpl = ["http://www.kuaidaili.com/free/inha/"]
    # px.importproxy("C:\\Users\\octnn\\Downloads\\daxiang.txt")
    daxiangapi = "http://tpv.daxiangdaili.com/ip/?tid=559083828707040&num=10&delay=1&foreign=none&filter=on";
    # daxiangapi = "http://tpv.daxiangdaili.com/ip/?tid=559083828707040&num=500";
    px.retrieveproxy(daxiangapi)
    px.multi_test_proxy()
    # px.crawl_proxyurl_inorder(targetpl)

    from pathos.multiprocessing import ProcessingPool as Pool;
    # from multiprocessing import Process;
    # Process(target=run_thread_by_pool,args=(toptestproxy,(px.pool,px.db,))).start()
    # p = Pool(4)
    # p.map(px.multi_test_proxy)
    # p.map(px.crawl_proxyurl_inorder,(targetpl,))
    # p = Process(target=px.multi_test_proxy).start()
    # q = Process(target=px.crawl_proxyurl_inorder,args=(targetpl,)).start()


# CREATE TABLE `proxylist` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `ip` varchar(255) DEFAULT NULL,
#   `port` varchar(255) DEFAULT NULL,
#   `type` varchar(255) DEFAULT NULL,
#   `enabled` int(11) DEFAULT '1',
#   `createtime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;