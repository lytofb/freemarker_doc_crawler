__author__ = 'root'
from smb.SMBConnection import SMBConnection
import os;
def smbwalk(top,conn):
    yield from _smbwalk(top,conn);

def _smbwalk(top,conn):
    shareds = conn.listpath_ex(top)
    for share in shareds:
        filename = share.filename;
        isdirectory = share.isDirectory;
        yield top,filename,isdirectory;
        if filename=="." or filename=="..":
            continue
        if isdirectory:
            thistop = os.path.join(top,filename)
            yield from _smbwalk(thistop,conn)

def listpath_ex(self, path):
    return self.listPath(self.remote_sv,path)

MySMBConnection = type('MySMBConnection',(SMBConnection,),{"listpath_ex":listpath_ex,"remote_sv":'knose'})
conn = MySMBConnection('root', 'p@ssw0rd', 'lytofb', 'root', use_ntlm_v2 = True)
conn.connect('172.28.217.66', 139)
smbresult = smbwalk("/",conn)
for r in smbresult:
    print(r)
# shares = conn.listShares()
# dircontents = conn.listpath_ex('/')
# for dirc in dircontents:
#     print(dirc.filename,dirc.isDirectory)