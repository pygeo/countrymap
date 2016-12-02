# -*- coding: utf-8 -*-

from unittest import TestCase
import unittest

import sys
sys.path.append('..')

import tempfile
from countrymap import Map

import os



#~ from nose.tools import assert_raises

#~ import matplotlib.pyplot as plt

class TestCountrymap(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        #~ self.del_file('TM_WORLD_BORDERS-0.3.prj')
        #~ self.del_file('TM_WORLD_BORDERS-0.3.shp')

    def del_file(self, f):
        if os.path.exists(f):
            os.remove(f)

    def test_init(self):
        M1 = Map(region='europe')
        self.assertEqual(M1.label, 'europe')

        lon1 = -20.
        lon2=20.
        lat1=0.
        lat2=50.
        M2 = Map(region={'test': {'lon1':lon1,'lon2':lon2,'lat1':lat1,'lat2':lat2}})

        self.assertEqual(M2.x1,lon1)
        self.assertEqual(M2.x2,lon2)
        self.assertEqual(M2.y1,lat1)
        self.assertEqual(M2.y2,lat2)
        self.assertEqual(M2.label, 'test')

    #~ def test_getdefaultshape(self):
        #~ M = Map(region='europe')
        #~ M._download_shape()

    def test_readshape(self):
        M = Map(region='europe')
        M.read_shape()

    def test_draw_basic(self):
        M = Map(region='europe')
        M.draw()

    def test_draw_detail(self):
        M = Map(region='europe')
        M.read_shape()
        M.draw()
        M.draw_details(['France', 'Germany','United Kingdom','Netherlands', 'Estonia', 'Spain'], color='tomato')

    def test_getnames(self):
        M = Map(region='europe')
        M.read_shape()
        res = M.get_country_names()
        print res
        self.assertTrue('Germany' in res)

if __name__ == '__main__':
    unittest.main()
