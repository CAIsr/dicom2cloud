from __future__ import print_function
import unittest2 as unittest

from dicom2cloud.config.dbquery import DBI


class TestDBquery(unittest.TestCase):
    def setUp(self):
        self.dbi = DBI()
        self.dbi.getconn()

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