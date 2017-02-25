from harpia.model.port import Port

class IntPort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_INT"
        self.language = "C"
        self.label = "INT"
        self.color = "#F00"
        self.multiple = False
        self.code = "block$sink$_int_i$sink_port$ = block$source$_int_o$source_port$;// INT conection\n"
