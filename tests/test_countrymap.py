# -*- coding: utf-8 -*-

from unittest import TestCase
import unittest

import sys
sys.path.append('..')

import tempfile
from countrymap import Map


#~ from nose.tools import assert_raises

#~ import matplotlib.pyplot as plt

class TestCountrymap(unittest.TestCase):

    def setUp(self):
        pass

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




if __name__ == '__main__':
    unittest.main()
