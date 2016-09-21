def makedirs(path):
    import os;
    path = path.strip()
    path = path.rstrip("\\")
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        print(path+" made")
        return True;
    else:
        return False

def download_file_by_url(localpath,httpurl):
    import requests,os;
    if os.path.exists(localpath):
        print(localpath+" exists")
        return
    print("begin download "+httpurl+"save to "+localpath)
    r = requests.get(httpurl)
    if r.status_code==200:
        print("save success")
        with open(localpath,"wb") as download_file:
            download_file.write(r.content)
