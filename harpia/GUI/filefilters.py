import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk

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

class CCOdeFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("C Code (*.c)")
        self.add_pattern("*.c")

class PNGFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Png")
        self.add_pattern("*.png")

class JPGFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("JPG")
        self.add_pattern("*.jpg")

class XMLImageFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("XML Image")
        self.add_pattern("*.xml")


class VideoFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Videos")
        self.add_mime_type("*.mpeg")
        self.add_mime_type("*.avi")
        self.add_mime_type("*.mpg")
        self.add_mime_type("*.wmv")

class ImageFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Images")
        self.add_mime_type("*.jpg")
        self.add_mime_type("*.bmp")
        self.add_mime_type("*.png")
        self.add_mime_type("*.gif")

class AVIFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("AVI Videos")
        self.add_mime_type("*.avi")

