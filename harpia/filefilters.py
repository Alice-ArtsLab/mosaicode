import gtk

class AllFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("All Archives")
        self.add_pattern("*")

class HarpiaFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("Harpia Files")
        self.add_pattern("*.hrp")

class CCOdeFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("C Code (*.c)")
        self.add_pattern("*.c")

class PNGFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("Png")
        self.add_pattern("*.png")

class JPGFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("JPG")
        self.add_pattern("*.jpg")

class XMLImageFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("XML Image")
        self.add_pattern("*.xml")


class VideoFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("Videos")
        self.add_mime_type("*.mpeg")
        self.add_mime_type("*.avi")
        self.add_mime_type("*.mpg")
        self.add_mime_type("*.wmv")

class ImageFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("Images")
        self.add_mime_type("*.jpg")
        self.add_mime_type("*.bmp")
        self.add_mime_type("*.png")
        self.add_mime_type("*.gif")

class AVIFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)
        self.set_name("AVI Videos")
        self.add_mime_type("*.avi")

