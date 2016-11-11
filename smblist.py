__author__ = 'root'
from smb.SMBConnection import SMBConnection
import os;
def smbwalk(self,top):
    yield from self._smbwalk(top);

def _smbwalk(self,top):
    shareds = self.listpath_ex(top)
    dirs = [];
    files = [];
    for share in shareds:
        filename = share.filename;
        isdirectory = share.isDirectory;
        if filename=="." or filename=="..":
            continue
        if isdirectory:
            dirs.append(filename)
        else :
            files.append(filename)
    yield top,dirs,files
    for thisdir in dirs:
        thistop = os.path.join(top,thisdir)
        yield from self._smbwalk(thistop)

def listpath_ex(self, path):
    return self.listPath(self.remote_sv,path)

def mysmbcon_factory(host,remote_server,username,password,my_name='default_name',port=139,remote_name='root',use_ntlm_v2 = True):
    MySMBConnection = type('MySMBConnection',(SMBConnection,),{"listpath_ex":listpath_ex,"remote_sv":remote_server,"smbwalk":smbwalk,"_smbwalk":_smbwalk})
    conn = MySMBConnection(username, password, my_name, remote_name, use_ntlm_v2 = use_ntlm_v2)
    conn.connect(host, port)
    return conn;

if __name__=="__main__":
    conn = mysmbcon_factory('172.28.217.66','knose','root','p@ssw0rd')
    smbresult = conn.smbwalk("/maven")
    for r in smbresult:
        print(r)