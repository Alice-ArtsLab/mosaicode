import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
"""
This module contains the AllFileFilter class, HarpiaFileFilter and PNGFileFilter class.
"""


class AllFileFilter(Gtk.FileFilter):

    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("All Archives")
        self.add_pattern("*")


class HarpiaFileFilter(Gtk.FileFilter):

    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Harpia Files")
        self.add_pattern("*.hrp")


class PNGFileFilter(Gtk.FileFilter):

    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Png")
        self.add_pattern("*.png")
