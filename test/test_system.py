from unittest import TestCase
from mosaicode.system import System


class Log(object):

    def log(self, msg):
        print msg.encode('ascii', 'ignore')


class TestSystem(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        System()

    def test_set_log(self):
        System.set_log(Log())

    def test_log(self):
        System.log("Hello World")
