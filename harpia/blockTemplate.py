from harpia.s2idirectory import *

class BlockTemplate:

    #-------------------------------------------------------------------------
    def __init__(self, plugin):
        self.plugin = plugin
        self.myConnections = []
        self.header = ''
        self.imagesIO = ''
        self.functionCall = ''
        self.dealloc = ''
        self.outDealloc = ''
        self.weight = 1

    #-------------------------------------------------------------------------
    def generate_block_code(self):

        self.plugin.generate(self)

        for key in self.plugin.__dict__:
            # Replace all object properties by their values
            value = str(self.plugin.__dict__[key])
            my_key = "$" + key + "$"
            self.imagesIO = self.imagesIO.replace(my_key, value)
            self.dealloc = self.dealloc.replace(my_key, value)
            self.outDealloc = self.outDealloc.replace(my_key, value)
            self.functionCall = self.functionCall.replace(my_key, value)

        for x in self.myConnections:
            if x.to_block == '--':
                continue
            if x.type in harpia.s2idirectory.connections:
                self.functionCall +=  harpia.s2idirectory.connections[x.type]["code"]
            self.functionCall = self.functionCall.replace("$to_block$", str(x.to_block))
            self.functionCall = self.functionCall.replace("$to_block_in$", str(int(x.to_block_in ) + 1))
            self.functionCall = self.functionCall.replace("$from_block$", str(x.from_block))
            self.functionCall = self.functionCall.replace("$from_block_out$", str(int (x.from_block_out) + 1))

