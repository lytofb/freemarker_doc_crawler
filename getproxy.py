__author__ = 'root'
import request_class;
from db_mysql_module import SQLiteWraper;
import traceback;
import random;
import time;

class proxypool(object):
    def __init__(self,username,password,host,dbname):
        self.pool = [];
        self.db = SQLiteWraper(username,password,host,dbname);
        try:
            result = self.db.select("select * from proxylist");
            for record in result:
                self.pool.append({"http":"http://"+record["ip"]+":"+record["port"]})
        except Exception as e:
            traceback.print_stack()

    def buildpool(self,url):
        soup = self.retryurl(3,url)
        return soup;

    def retryurl(self,times,url):
        if times>0:
            times = times -1;
            try:
                if len(self.pool)>0:
                    proxyobj = random.choice(self.pool)
                    soup = request_class.getsoup_by_url(url,proxyobj)
                else:
                    soup = request_class.getsoup_by_url(url)
                return soup;
            except Exception as e:
                return self.retryurl(times,url)
        else:
            return request_class.getsoup_by_url(url);

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


if __name__=="__main__":
    px = proxypool('developer','developer','172.28.217.66','smzdmcrawl')
    for i in range(1,20):
        if i ==1:
            targeturl = "http://www.kuaidaili.com/free/inha/"
        else:
            targeturl = "http://www.kuaidaili.com/free/inha/"+str(i)
        px.crawlproxypage(targeturl)


# CREATE TABLE `proxylist` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `ip` varchar(255) DEFAULT NULL,
#   `port` varchar(255) DEFAULT NULL,
#   `type` varchar(255) DEFAULT NULL,
#   `enabled` int(11) DEFAULT '1',
#   `createtime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
