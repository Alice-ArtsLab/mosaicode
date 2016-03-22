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
        self.functionArguments = self.functionArguments.replace("$$", str(self.blockNumber))

        ############################ connectors ####################################
        # THIS CODE IS RESPONSIBLE FOR CREATING THE ASSIGNMENTS BETWEEN THE IMAGES #
        ############################################################################
        # It works simply by copying all the content resulting from it's processing to feed another image.

    def connectorCodeWriter(self):
        global g_bLive
        global g_flagFrame
        global g_bSaveVideo
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
                    # if ( (not g_bLive) or (g_flagFrame == 0) ):
                # self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(block' + self.blockNumber + '_img_o' + x.sourceOutput + ');//conection\n'
                # elif g_flagFrame:
                #   self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(frame);//conection\n'
                #   global g_flagFrame
                #   g_flagFrame = 0
                ############################################################################


                #############################   savers   #######################################
                # THIS CODE IS TO SAVE IMAGES THAT WILL BE RETURNED AFTER THE IMAGE PROCESSING #
                ################################################################################

    def saverCodeWriter(self):
        global g_bLive
        for x in self.outputsToSave:
            # if g_bLive:
            # self.functionCall = self.functionCall + 'cvNamedWindow("block' + self.blockNumber + '_img_o' + x +',block' + self.blockNumber + '_img_o' + x + ');\n cvShowImage("block' + self.blockNumber + '_img_o' + x +',block' + self.blockNumber + '_img_o' + x + '); \n'
            # else:
            self.functionCall = self.functionCall + 'cvSaveImage("block' + self.blockNumber + '_img_o' + x + '.png" ,block' + self.blockNumber + '_img_o' + x + ');\n'

    def create_XML_result(self, dirPathName):
        for x in self.outputsToSave:
            filename = "block" + str(self.blockNumber) + "_img_o" + x + ".png"
            im = Image.open(tmpDir + dirPathName + "/" + filename)
            if (im.mode == 'RGB' or im.mode == 'HSV'):
                nChannels = 3
            else:
                nChannels = 1
            depth = nChannels * 8  # Provisoriamente
            self.xmlResult = '<result block=\"' + str(self.blockNumber) + '\" output=\"' + str(
                x) + '\">\n<content type = \"image\">\n<filename> ' + filename + '</filename>\n<properties depth=\"' + str(
                depth) + '\"  height= \"' + str(im.size[0]) + '\" width= \"' + str(
                im.size[1]) + '\"  channels=\"' + str(nChannels) + '\" />\n</content>\n</result>'


#######################EXAMPLE OF XML_RESULT###################################
# <result block='03' output='o1'>
#  <content type='image'>
#    <buffer>000011111101</buffer>
#    <properties depth='24' height='640'
#                width='480' channels='3' />
#  </content>
# </result>
################################################################################
