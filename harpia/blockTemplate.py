import s2idirectory

class BlockTemplate:
    header = ''
    imagesIO = ''
    functionCall = ''
    dealloc = ''
    outDealloc = ''
    myConnections = []
    weight = 1

    #-------------------------------------------------------------------------
    def __init__(self, plugin):
        self.plugin = plugin
        self.myConnections = []

    #-------------------------------------------------------------------------
    def generate_block_code(self):

        self.plugin.generate(self)

        self.imagesIO = self.imagesIO.replace("$$", str(self.plugin.id))
        self.dealloc = self.dealloc.replace("$$", str(self.plugin.id))
        self.outDealloc = self.outDealloc.replace("$$", str(self.plugin.id))
        self.functionCall = self.functionCall.replace("$$", str(self.plugin.id))

        for key in self.plugin.__dict__:
            value = str(self.plugin.__dict__[key])
            my_key = "$" + key + "$"
            self.imagesIO = self.imagesIO.replace(my_key, value)
            self.dealloc = self.dealloc.replace(my_key, value)
            self.outDealloc = self.outDealloc.replace(my_key, value)
            self.functionCall = self.functionCall.replace(my_key, value)

        for x in self.myConnections:
            if x.destinationNumber == '--':
                continue
            if x.connType == "HRP_IMAGE":
                self.functionCall += 'if(block$bn$_img_o$so$)// IMG conection\n'
                self.functionCall += 'block$dn$_img_i$di$ = cvCloneImage(block$bn$_img_o$so$);// IMG conection\n'
            elif x.connType == "HRP_INT":
                self.functionCall += 'block$dn$_int_i$di$ = block$bn$_int_o$so$;// INT conection\n'
            elif x.connType == "HRP_POINT":
                self.functionCall += 'block$dn$_point_i$di$ = block$bn$_point_o$so$;// POINT conection\n'
            elif x.connType == "HRP_RECT":
                self.functionCall += 'block$dn$_rect_i$di$ = block$bn$_rect_o$so$;// RECT conection\n'
            elif x.connType == "HRP_DOUBLE":
                self.functionCall += 'block$dn$_double_i$di$ = block$bn$_double_o$so$;// DOUBLE conection\n'
            elif x.connType == "HRP_SIZE":
                self.functionCall += 'block$dn$_size_i$di$ = block$bn$_size_o$so$;// SIZE conection\n'
            else:
                self.functionCall += 'block$dn$_img_i$di$ = cvCloneImage(block$bn$_img_o$so$);// IMG conection\n'

            self.functionCall = self.functionCall.replace("$dn$", str(x.destinationNumber))
            self.functionCall = self.functionCall.replace("$di$", str(x.destinationInput))
            self.functionCall = self.functionCall.replace("$bn$", str(self.plugin.id))
            self.functionCall = self.functionCall.replace("$so$", str(x.sourceOutput))
