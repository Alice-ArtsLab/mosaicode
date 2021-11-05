import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from time import sleep
import threading
from tests.mosaicode.test_base import TestBase
from mosaicode.GUI.messagedialog import MessageDialog

class TestMessageDialog(TestBase):

    def test_constructor(self):
        self.dialog = MessageDialog(
                    "Test Message Dialog",
                    "Test",
                    self.create_main_window()
                    )
        t1 = threading.Thread(target=self.dialog.run, args=());
        t1.start()
        sleep(1)
        self.dialog.response(Gtk.ResponseType.OK)
        self.refresh_gui()
        t1.join()
        self.dialog.close()
        self.dialog.destroy()

