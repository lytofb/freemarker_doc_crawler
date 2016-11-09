__author__ = 'root'
import os;
from db_mysql_module import SQLiteWraper;
from optparse import OptionParser;
def getappendfix(f):
    appendfix = '';
    fsplit = f.split(".")
    if len(fsplit)>1:
        appendfix = fsplit[-1]
    return appendfix;

if __name__=="__main__":
    parser = OptionParser();
    parser.add_option("-d", "--dir",dest="dirname",action="store",type="string",
                  help="write report to FILE",default="/home/dev/githubClone/shadowsocks")
    (options, args) = parser.parse_args();
    import pdb;pdb.set_trace();
    db = SQLiteWraper();
    for root, dirs, files, rootfd in os.fwalk(options.dirname):
        #print(root, dirs, files, rootfd)
        for f in files:
            appendfix = getappendfix(f)
            filehere = os.path.join(root,f)
            insertsql = "insert into filedict (filedir,filename,appendfix) values ('"+filehere+"','"+f+"','"+appendfix+"')"
            db.execute(insertsql)