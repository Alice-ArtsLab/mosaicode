from harpia.model.port import Port

class DoublePort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_DOUBLE"
        self.language = "c"
        self.label = "DOUBLE"
        self.color = "#000"
        self.multiple = False
        self.code = "block$sink$_double_i$sink_port$ = block$source$_double_o$source_port$;// DOUBLE conection\n"
