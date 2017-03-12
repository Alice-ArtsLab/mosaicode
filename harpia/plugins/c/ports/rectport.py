from harpia.model.port import Port

class RectPort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_RECT"
        self.language = "c"
        self.label = "RCT"
        self.color = "#00F"
        self.multiple = False
        self.code = "block$sink$_rect_i$sink_port$ = block$source$_rect_o$source_port$;// RECT conection\n"
        self.input_vars = "CvRect block$id$_rect_i$port_number$ = cvRect( 0, 0, 1, 1);\n"
        self.output_vars = "CvRect block$id$_rect_o$port_number$ = cvRect( 0, 0, 1, 1);\n"
