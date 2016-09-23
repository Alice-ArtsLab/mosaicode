from harpia.s2idirectory import *

class BlockTemplate:

    #-------------------------------------------------------------------------
    def __init__(self, plugin):
        self.plugin = plugin
        self.myConnections = []
        self.header = ''
        self.declaration = ''
        self.functionCall = ''
        self.connections = ''
        self.dealloc = ''
        self.outDealloc = ''
        self.weight = 1

    #-------------------------------------------------------------------------
    def generate_block_code(self):

        self.header = self.plugin.generate_header()
        self.declaration = self.plugin.generate_vars()
        self.functionCall = self.plugin.generate_function_call()
        self.dealloc = self.plugin.generate_dealloc()
        self.outDealloc = self.plugin.generate_out_dealloc()

        for key in self.plugin.__dict__:
            # Replace all object properties by their values
            value = str(self.plugin.__dict__[key])
            my_key = "$" + key + "$"
            self.declaration = self.declaration.replace(my_key, value)
            self.dealloc = self.dealloc.replace(my_key, value)
            self.outDealloc = self.outDealloc.replace(my_key, value)
            self.functionCall = self.functionCall.replace(my_key, value)

        for x in self.myConnections:
            if x.to_block == '--':
                continue
            if x.type in harpia.s2idirectory.connections:
                self.connections +=  harpia.s2idirectory.connections[x.type]["code"]
            self.connections = self.connections.replace("$to_block$", str(x.to_block))
            self.connections = self.connections.replace("$to_block_in$", str(int(x.to_block_in ) + 1))
            self.connections = self.connections.replace("$from_block$", str(x.from_block))
            self.connections = self.connections.replace("$from_block_out$", str(int (x.from_block_out) + 1))

