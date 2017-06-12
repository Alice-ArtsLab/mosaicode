from unittest import TestCase
from mosaicode.control.preferencescontrol import PreferencesControl
from mosaicode.system import System


class TestPreferencesControl(TestCase):

        # ----------------------------------------------------------------------
    def setUp(self):
        """Do the test basic setup."""
        prop = System.properties
        self.preferences_control = PreferencesControl(prop)

    # ----------------------------------------------------------------------
    def test_load(self):
        self.preferences_control.load()

    # ----------------------------------------------------------------------
    def test_save(self):
        self.x.save()
