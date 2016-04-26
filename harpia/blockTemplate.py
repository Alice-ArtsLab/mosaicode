import s2idirectory

############################################################
##################### block templates ######################
class blockTemplate:
    blockType = 'NA'
    blockNumber = 'NA'
    imagesIO = ''
    dealloc = ''
    outDealloc = ''
    properties = []
    myConnections = []
    outputsToSave = []
    weight = 1
    outTypes = []
    header = ''

    ###########################################################################
    def __init__(self, block_type, block_id):
        self.blockType = block_type
        self.blockNumber = block_id
        self.properties = []
        self.myConnections = []
        self.outputsToSave = []

    ######################################################3
    #### Added by cpscotti. blockTemplate needs its outputTypes even "before" its code.. here it is
    def getBlockOutputTypes(self):
        try:
            self.outTypes = s2idirectory.block[int(self.blockType)]["OutTypes"]
        except:
            self.outTypes = "HRP_IMAGE", "HRP_IMAGE", "HRP_IMAGE", "HRP_IMAGE"

    def blockCodeWriter(self):
        PkgName = 'harpia.bpGUI.'
        ModName = str(s2idirectory.block[int(self.blockType)]["Path"]["Python"])
        #from spam.ham import eggs" results in "
        harpia_bpGUI_Mod = __import__(PkgName, globals(), locals(), [ModName])
        guiMod = getattr(harpia_bpGUI_Mod, ModName)
        guiMod.generate(self)
        self.imagesIO = self.imagesIO.replace("$$", str(self.blockNumber))
        self.functionCall = self.functionCall.replace("$$", str(self.blockNumber))
        self.dealloc = self.dealloc.replace("$$", str(self.blockNumber))
        self.outDealloc = self.outDealloc.replace("$$", str(self.blockNumber))

    def connectorCodeWriter(self):
        for x in self.myConnections:
            if x.destinationNumber != '--':
                if x.connType == "HRP_IMAGE":
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
                self.functionCall = self.functionCall.replace("$bn$", str(self.blockNumber))
                self.functionCall = self.functionCall.replace("$so$", str(x.sourceOutput))

    def saverCodeWriter(self):
        for x in self.outputsToSave:
            self.functionCall += 'cvSaveImage("block$$_img_o' + x + '.png" ,block$$_img_o' + x + ');\n'
        self.functionCall = self.functionCall.replace("$$", str(self.blockNumber))
