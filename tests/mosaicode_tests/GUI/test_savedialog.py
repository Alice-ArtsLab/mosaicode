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
from mosaicode.GUI.savedialog import SaveDialog

class TestSaveDialog(TestBase):

    def setUp(self):
        self.dialog = SaveDialog(
                    self.create_main_window(),
                    "Test",
                    "*.jpg",
                    None
                    )
        self.dialog = SaveDialog(
                    self.create_main_window(),
                    "Test",
                    None,
                    "Test"
                    )

    def test_run(self):
        t1 = threading.Thread(target=self.dialog.run, args=());
        t1.start()
        sleep(0.2)
        while not self.dialog.is_visible():
            sleep(0.1)
        self.dialog.response(Gtk.ResponseType.OK)
        self.refresh_gui()
        t1.join()
