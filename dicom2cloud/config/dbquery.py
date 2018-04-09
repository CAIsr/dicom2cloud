from __future__ import print_function
import sqlite3
import pandas
import glob
from os.path import join,abspath, isdir,isfile
from os import access, R_OK, W_OK

class DBI():
    def __init__(self):
        """
        Init for connection to config db
        :param dbfile:
        """
        #locate db in config/
        dbname= 'd2c.db'
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

    def __validstring(self,ref):
        if not isinstance(ref,str) and not isinstance(ref,unicode):
            raise ValueError('Ref is not valid string')
        return ref

    def connect(self):
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
            self.connect()
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
            self.connect()
        self.c.execute("SELECT ref FROM processes")
        qry = self.c.fetchall()
        data = [d[0] for d in qry]
        return data

    def getDescription(self,caption):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT description FROM processes WHERE process=?", (self.__validstring(caption),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getCaption(self,ref):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT process FROM processes WHERE ref=?", (self.__validstring(ref),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessModule(self,ref):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT module FROM processes WHERE ref=?", (self.__validstring(ref),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessClass(self,ref):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT class FROM processes WHERE ref=?", (self.__validstring(ref),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getFiles(self,uuid):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT filename FROM dicomfiles WHERE uuid=?", (self.__validstring(uuid),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def addDicomdata(self,dicomdata):
        """
        Load new dicomdata for series
        :param dicomdata: dict with dicomdata fields
        :return:
        """
        #'patientid', 'patientname', 'seriesnum', 'sequence', 'protocol', 'imagetype'
        if self.c is None:
            self.connect()
        if isinstance(dicomdata,dict):
            self.c.execute("INSERT INTO dicomdata (uuid,patientid,patientname,seriesnum,sequence,protocol,imagetype) VALUES (?,?,?,?,?,?,?)", (dicomdata['uuid'],dicomdata['patientid'], dicomdata['patientname'], dicomdata['seriesnum'], dicomdata['sequence'], dicomdata['protocol'], dicomdata['imagetype']))
            self.conn.commit()
            print('Dicomdata loaded: ', dicomdata)
            rtn = 1
        else:
            self.conn.rollback()
            print('Dicomdata not dict')
            rtn = 0
        return rtn
            
    def addDicomfile(self,uuid,dicomfile):
        if self.c is None:
            self.connect()
        if self.__validstring(uuid) and isfile(dicomfile):
            self.c.execute("INSERT INTO dicomfiles (filename,uuid) VALUES(?,?)", (dicomfile,uuid))
            self.conn.commit()
            print('Dicomfile loaded: ', dicomfile)
            rtn = 1
        else:
            self.conn.rollback()
            print('Dicomfile not loaded')
            rtn = 0
        return rtn
            
    def getUuids(self):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT uuid FROM dicomdata")
        qry = self.c.fetchall()
        data = [d[0] for d in qry]
        return data

    def getNumberFiles(self,uuid):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT COUNT(*) FROM dicomfiles WHERE uuid=?", (self.__validstring(uuid),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getDicomdata(self,uuid,fieldname):
        if self.c is None:
            self.connect()
        if not self.__validstring(fieldname) or fieldname == 'all':
            self.c.execute("SELECT uuid,patientid,patientname,seriesnum,sequence,protocol,imagetype FROM dicomdata WHERE uuid=?", (self.__validstring(uuid),))
            data = self.c.fetchall()
            if data is not None:
                data = {'uuid': data[0][0],
                           'patientid': data[0][1],
                           'patientname': data[0][2],
                           'seriesnum': data[0][3],
                           'sequence': data[0][4],
                           'protocol': data[0][5],
                           'imagetype': data[0][6]}
        else:
            self.c.execute("SELECT " + fieldname + " FROM dicomdata WHERE uuid=?", (self.__validstring(uuid),))
            data = self.c.fetchall()
            if data is not None:
                data = data[0][0]
        return data
        

#############################################################################
if __name__ == "__main__":
    import os

    print(os.getcwd())

    configdb = join('..', 'config', 'd2c.db')
    if access(configdb,R_OK):
        dbi = DBI()
        dbi.connect()
        data = dbi.getCaptions()
        print(data)

    else:
        raise IOError("cannot access db")

