import s2idirectory

############################################################
##################### block templates ######################
class blockTemplate:
    blockType = 'NA'
    blockNumber = 'NA'
    imagesIO = ''
    functionArguments = ''
    outputCopy = ''
    xmlResult = ''
    dealloc = ''
    outDealloc = ''
    properties = []
    myConnections = []
    outputsToSave = []
    weight = 1
    outTypes = []

    ###########################################################################

    ######################################################3
    #### Added by cpscotti. blockTemplate needs its outputTypes even "before" its code.. here it is
    def getBlockOutputTypes(self):
        try:
            self.outTypes = s2idirectory.block[int(self.blockType)]["OutTypes"]
        except:
            self.outTypes = "HRP_IMAGE", "HRP_IMAGE", "HRP_IMAGE", "HRP_IMAGE"

        ############################### processors #################################
        # THIS CODE IS TO CREATE THE C LINES FROM THE XML PARSING                  #
        ############################################################################
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
        self.dealloc = self.dealloc.replace("$$", str(self.blockNumber))
        self.outDealloc = self.outDealloc.replace("$$", str(self.blockNumber))
        self.functionArguments = self.functionArguments.replace("$$", str(self.blockNumber))

        ############################ connectors ####################################
        # THIS CODE IS RESPONSIBLE FOR CREATING THE ASSIGNMENTS BETWEEN THE IMAGES #
        ############################################################################
        # It works simply by copying all the content resulting from it's processing to feed another image.

    def connectorCodeWriter(self):
        for x in self.myConnections:
            if x.destinationNumber <> '--':
                ##### cpscotti typed connections..
                if x.connType == "HRP_IMAGE":
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(block' + self.blockNumber + '_img_o' + x.sourceOutput + ');// IMAGE conection\n'
                elif x.connType == "HRP_INT":
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_int_i' + x.destinationInput + ' = block' + self.blockNumber + '_int_o' + x.sourceOutput + ';// INT conection\n'
                elif x.connType == "HRP_POINT":
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_point_i' + x.destinationInput + ' = block' + self.blockNumber + '_point_o' + x.sourceOutput + ';// POINT conection\n'
                elif x.connType == "HRP_RECT":
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_rect_i' + x.destinationInput + ' = block' + self.blockNumber + '_rect_o' + x.sourceOutput + ';// RECT conection\n'
                elif x.connType == "HRP_DOUBLE":
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_double_i' + x.destinationInput + ' = block' + self.blockNumber + '_double_o' + x.sourceOutput + ';// DOUBLE conection\n'
                elif x.connType == "HRP_SIZE":
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_size_i' + x.destinationInput + ' = block' + self.blockNumber + '_size_o' + x.sourceOutput + ';// SIZE conection\n'
                else:
                    self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(block' + self.blockNumber + '_img_o' + x.sourceOutput + ');// IMAGE conection\n'

                #############################   savers   #######################################
                # THIS CODE IS TO SAVE IMAGES THAT WILL BE RETURNED AFTER THE IMAGE PROCESSING #
                ################################################################################

    def saverCodeWriter(self):
        for x in self.outputsToSave:
            self.functionCall = self.functionCall + 'cvSaveImage("block' + self.blockNumber + '_img_o' + x + '.png" ,block' + self.blockNumber + '_img_o' + x + ');\n'
