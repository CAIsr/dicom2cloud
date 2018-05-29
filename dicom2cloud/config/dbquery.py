from __future__ import print_function

import datetime
import shutil
import sqlite3
from os import access, R_OK, mkdir
from os.path import join, isfile, expanduser

from dicom2cloud.controller_utils import findResourceDir


class DBI():
    def __init__(self, test=False):
        """
        Init for connection to config db
        :param dbfile:
        """
        # locate db in config/
        self.resourcesdir = findResourceDir()

        if test:
            dbname = 'd2c-test.db'
        else:
            dbname = 'd2c.db'
        self.dbfile = self.getConfigdb(dbname)
        self.c = None

    def getConfigdb(self, dbname):
        # Save config db to user's home dir or else will be overwritten with updates
        self.userconfigdir = join(expanduser('~'), '.d2c')
        # dbname = 'autoconfig.db'
        if not access(self.userconfigdir, R_OK):
            mkdir(self.userconfigdir)
        configdb = join(self.userconfigdir, dbname)
        if not access(configdb, R_OK):
            defaultdb = join(self.resourcesdir, dbname)
            shutil.copy(defaultdb, configdb)
        print('Database: ', configdb)
        return configdb

    def validstring(self, ref):
        if not isinstance(ref, str) and not isinstance(ref, unicode):
            raise ValueError('Ref is not valid string')
        return ref

    def connect(self):
        self.conn = sqlite3.connect(self.dbfile)
        self.c = self.conn.cursor()

    def closeconn(self):
        self.conn.close()

    def deleteData(self, table):
        """
        TODO: This is causing database locking ??
        :param table:
        :return:
        """
        if self.c is None:
            self.connect()
        self.c.execute('DELETE FROM `' + table + '`')
        print('Table data deleted: ', table)
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

    def getDescription(self, caption):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT description FROM processes WHERE process=?", (self.validstring(caption),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getCaption(self, ref):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT process FROM processes WHERE ref=?", (self.validstring(ref),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessModule(self, ref):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT module FROM processes WHERE ref=?", (self.validstring(ref),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessClass(self, ref):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT class FROM processes WHERE ref=?", (self.validstring(ref),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getFiles(self, uuid):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT filename FROM dicomfiles WHERE uuid=?", (self.validstring(uuid),))
        data = self.c.fetchall()
        if data is not None:
            data = [d[0] for d in data]
        return data

    def addDicomdata(self, dicomdata):
        """
        Load new dicomdata for series
        :param dicomdata: dict with dicomdata fields
        :return:
        """
        # 'patientid', 'patientname', 'seriesnum', 'sequence', 'protocol', 'imagetype'
        if self.c is None:
            self.connect()
        if isinstance(dicomdata, dict):
            self.c.execute(
                "INSERT INTO dicomdata (uuid,patientid,patientname,seriesnum,sequence,protocol,imagetype) VALUES (?,?,?,?,?,?,?)",
                (dicomdata['uuid'], dicomdata['patientid'], dicomdata['patientname'], dicomdata['seriesnum'],
                 dicomdata['sequence'], dicomdata['protocol'], dicomdata['imagetype']))
            self.conn.commit()
            print('Dicomdata loaded: ', dicomdata)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Dicomdata')
            rtn = 0
        return rtn

    def addDicomfile(self, uuid, dicomfile):
        if self.c is None:
            self.connect()
        if self.validstring(uuid) and isfile(dicomfile):
            self.c.execute("INSERT INTO dicomfiles (filename,uuid) VALUES(?,?)", (dicomfile, uuid))
            self.conn.commit()
            print('Dicomfile loaded: ', dicomfile)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Dicomfile')
            rtn = 0
        return rtn

    def hasFile(self, dicomfile):
        rtn = False
        if self.c is None:
            self.connect()
        self.c.execute("SELECT COUNT(*) FROM dicomfiles WHERE filename=?", (dicomfile,))
        data = self.c.fetchone()
        if data is not None and data[0] > 0:
            rtn = True
        return rtn

    def getUuids(self):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT uuid FROM dicomdata")
        qry = self.c.fetchall()
        data = [d[0] for d in qry]
        return data

    def getNewUuids(self):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT uuid FROM dicomdata")
        qry = self.c.fetchall()
        self.c.execute("SELECT uuid FROM seriesprocess")
        sps = self.c.fetchall()
        data = [d[0] for d in qry if d not in sps]
        return data

    def hasUuid(self, uuid):
        rtn = False
        if self.c is None:
            self.connect()
        self.c.execute("SELECT COUNT(*) FROM dicomdata WHERE uuid=?", (self.validstring(uuid),))
        data = self.c.fetchone()
        if data is not None and data[0] > 0:
            rtn = True
        return rtn

    def getNumberFiles(self, uuid):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT COUNT(*) FROM dicomfiles WHERE uuid=?", (self.validstring(uuid),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getDicomdata(self, uuid, fieldname):
        if self.c is None:
            self.connect()
        if not self.validstring(fieldname) or fieldname == 'all':
            self.c.execute(
                "SELECT uuid,patientid,patientname,seriesnum,sequence,protocol,imagetype FROM dicomdata WHERE uuid=?",
                (self.validstring(uuid),))
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
            self.c.execute("SELECT " + fieldname + " FROM dicomdata WHERE uuid=?", (self.validstring(uuid),))
            data = self.c.fetchall()
            if data is not None:
                data = data[0][0]
        return data

    def getRef(self, processname):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT ref FROM processes WHERE process=?", (self.validstring(processname),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def setSeriesProcess(self, uuid, pid, server, status, starttime, outputdir):
        if self.c is None:
            self.connect()
        if self.validstring(uuid) and self.validstring(server):
            self.c.execute(
                "INSERT INTO seriesprocess (uuid,processid,server,status,starttime,outputdir) VALUES(?,?,?,?,?,?)",
                (uuid, pid, server, status, starttime, outputdir))
            self.conn.commit()
            print('Seriesprocess loaded: ', uuid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Seriesprocess')
            rtn = 0
        return rtn

    def setSessionProcess(self, uuid, pid, server, status, starttime, outputdir):
        if self.c is None:
            self.connect()
        if self.validstring(uuid) and self.validstring(server):
            self.c.execute(
                "INSERT INTO sessionprocess (sessionid,processid,server,status,starttime,outputdir) VALUES(?,?,?,?,?,?)",
                (uuid, pid, server, status, starttime, outputdir))
            self.conn.commit()
            print('Sessionprocess loaded: ', uuid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Sessionprocess')
            rtn = 0
        return rtn

    def setSessionSeries(self, sessionid, seriesid, timestamp):
        if self.c is None:
            self.connect()
        if self.validstring(sessionid) and self.validstring(seriesid):
            self.c.execute(
                "INSERT INTO sessionseries (sessionid, seriesid, timestamp) VALUES(?,?,?)",
                (sessionid, seriesid, timestamp))
            self.conn.commit()
            print('Sessionseries loaded: ', sessionid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Sessionseries')
            rtn = 0
        return rtn

    def getSessionFiles(self,sessionid):
        if self.c is None:
            self.connect()
        if self.validstring(sessionid):
            self.c.execute("SELECT d.filename FROM dicomfiles as d, sessionseries as s WHERE d.uuid=s.seriesid AND s.sessionid=?", (sessionid,))
            data = self.c.fetchall()
            if data is not None:
                data = [d[0] for d in data]
            return data


    def getProcessId(self, processname):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT id FROM processes WHERE process=?", (self.validstring(processname),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessField(self, fieldname, processname):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT " + fieldname + " FROM processes WHERE process=?", (self.validstring(processname),))
        data = self.c.fetchone()
        if data is not None:
            data = data[0]
        return data

    def getProcessData(self):
        if self.c is None:
            self.connect()
        self.c.execute("SELECT * FROM processes")
        data = self.c.fetchall()
        # if data is not None:
        #     data = {'id': data[0][0],
        #             'ref': data[0][1],
        #             'process': data[0][2],
        #             'description': data[0][3],
        #             'module': data[0][4],
        #             'class': data[0][5],
        #             'container': data[0][6],
        #             'containerinputdir': data[0][7],
        #             'containeroutputdir': data[0][8],
        #             'outputfile': data[0][9],
        #             'filename': data[0][10],
        #             }
        return data

    def setProcessData(self, datalist):
        if self.c is None:
            self.connect()
        try:
            if datalist is not None and len(datalist) > 0:
                self.c.execute('DELETE FROM processes')
                self.c.executemany("INSERT INTO processes VALUES(?,?,?,?,?,?,?,?,?,?,?)",datalist)
                self.conn.commit()
                print('Process data saved')
        except:
            self.conn.rollback()
            print('Invalid data for Process')
        return len(datalist)

    def getActiveProcesses(self):
        if self.c is None:
            self.connect()
        self.c.execute(
            "SELECT sp.sessionid,p.process,sp.server,sp.status,sp.starttime,sp.endtime, sp.outputdir FROM sessionprocess as sp, processes as p WHERE sp.processid = p.id")
        data = self.c.fetchall()
        return data

    def setSeriesProcessInprogress(self, uuid):
        if self.c is None:
            self.connect()
        if self.validstring(uuid):
            status = 2  # in progress - correlate with lookup status
            self.c.execute("UPDATE seriesprocess SET status=? WHERE uuid=?", (status, uuid))
            self.conn.commit()
            print('Seriesprocess updated: ', uuid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Seriesprocess')
            rtn = 0
        return rtn

    def setSeriesProcessFinished(self, uuid):
        if self.c is None:
            self.connect()
        if self.validstring(uuid):
            status = 3  # Finished - correlate with lookup status
            endtime = datetime.datetime.now()
            self.c.execute("UPDATE seriesprocess SET status=?, endtime=? WHERE uuid=?", (status, endtime, uuid))
            self.conn.commit()
            print('Seriesprocess loaded: ', uuid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Seriesprocess')
            rtn = 0
        return rtn

    def setSessionProcessInprogress(self, sessionid):
        if self.c is None:
            self.connect()
        if self.validstring(sessionid):
            status = 2  # in progress - correlate with lookup status
            self.c.execute("UPDATE sessionprocess SET status=? WHERE sessionid=?", (status, sessionid))
            self.conn.commit()
            print('Sessionprocess updated: ', sessionid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Sessionprocess')
            rtn = 0
        return rtn

    def setSessionProcessFinished(self, sessionid):
        if self.c is None:
            self.connect()
        if self.validstring(sessionid):
            status = 3  # Finished - correlate with lookup status
            endtime = datetime.datetime.now()
            self.c.execute("UPDATE sessionprocess SET status=?, endtime=? WHERE sessionid=?", (status, endtime, sessionid))
            self.conn.commit()
            print('Sessionprocess loaded: ', sessionid)
            rtn = 1
        else:
            self.conn.rollback()
            print('Invalid data for Sessionprocess')
            rtn = 0
        return rtn

    def deleteSeriesData(self, uuid):
        """
        Remove all data from database for a series
        :param uuid:
        :return:
        """
        rtn = False
        if self.c is None:
            self.connect()
        if self.validstring(uuid):
            self.c.execute('DELETE FROM dicomdata WHERE uuid=?', (uuid,))  # cascade NOT working?
            self.c.execute('DELETE FROM dicomfiles WHERE uuid=?', (uuid,))
            self.c.execute('DELETE FROM seriesprocess WHERE uuid=?', (uuid,))
            self.conn.commit()
            print('Series data deleted: ', uuid)
            rtn = True
        return rtn

    def deleteSessionData(self, sessionid):
        """
        Remove all data from database for a session
        :param uuid:
        :return:
        """
        rtn = False
        if self.c is None:
            self.connect()
        if self.validstring(sessionid):
            seriesids = self.getSeriesFromSession(sessionid)
            for uuid in seriesids:
                self.c.execute('DELETE FROM dicomdata WHERE uuid=?', (uuid,))  # cascade NOT working?
                self.c.execute('DELETE FROM dicomfiles WHERE uuid=?', (uuid,))
            self.c.execute('DELETE FROM sessionseries WHERE sessionid=?', (sessionid,))
            self.c.execute('DELETE FROM sessionprocess WHERE sessionid=?', (sessionid,))
            self.conn.commit()
            print('Series data deleted: ', sessionid)
            rtn = True
        return rtn

    def getSeriesFromSession(self,sessionid):
        data = None
        if self.c is None:
            self.connect()
        if self.validstring(sessionid):
            self.c.execute("SELECT seriesid FROM sessionseries")
            data = self.c.fetchall()
            if data is not None:
                data = [d[0] for d in data]
        return data

    def getServerConfig(self):
        """
        Get server config name-value-description as dict
        :return: dict[name] = [val,desc]
        """
        if self.c is None:
            self.connect()
        config = {}
        self.c.execute("SELECT * FROM serverconfig")
        for k, val, desc in self.c.fetchall():
            config[k] = [val, desc]
        if len(config) <= 0:
            config = None
        return config

    def addServerConfig(self,idlist):
        """
        Save changes to Incorrect and Correct IDs - all are replaced
        :param idlist:
        :return: number of ids added (total)
        """
        cnt = 0
        if self.c is None:
            self.connect()
        if len(idlist) > 0:
            #remove entries
            cnt = self.c.execute("DELETE FROM serverconfig").rowcount
            print('Deleted rows: ', cnt)
            cnt = self.c.executemany('INSERT INTO serverconfig VALUES(?,?,?)', idlist).rowcount
            print('Inserted rows: ', cnt)
            self.conn.commit()

        return cnt

    def getServerConfigByName(self,sid):
        """
        Get correct ID if it exists in lookup table
        :param sid:
        :return:
        """
        if self.c is None:
            self.connect()
        self.c.execute('SELECT value FROM serverconfig WHERE Name=?',(sid,))
        data = self.c.fetchone()
        if data is not None:
            cid = data[0]
        else:
            cid = None
        return cid


#############################################################################
if __name__ == "__main__":
    import os

    print(os.getcwd())
    try:
        dbi = DBI()
        dbi.connect()
        data = dbi.getCaptions()
        print(data)
        # Delete
        # uuid = '5d74a20b44ec1dfd0af4fbc6bb680e0f557c14a08a143b843ef40977697e2bea'
        # dbi.deleteSeriesData(uuid)
        ds = dbi.getProcessData()
        print(ds)

    except:
        raise IOError("cannot access db")
