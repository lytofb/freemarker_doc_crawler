__author__ = 'root'
import request_class;
lianjia_detail_url = "http://dl.lianjia.com/ershoufang/"

def get_header():
    headers = {"Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate, sdch',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'Upgrade-Insecure-Requests':1,
               'Connection':'keep-alive',
               'Host':'dl.lianjia.com',
               'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'"}
    return headers;

def get_lianjia_detail_soup(url):
    soup = request_class.getsoup_by_url(url,get_header(),"utf-8")
    return soup;

def get_area_list(url):
    lianjia_soup = get_lianjia_detail_soup(url)
    taglist = lianjia_soup.select("[data-role='ershoufang'] a")
    sublinklist = [{'text':x.text,'href':x.attrs['href'],'title':x.attrs['title']} for x in taglist]
    return sublinklist

def get_subarea_list(url):
    subarea_soup = get_lianjia_detail_soup(url)
    taglist = subarea_soup.select("[data-role='ershoufang'] div")[1].select('a')
    sublinklist = [{'text':x.text,'href':x.attrs['href']} for x in taglist]
    return sublinklist

def get_detail_info(url):
    detail_soup = get_lianjia_detail_soup(url)
    taglist = detail_soup.select(".houseInfo")
    taglista = [t.select('a').attrs['href'] for t in taglist]
    infolist = [x for x in taglist]
if __name__=='__main__':
    # arealinklist = get_area_list(lianjia_detail_url)
    get_subarea_list("http://dl.lianjia.com/ershoufang/ganjingzi/")