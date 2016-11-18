__author__ = 'root'
import request_class;
import json;
import time;
import re;
from db_mysql_module import SQLiteWraper;

def _loadzmdajax(sorttime,harfile,zdmajaxtpl="http://faxian.smzdm.com/json_more?filter=h1s183t0f0c0&type=new&timesort=",depth = 1):
    ajaxsession = request_class.getsession(harfile=harfile)
    ajaxsession.headers.update({"X-Requested-With":"XMLHttpRequest","Referer":"http://faxian.smzdm.com/h1s183t0f0c0p1/"})
    resp = ajaxsession.get(zdmajaxtpl+sorttime)
    json_object_list =  json.loads(resp.text);
    for json_object in json_object_list:
        yield json_object;
    if depth>1:
        depth = depth-1;
        yield from _loadzmdajax(str(json_object_list[-1]["timesort"]),harfile,zdmajaxtpl,depth)

def loadzmdajax(sortime,harfile,ajaxtpl,depth=1):
    yield from _loadzmdajax(sortime,harfile,ajaxtpl,depth)

def getdictobject(dictionary,key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None;


# soup = request_class.getsoup_by_url("http://faxian.smzdm.com/h1s183t0f0c0p1/",harfile=harfile);
# feedlist = soup.select("ul.feed-list-col li")
# lasttimesort = feedlist[-1].attrs;
# ajaxsession = request_class.getsession(harfile=harfile)
# ajaxsession.headers.update({"X-Requested-With":"XMLHttpRequest","Referer":"http://faxian.smzdm.com/h1s183t0f0c0p1/"})
# resp = ajaxsession.get("http://faxian.smzdm.com/json_more?filter=h1s183t0f0c0&type=new&timesort="+lasttimesort["timesort"])
# responsejson = json.loads(resp.text);
# for feed in feedlist:
#     producttitle = feed.select(".feed-ver-title")[0]
#     productprice = producttitle.find_next_siblings("div")[0].text
#     productname = feed.select(".feed-ver-title a")[0].text
#     smzdmlink = producttitle.find("a").attrs['href'];
#     zdmid = smzdmlink.split("/")[-2]
#     try:
#         feedlink = feed.select(".feed-link-btn-inner a")[0].attrs['href']
#     except Exception as e:
#         feedlink = ""
#     print(productname,productprice,smzdmlink,feedlink,"\n")


if __name__=="__main__":
    db = SQLiteWraper("developer","developer","172.28.217.66","smzdmcrawl");
    harfile = "D:\\build\\jingxuan.har"
    ajaxtpl="http://www.smzdm.com/json_more?timesort="
    thistime = str(int(time.time()))
    jsono = loadzmdajax(thistime,harfile,ajaxtpl,1)
    stack=[]
    for json_object in jsono:
        # print(json_object)
        # article_avatar = json_object['article_avatar']
        # article_avatar_url = json_object['article_avatar_url']
        article_id = json_object.get('article_id')
        article_url = json_object.get('article_url')
        article_link = json_object.get('article_link')
        article_mall = json_object.get('article_mall')
        article_mall_domain = json_object.get('article_mall_domain')
        article_price = json_object.get('article_price')
        article_title = json_object.get('article_title')
        article_top_category = json_object.get('article_top_category')
        gtm = json_object.get('gtm')
        if gtm:
            gtmprice = gtm.get('rmb_price')
            gtmtitle = gtm.get('title')
            gtmbrand = gtm.get('brand')
            gtmmall = gtm.get('mall')
            gtmid = gtm.get('id')
            if not re.match(r"^-?[0-9]+$",str(gtmprice)):
                gtmprice = 0;
            gtmtuple = (gtmtitle,gtmbrand,gtmmall,gtmprice,gtmid)
        else :
            gtmtuple = (None,None,None,None,None)
        paramtuple = gtmtuple\
                     +(article_id,article_url,article_link,article_mall,article_mall_domain,article_price,article_title,article_top_category)
        stack.append(paramtuple)
    while len(stack)>0:
        ptuple = stack.pop()
        if db.isunique("zdmcrawl","article_id",ptuple[5]):
            insertsql = "insert into zdmcrawl (gtmtitle,gtmbrand,gtmmall,gtmprice,gtmid,article_id,article_url,article_link,article_mall,article_mall_domain,article_price,article_title,article_top_category) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            db.execute(insertsql,*ptuple)



# CREATE TABLE `zdmcrawl` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `gtmtitle` varchar(255) DEFAULT NULL,
#   `gtmbrand` varchar(255) DEFAULT NULL,
#   `gtmmall` varchar(255) DEFAULT NULL,
#   `gtmprice` int(11) DEFAULT NULL,
#   `gtmid` int(11) DEFAULT NULL,
#   `article_id` int(11) DEFAULT NULL,
#   `article_url` varchar(255) DEFAULT NULL,
#   `article_link` varchar(255) DEFAULT NULL,
#   `article_mall` varchar(255) DEFAULT NULL,
#   `article_mall_domain` varchar(255) DEFAULT NULL,
#   `article_price` varchar(255) DEFAULT NULL,
#   `article_title` varchar(255) DEFAULT NULL,
#   `article_top_category` varchar(255) DEFAULT NULL,
#   `published` int(11) DEFAULT '0',
#   `createtime` timestamp NULL DEFAULT NULL,
#   `updatetime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `article_id_index` (`article_id`) USING HASH
# ) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
#