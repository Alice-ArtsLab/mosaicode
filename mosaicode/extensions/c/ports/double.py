from mosaicode.model.port import Port

class Double(Port):

    def __init__(self):
        Port.__init__(self)
        self.language = "c"
        self.label = "DOUBLE"
        self.color = "#000"
        self.multiple = False
        self.code = "block$sink$_double_i$sink_port$ = block$source$_double_o$source_port$;// DOUBLE conection\n"
        self.input_codes[1] = "double block$id$_double_i$port_number$;\n"
        self.output_codes[1] = "double block$id$_double_o$port_number$;\n"
