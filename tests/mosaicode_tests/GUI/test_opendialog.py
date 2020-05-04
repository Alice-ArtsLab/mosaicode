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
from mosaicode.GUI.opendialog import OpenDialog

class TestOpenDialog(TestBase):

    def test_run(self):
        self.dialog = OpenDialog("Test", self.create_main_window(), "*.jpg", ".")
        self.dialog = OpenDialog("Test", self.create_main_window(), None, None)
        self.dialog = OpenDialog("Test", self.create_main_window(), "*.mscd", None)
        t1 = threading.Thread(target=self.dialog.run, args=());
        t1.start()
        sleep(1)
        self.dialog.select_filename("LICENSE")
        self.dialog.response(Gtk.ResponseType.OK)
        self.refresh_gui()
        t1.join()
        self.dialog.close()
        self.dialog.destroy()
