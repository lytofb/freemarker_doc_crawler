__author__ = 'root'
import request_class;
import json;
import time;

def loadzmdajax(sorttime):
    ajaxsession = request_class.getsession(harfile=harfile)
    ajaxsession.headers.update({"X-Requested-With":"XMLHttpRequest","Referer":"http://faxian.smzdm.com/h1s183t0f0c0p1/"})
    resp = ajaxsession.get("http://faxian.smzdm.com/json_more?filter=h1s183t0f0c0&type=new&timesort="+sorttime)
    return json.loads(resp.text);


harfile = "D:\\build\\smzdm.com.har"
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
    thistime = str(int(time.time()))
    jsono = loadzmdajax(thistime)
    print(jsono)