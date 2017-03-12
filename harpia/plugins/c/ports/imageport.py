from harpia.model.port import Port

class ImagePort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_IMAGE"
        self.language = "c"
        self.label = "IMG"
        self.color = "#F0F"
        self.multiple = False
        self.code = "block$sink$_img_i$sink_port$ = cvCloneImage(block$source$_img_o$source_port$);// IMG conection\n"
        self.input_vars = "IplImage * block$id$_img_i$port_number$ = NULL;\n"
        self.output_vars = "IplImage * block$id$_img_o$port_number$ = NULL;\n"
        self.input_dealloc = "cvReleaseImage(&block$id$_img_i$port_number$);\n"
        self.output_dealloc = "cvReleaseImage(&block$id$_img_o$port_number$);\n"

