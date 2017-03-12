from harpia.model.port import Port

class FloatPort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_WEBAUDIO_FLOAT"
        self.language = "javascript"
        self.label = "FLOAT"
        self.color = "#000"
        self.multiple = True
        self.code = "block_$source$_o$source_port$.push(block_$sink$_i$sink_port$);"
        self.input_vars = "var block_$id$_i$port_number$ = function(value){\n//Put your code here\n};\n"
        self.output_vars = "var block_$id$_o$port_number$ = [];\n"
