from harpia.model.port import Port

class Point(Port):

    def __init__(self):
        Port.__init__(self)
        self.language = "c"
        self.label = "POINT"
        self.color = "#0FF"
        self.multiple = False
        self.code = "block$sink$_point_i$sink_port$ = block$source$_point_o$source_port$;// POINT conection\n"
        self.input_codes[1] = "CvPoint block$id$_point_i$port_number$;\n"
        self.output_codes[1] = "CvPoint block$id$_point_o$port_number$;\n"

