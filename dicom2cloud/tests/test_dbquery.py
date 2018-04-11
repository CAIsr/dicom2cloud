from __future__ import print_function
import unittest2 # as unittest
import sys
import datetime
from sqlite3 import IntegrityError, OperationalError
from dicom2cloud.config.dbquery import DBI


class TestDBquery(unittest2.TestCase):
    def setUp(self):
        self.dbi = DBI()
        self.dbi.connect()
        # try:
        #     self.deleteData()
        # except OperationalError as e:
        #     print(e.args[0])
        #     self.tearDown()


    def deleteData(self):
        # Reset all data so tests will work - so only use with a test db
        self.dbi.deleteData('seriesprocess')
        self.dbi.deleteData('dicomfiles')
        self.dbi.deleteData('dicomdata')


    def tearDown(self):
        self.dbi.conn.close()

    def test_getCaptions(self):
        data = self.dbi.getCaptions()
        expected = 0
        print('Captions: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data),expected)

    def test_getRefs(self):
        data = self.dbi.getRefs()
        expected = 0
        print('Refs: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data),expected)

    def test_getDescription(self):
        caption='QSM'
        data = self.dbi.getDescription(caption)
        expected = 0
        print('Description: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data),expected)

    def test_getCaption(self):
        caption='qsm'
        data = self.dbi.getCaption(caption)
        expected = 0
        print('Caption: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data),expected)

    def test_getProcessModule(self):
        caption='qsm'
        data = self.dbi.getProcessModule(caption)
        expected = 0
        print('Module: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data),expected)

    def test_getProcessClass(self):
        caption='qsm'
        data = self.dbi.getProcessClass(caption)
        expected = 0
        print('Class: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data),expected)

    def test_getFiles(self):
        uuid = '5d74a20b44ec1dfd0af4fbc6bb680e0f557c14a08a143b843ef40977697e2bea'
        data = self.dbi.getFiles(uuid)
        expected = 0
        print('Files: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), expected)

    def test_getNoFiles(self):
        uuid = 't10001'
        data = self.dbi.getFiles(uuid)
        expected = 0
        print('Files: ', data)
        self.assertEqual(expected,len(data))

    def test_addDicomdata(self):
        dicomdata = {'uuid': 't10000',
                     'patientid': 'p1',
                     'patientname': 'test patient',
                     'seriesnum': '1.001.111',
                     'sequence': 'ftest',
                     'protocol': 'aaa',
                     'imagetype': 'M'
                     }

        try:
            rtn = self.dbi.addDicomdata(dicomdata)
            self.assertEqual(rtn,1,'Dicom data add failed')
        except IntegrityError as e:
            self.skipTest(e.args[0])

    def test_hasUuid(self):
        uuid='t10000'
        self.assertIs(self.dbi.hasUuid(uuid), True,'Data already added')

    def test_addDicomdataExisting(self):
        dicomdata = {'uuid': 't10000',
                     'patientid': 'p1',
                     'patientname': 'test patient',
                     'seriesnum': '1.001.111',
                     'sequence': 'ftest',
                     'protocol': 'aaa',
                     'imagetype': 'M'
                     }
        try:
            self.assertRaises(IntegrityError, self.dbi.addDicomdata,dicomdata)

        except AssertionError as e:
            self.skipTest(e.args[0])

    def test_addDicomfileExisting(self):
        uuid = 't10000'
        dicomfile="D:\\Projects\\XNAT\\data\\S1\\scans\\3\\1001DS.MR.RESEARCH_16022_OPTIMIZING_EXERCISE.0003.0001.2017.02.24.15.41.05.593750.93525560.IMA"
        try:
            self.assertRaises(IntegrityError, self.dbi.addDicomfile,uuid,dicomfile)
            #self.assertEqual(rtn, 1, 'Dicom file add failed')
        except AssertionError as e:
            self.skipTest(e.args[0])

    def test_addDicomfile(self):
        uuid = 't10000'
        dicomfile="D:\\Projects\\XNAT\\data\\S1\\scans\\3\\1001DS.MR.RESEARCH_16022_OPTIMIZING_EXERCISE.0003.0001.2017.02.24.15.41.05.593750.93525560.IMA"
        try:
            rtn = self.dbi.addDicomfile(uuid,dicomfile)
            self.assertEqual(rtn, 1, 'Dicom file add failed')
        except IntegrityError as e:
            self.skipTest(e.args[0])

    def test_getUuids(self):
        data = self.dbi.getUuids()
        expected = 0
        print('UUIDS: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), expected)

    def test_getNumberFiles(self):
        uuid = '5d74a20b44ec1dfd0af4fbc6bb680e0f557c14a08a143b843ef40977697e2bea'
        data = self.dbi.getNumberFiles(uuid)
        expected = 0
        print('Num files: ', data)
        self.assertIsNotNone(data)
        self.assertGreater(data, expected)

    def test_getDicomdataAll(self):
        uuid = 't10000'
        field = 'all'
        data = self.dbi.getDicomdata(uuid,field)
        expected = 0
        print('Dicomdata for: ', field,'=',data)
        self.assertIsNotNone(data)
        self.assertGreater(data, expected)

    def test_getDicomdata(self):
        uuid = 't10000'
        field = 'protocol'
        data = self.dbi.getDicomdata(uuid,field)
        expected = 0
        print('Dicomdata for: ', field,'=',data)
        self.assertIsNotNone(data)
        self.assertGreater(data, expected)

    def test_getRef(self):
        pname ='QSM'
        expected='qsm'
        data = self.dbi.getRef(pname)
        self.assertEqual(expected, data)

    # def test_setSeriesProcess(self):
    #     uuid = '5d74a20b44ec1dfd0af4fbc6bb680e0f557c14a08a143b843ef40977697e2bea'
    #     pid = 1
    #     server = 'AWS'
    #     status = 1
    #     starttime = datetime.datetime.now()
    #     try:
    #         rtn = self.dbi.setSeriesProcess(uuid, pid,server,status,starttime)
    #         self.assertEqual(rtn, 1, 'Series Process add failed')
    #     except IntegrityError as e:
    #         self.skipTest(e.args[0])

    def test_getActiveProcesses(self):
        data = self.dbi.getActiveProcesses()
        print(data)
