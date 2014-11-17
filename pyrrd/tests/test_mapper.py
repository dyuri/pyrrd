from unittest import TestCase

from pyrrd.mapper import RRDMapper
from pyrrd.testing import dump
from pyrrd.util import NaN, XML


class FakeBackend(object):

    def __init__(self, tree):
        self.tree = tree

    def load(self, filename):
        return self.tree


class RRDMapperTestCase(TestCase):

    def setUp(self):
        self.tree = XML(dump.simpleDump01)

    def makeMapper(self):
        rrd = RRDMapper()
        rrd.filename = None
        rrd.backend = FakeBackend(self.tree)
        rrd.map()
        return rrd

    def test_map(self):
        rrd = self.makeMapper()
        self.assertEqual(rrd.version, 3)
        self.assertEqual(rrd.step, 300)
        self.assertEqual(rrd.lastupdate, 920804400)

    def test_mapDS(self):
        rrd = self.makeMapper()
        self.assertEqual(len(rrd.ds), 1)
        ds = rrd.ds[0]
        self.assertEqual(ds.name, "speed")
        self.assertEqual(ds.type, "COUNTER")
        self.assertEqual(ds.minimal_heartbeat, 600)
        self.assertEqual(ds.min, "NaN")
        self.assertEqual(ds.max, "NaN")

    def test_mapRRA(self):
        rrd = self.makeMapper()
        self.assertEqual(len(rrd.rra), 2)
        rra1 = rrd.rra[0]
        self.assertEqual(rra1.cf, "AVERAGE")
        self.assertEqual(rra1.pdp_per_row, 1)
        rra2 = rrd.rra[1]
        self.assertEqual(rra2.cf, "AVERAGE")
        self.assertEqual(rra2.pdp_per_row, 6)

    def test_mapRRAParams(self):
        rrd = self.makeMapper()
        rra1 = rrd.rra[0]
        self.assertEqual(rra1.xff, 0.5)
        rra2 = rrd.rra[1]
        self.assertEqual(rra2.xff, 0.5)

    def test_mapRRACDPPrep(self):
        rrd = self.makeMapper()
        ds1 = rrd.rra[0].ds
        self.assertEqual(len(ds1), 1)
        self.assertEqual(ds1[0].primary_value, 0.0)
        self.assertEqual(ds1[0].secondary_value, 0.0)
        self.assertEqual(str(ds1[0].value), str(NaN()))
        self.assertEqual(ds1[0].unknown_datapoints, 0)
        ds2 = rrd.rra[1].ds
        self.assertEqual(len(ds2), 1)
        self.assertEqual(len(ds1), 1)
        self.assertEqual(ds2[0].primary_value, 0.0)
        self.assertEqual(ds2[0].secondary_value, 0.0)
        self.assertEqual(str(ds2[0].value), str(NaN()))
        self.assertEqual(ds2[0].unknown_datapoints, 0)
