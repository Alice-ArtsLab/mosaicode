from harpia.model.port import Port

class ImagePort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_IMAGE"
        self.language = "C"
        self.label = "IMG"
        self.color = "#F0F"
        self.multiple = False
        self.code = "block$sink$_img_i$sink_port$ = cvCloneImage(block$source$_img_o$source_port$);// IMG conection\n"
