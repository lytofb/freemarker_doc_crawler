__author__ = 'root'
import os;
import smblist;
from db_mysql_module import SQLiteWraper;
from optparse import OptionParser;
def getappendfix(f):
    appendfix = '';
    fsplit = f.split(".")
    if len(fsplit)>1:
        appendfix = fsplit[-1]
    return appendfix;

def getsmbwalklist(host,remote_server,user,password,path):
    conn = smblist.mysmbcon_factory(host,remote_server,user,password)
    # conn = smblist.mysmbcon_factory('192.168.1.1','Expansion_Drive(1)','admin','Ab860813')
    smbresult = conn.smbwalk(path)
    return smbresult;

if __name__=="__main__":
    parser = OptionParser();
    parser.add_option("-d", "--dir",dest="dirname",action="store",type="string",
                  help="write report to FILE",default="/home/dev/githubClone/shadowsocks")
    (options, args) = parser.parse_args();
    import pdb;pdb.set_trace();
    db = SQLiteWraper('root','root','127.0.0.1','walkdir');
    dirwalk = os.fwalk(options.dirname);
    smbwalk = getsmbwalklist('192.168.1.1','Expansion_Drive(1)','admin','Ab860813','/qzfs/yy/aido')
    # composewalk = chain(dirwalk,smbwalk);
    for root, dirs, files,rootfd in dirwalk:
        #print(root, dirs, files, rootfd)
        for f in files:
            appendfix = getappendfix(f)
            filehere = os.path.join(root,f)
            dbresult = db.select("select * from filedict where filedir = '"+filehere.replace("'","_")+"'")
            if(len(dbresult)==0):
                insertsql = "insert into filedict (filedir,filename,appendfix) values ('"+filehere.replace("'","_")+"','"+f.replace("'","_")+"','"+appendfix+"')"
                db.execute(insertsql)
    for root, dirs, files in smbwalk:
        #print(root, dirs, files, rootfd)
        for f in files:
            appendfix = getappendfix(f)
            filehere = os.path.join(root,f)
            dbresult = db.select("select * from filedict where filedir = '"+filehere+"'")
            if(len(dbresult)==0):
                insertsql = "insert into filedict (filedir,filename,appendfix) values ('"+filehere+"','"+f+"','"+appendfix+"')"
                db.execute(insertsql)