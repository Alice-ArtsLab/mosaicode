from mosaicode.model.port import Port

class Float(Port):

    def __init__(self):
        Port.__init__(self)
        self.language = "javascript"
        self.label = "FLOAT"
        self.color = "#000"
        self.multiple = True
        self.code = "block_$source$_o$source_port$.push(block_$sink$_i$sink_port$);\n"
        self.input_codes[1] = "var block_$id$_i$port_number$ = function(value){\n//Put your code here\n};\n"
        self.output_codes[1] = "var block_$id$_o$port_number$ = [];\nfunction update_block_$id$_o$port_number$(value){\nfor (var i = 0; i &lt; block_$id$_o$port_number$.length ; i++){\n        block_$id$_o$port_number$[i](value);\n    }\n}\n"
        self.var_name = "block_$id$_$conn_type$$port_number$"
