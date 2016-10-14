from unittest import TestCase
from harpia.control.preferencescontrol import PreferencesControl
from harpia.system import System

class TestPreferencesControl(TestCase):

	# ----------------------------------------------------------------------
    def setUp(self):
        """Do the test basic setup."""
        prop = System.properties
        self.x = PreferencesControl(prop)

    # ----------------------------------------------------------------------
    def test_load(self):
        self.x.load()

    # ----------------------------------------------------------------------
    def test_save(self):
    	self.x.save()