from harpia.model.port import Port

class PointPort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_POINT"
        self.language = "C"
        self.label = "POINT"
        self.color = "#0FF"
        self.multiple = False
        self.code = "block$sink$_point_i$sink_port$ = block$source$_point_o$source_port$;// POINT conection\n"
