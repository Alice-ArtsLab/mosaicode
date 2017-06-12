from mosaicode.model.port import Port

class Char(Port):

    def __init__(self):
        Port.__init__(self)
        self.language = "javascript"
        self.label = "CHAR"
        self.color = "#00F"
        self.multiple = True
        self.code = "block_$source$_o$source_port$.push(block_$sink$_i$sink_port$);"
        self.input_codes[1] = "var block_$id$_i$port_number$ = function(value){\n//Put your code here\n};\n"
        self.output_codes[1] = "var block_$id$_o$port_number$ = [];\n"
        self.var_name = "block_$id$_$conn_type$$port_number$"
