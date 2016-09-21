__author__ = 'root'
import requests;import os;
from bs4 import BeautifulSoup;
import download_file;
import re;

def getsession():
    headers = {"Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate, sdch',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'Upgrade-Insecure-Requests':1,
               'Connection':'keep-alive,Host:freemarker.org',
               'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'"}
    req_session = requests.session();
    req_session.headers.update(headers)
    return req_session;

def getsoup_by_url(url):
    session = getsession();
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup;

def get_resource_url(base_url,append_url__taglist):
    return [{"absolute":base_url+x.attrs['src'],"relative":x.attrs['src']} for x in append_url__taglist]

def get_css_resource_url(base_url,append_url__taglist):
    return [{"absolute":base_url+x.attrs['href'],"relative":x.attrs['href']} for x in append_url__taglist]

def get_next_page_node_attrs(soup):
    next_tag = soup.select(".next")[0];
    return next_tag.attrs

def download_page_resource(entry_url):
    baseurl = "http://freemarker.org/docs/"
    html_local_path = "D:\\build\\freemarker"
    js_local_path = "D:\\build\\freemarker\\js"
    css_local_path = "D:\\build\\freemarker\\css"
    print("begin download "+entry_url)
    download_file.download_file_by_url(os.path.join(html_local_path,entry_url.split("/")[-1]),entry_url)
    soup = getsoup_by_url(entry_url)
    script_resource = soup.select("script")
    script_tag_list = list(filter(lambda x: 'src' in x.attrs, script_resource))
    script_resource_url_list = get_resource_url(baseurl,script_tag_list);
    css_resource = soup.select("link")
    css_tag_list = list(filter(lambda x: 'href' in x.attrs and (len(x.attrs['href'])<4 or x.attrs['href'][0:4]!='http'), css_resource))
    css_resource_url_list = get_css_resource_url(baseurl,css_tag_list);
    for url in script_resource_url_list:
        download_file.makedirs(os.path.split(os.path.join(js_local_path,url["relative"].replace("/","\\")))[0])
        download_file.download_file_by_url(os.path.join(js_local_path,url["relative"].replace("/","\\")),url["absolute"])
    for url in css_resource_url_list:
        download_file.makedirs(os.path.split(os.path.join(css_local_path,url["relative"].replace("/","\\")))[0])
        download_file.download_file_by_url(os.path.join(css_local_path,url["relative"].replace("/","\\")),url["absolute"])
    next_node_resource = get_next_page_node_attrs(soup);
    if 'href' in next_node_resource:
        next_url = next_node_resource['href']
        download_page_resource(baseurl+next_url)
    else:
        print("download end")

if __name__=='__main__':
    url = "http://freemarker.org/docs/index.html";
    download_page_resource(url)

    local_path = "D:\\build\\freemarker\\docgen-resources"
    with open("D:\\build\\freemarker"+"\\docgen-resources\\docgen.min.css","r") as cssfile:
        css_content =cssfile.read();
        print(css_content)
        extra_resource_list = re.findall('url\((.*?)\)',css_content);
        for url in extra_resource_list:
            resource_url = "http://freemarker.org/docs/docgen-resources/"+url;
            download_file.makedirs(os.path.split(os.path.join(local_path,url.replace("/","\\")))[0])
            download_file.download_file_by_url(os.path.join(local_path,url.replace("/","\\")).split("?")[0],resource_url)
