import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk

from tests.mosaicode.test_base import TestBase
from mosaicode.GUI.buttonbar import ButtonBar

class TestButtonBar(TestBase):

    def setUp(self):
        self.buttonbar = ButtonBar()

    def test_add_button(self):
        self.buttonbar.add_button({
                    "icone":Gtk.STOCK_NEW,
                    "action": self.test_add_button,
                    "data":None
                    })
