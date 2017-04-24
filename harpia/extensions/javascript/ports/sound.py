from harpia.model.port import Port

class Sound(Port):

    def __init__(self):
        Port.__init__(self)
        self.language = "javascript"
        self.label = "SOUND"
        self.color = "#F00"
        self.multiple = True
        self.code = "block_$source$.connect(block_$sink$_i$sink_port$);"
        self.input_codes[1] = "var block_$id$_i$port_number$ = null;\n"
        self.output_codes[1] = "var block_$id$_o$port_number$ = null; // It must be an object with a connect method\n"
        self.var_name = "block_$id$_$conn_type$$port_number$"
