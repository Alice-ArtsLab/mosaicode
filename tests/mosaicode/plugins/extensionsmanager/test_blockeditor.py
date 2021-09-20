import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import threading
from time import sleep
from tests.mosaicode.test_base import TestBase
from mosaicode.plugins.extensionsmanager.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.blockmanager import BlockManager

class TestBlockEditor(TestBase):

    def setUp(self):
        self.parent = BlockManager(self.create_main_window())
        self.widget = BlockEditor(self.parent, self.create_block())

    def test_run(self):
        self.widget.run()
        self.parent.close()
        self.parent.destroy()

