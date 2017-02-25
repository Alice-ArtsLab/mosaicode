from harpia.model.port import Port

class CharPort(Port):

    def __init__(self):
        Port.__init__(self)
        self.type = "HRP_WEBAUDIO_CHAR"
        self.language = "javascript"
        self.label = "CHAR"
        self.color = "#00F"
        self.multiple = True
        self.code = "block_$source$_o$source_port$.push(block_$sink$_i[$sink_port$]);"
