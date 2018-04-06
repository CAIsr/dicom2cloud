from __future__ import print_function
import sqlite3
import pandas
import glob
from os.path import join,abspath
from os import access, R_OK, W_OK

class DBI():
    def __init__(self):
        """
        Init for connection to config db
        :param dbfile:
        """
        #locate db in config/config.db
        dbname= 'config.db'
        cpath1 = join('config',dbname)
        cpath2 = join('..',cpath1)
        if access(dbname,R_OK):
            self.dbfile = abspath(dbname)
        elif access(cpath1, R_OK):
            self.dbfile = abspath(cpath1)
        elif access(cpath2, R_OK):
            self.dbfile = abspath(cpath2)
        else:
            raise IOError("Unable to locate Config db")

        self.c = None

    def getconn(self):
        self.conn = sqlite3.connect(self.dbfile)
        self.c = self.conn.cursor()

    def closeconn(self):
        self.conn.close()

    def getCaptions(self):
        """
        Get dict of config
        :return: name=value pairs or None
        """
        if self.c is None:
            self.getconn()
        self.c.execute("SELECT process FROM processes")
        qry = self.c.fetchall()
        data = [d[0] for d in qry]
        return data

    def getRefs(self):
        """
        Get dict of config
        :return: name=value pairs or None
        """
        if self.c is None:
            self.getconn()
        self.c.execute("SELECT ref FROM processes")
        qry = self.c.fetchall()
        data = [d[0] for d in qry]
        return data

    def getDescription(self,caption):
        if self.c is None:
            self.getconn()
        if not isinstance(caption,str):
            raise ValueError('Caption is invalid')
        self.c.execute("SELECT description FROM processes WHERE process=?", (caption,))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getCaption(self,ref):
        if self.c is None:
            self.getconn()
        if not isinstance(ref,str):
            raise ValueError('Ref is invalid')
        self.c.execute("SELECT process FROM processes WHERE ref=?", (ref,))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessModule(self,ref):
        if self.c is None:
            self.getconn()
        if not isinstance(ref,str):
            raise ValueError('Ref is invalid')
        self.c.execute("SELECT module FROM processes WHERE ref=?", (ref,))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessClass(self,ref):
        if self.c is None:
            self.getconn()
        if not isinstance(ref,str):
            raise ValueError('Ref is invalid')
        self.c.execute("SELECT class FROM processes WHERE ref=?", (ref,))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data


#############################################################################
if __name__ == "__main__":
    import os

    print(os.getcwd())

    configdb = join('..', 'config', 'config.db')
    if access(configdb,R_OK):
        dbi = DBI()
        dbi.getconn()
        data = dbi.getCaptions()
        print(data)

    else:
        raise IOError("cannot access db")

