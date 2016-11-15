import os
from ftplib import FTP;

class ftp_walker(object):
    def __init__(self, connection, root):
        self.connection = connection
        self.root = root

    def listdir(self, _path):
        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print ("the current path is : ", self.connection.pwd(), exp.__str__(), _path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name, size = info[0], info[-1], info[4]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

    def _iwalk(self, path,dirname):
        dirs, nondirs = self.listdir(dirname)
        yield path, dirs, nondirs
        originalpath = path
        for name in dirs:
            path = os.path.join(originalpath, name)
            yield from self._iwalk(path,name)
        self.connection.cwd("..")

    def iwalk(self,path):
        yield from self._iwalk(path,path)

if __name__=="__main__":
    ftp = FTP("172.28.217.66","test","123456")
    ftpwalker = ftp_walker(ftp,"/");
    a = ftpwalker.iwalk("/qgy")
    for aa in a:
        print(aa)