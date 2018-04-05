from os.path import join

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
        self.assertGreater(len(data),expected)

    def test_getDescription(self):
        caption='QSM'
        data = self.dbi.getDescription(caption)
        expected = 0
        self.assertGreater(len(data),expected)