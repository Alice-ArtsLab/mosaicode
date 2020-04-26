import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from time import sleep
import threading
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.messagedialog import MessageDialog

class TestMessageDialog(TestBase):

    def setUp(self):
        self.dialog = MessageDialog(
                    "Test Message Dialog",
                    "Test",
                    self.create_main_window()
                    )

    def test_constructor(self):
        pass

