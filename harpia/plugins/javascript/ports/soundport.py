from harpia.model.port import Port

class SoundPort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_WEBAUDIO_SOUND"
        self.language = "javascript"
        self.label = "SOUND"
        self.color = "#F00"
        self.multiple = True
        self.code = "block_$source$.connect(block_$sink$_i$sink_port$);"
        self.input_codes[1] = "var block_$id$_i$port_number$ = null;\n"
        self.output_codes[1] = "var block_$id$_o$port_number$ = null; // It must be an object with a connect method\n"
