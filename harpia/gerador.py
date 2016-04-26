# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2004 - 2006 Christian Silvano (christian.silvano@gmail.com), Mathias Erdtmann (erdtmann@gmail.com), S2i (www.s2i.das.ufsc.br)
#            2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
# ----------------------------------------------------------------------

################################WARNING!!###########################################
#                      DO NOT MANUALLY EDIT THIS FILE                              #
# LET THE MODIFICATIONS BE INSERTED BY THE TOOLS PROVIDED WITH HARPIA SYSTEM       #
####################################################################################

#############################INCLUDES AND DECLARATIONS##############################
import os
import gtk

####################################INCLUDES OF CLASS##########################################

from harpia.connection import connection
from harpia.blockTemplate import blockTemplate
from harpia.RunPrg import RunPrg

###############################################################################################
# from popen2 import Popen4

from harpia.bpGUI import *
from harpia.utils.XMLUtils import XMLParser
from harpia.constants import *
import s2idirectory

# i18n
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

# Global variable to indicate overall behavior of the code generator
g_bLive = False  # default eh live!!
g_bFrameRate = 0.1
usesFindSquares = 0
g_bCameras = []
g_bVideo = []  # default eh live!!
headers = []
images = []
functionCalls = []
deallocations = []
outDeallocations = []
blockList = []
g_bSaveVideo = []
usesFindSquares = 0
usesFindColor = 0
usesAdjustImage = 0
usesRads = 0

ErrorLog = 'ErrorLog'

if os.name == "nt":
    tmpDir = os.path.join(os.path.expanduser("~"), "tmp\\")
    if not (os.path.exists(tmpDir)):
        os.makedirs(tmpDir, mode=0700)
else:
    tmpDir = "/tmp/"

#----------------------------------------------------------------------
def __clean_generator():
    global headers
    global images
    global functionCalls
    global deallocations
    global outDeallocations
    global blockList
    global usesFindSquares
    global usesFindColor
    global usesAdjustImage
    global usesRads
    headers = []
    images = []
    functionCalls = []
    deallocations = []
    outDeallocations = []
    blockList = []
    g_bSaveVideo = []
    usesFindSquares = 0
    usesFindColor = 0
    usesAdjustImage = 0
    usesRads = 0

#----------------------------------------------------------------------
def adjust_images_size():
    return r"""
// And, Xor, Division, subtraction, sum and multiplication need images with the same size
void adjust_images_size(IplImage * img1, IplImage * img2, IplImage * img3){
    if(img1->width != img2->width || img1->height != img2->height){
	int minW,minH;
	if(img1->width > img2->width)
		minW = img2->width;
	else 
		minW = img1->width;

	if(img1->height > img2->height)
		minH = img2->height;
	else 
		minH = img1->height;

	cvSetImageROI(img2, cvRect( 0, 0, minW, minH ));
	cvSetImageROI(img1, cvRect( 0, 0, minW, minH ));
	cvSetImageROI(img3, cvRect( 0, 0, minW, minH ));
    }
}
"""

#----------------------------------------------------------------------
def __set_error_log(a_sError):
    if os.name == 'nt':
        Error = file(ErrorLog, 'wb')
    else:
        Error = file(ErrorLog, 'w')
    Error.write(a_sError)
    Error.close()

#----------------------------------------------------------------------
def __apply_weights_on_connections(listOfBlocks):
    ##For each block on listt:
    returnList = []
    for block in listOfBlocks:
        ##Put the connections on returnList
        for connection in block.myConnections:
            ##and apply the weight on this connection
            for tmpBlock in blockList:
                if tmpBlock.blockNumber == connection.destinationNumber:
                    tmpBlock.weight += block.weight
                    if tmpBlock not in returnList:
                        # if tmpBlock not in RollinList:
                        returnList.append(tmpBlock)
                    # RollinList.append(tmpBlock)
    return returnList

#----------------------------------------------------------------------
def parseAndGenerate(dirName, XMLChain, installDirName):
    __clean_generator()
    global g_bLive
    global g_bVideo
    global g_bCameras
    global g_bFrameRate
    global g_bSaveVideo
    g_bSaveVideo = []
    g_bVideo = []
    g_bCameras = []
    g_bFrameRate = 0.1
    g_bLive = False  # this shall be a list containing the "blockNumbers" for each live acquisition block; len(g_bLive) works just like it is now..
    yield [_("Starting Up Generator")]
    #doc = binderytools.bind_file(XMLChain)
    doc = XMLParser(XMLChain)
    ########################Create the blocks from XMLChain############################

    ##################################################################################
    # in the future we may want to show some kind of progress bar..
    # the next few comented lines implement a progress counter.. this could be thrown up to the GUI via yields =]
    ##################################################################################
    # t_nBlockCount = 0.0
    # for block in (doc.harpia.properties.block):
    # t_nBlockCount += 1.0
    # t_nItCount = 0.0
    yield [_("Generating Code")]
    blocks = doc.getTag("harpia").getTag("properties").getChildTags("block")
    for blockIter in blocks:
        # print str(100.0*(t_nItCount/t_nBlockCount)) + "%"
        # t_nItCount += 1.0
        tmpBlock = blockTemplate(blockIter.type, blockIter.id)
        try:
            block_properties = blockIter.getChildTags("property")
            for propIter in block_properties:
                tmpBlock.properties.append((propIter.name, propIter.value))
        except AttributeError:
            pass
        ID = tmpBlock.blockNumber
        tmpBlock.getBlockOutputTypes()

        net_blocks = doc.getTag("harpia").getTag("network").getChildTags("block")
        for block in net_blocks:
            if (block.id == ID and int(block.type) <> 10):
                portCount = -1
                outputs = block.getTag("outputs").getChildTags("output")
                for output in outputs:
                    tmpConnection = connection()
                    portCount += 1
                    if output.inBlock != '--':
                        tmpConnection.sourceOutput = output.id
                        tmpConnection.destinationInput = output.input
                        tmpConnection.destinationNumber = output.inBlock
                        tmpConnection.connType = tmpBlock.outTypes[int(tmpConnection.sourceOutput) - 1]
                        tmpBlock.myConnections.append(tmpConnection)
                    else:
                        tmpConnection.destinationNumber = '--'
                        tmpBlock.myConnections.append(tmpConnection)
                    try:
                        if output.grab == 'True':
                            tmpBlock.outputsToSave.append(output.id)
                    except:
                        pass
                    ###################################################################################
                    # ADDING TO EACH BLOCK OBJECT THE RESULTING CODE , THEN ADDING THE BLOCK IN A LIST #
                    ###################################################################################
                    ##Please, do not change the sequence
        tmpBlock.blockCodeWriter()
        tmpBlock.connectorCodeWriter()
        tmpBlock.saverCodeWriter()
        # Some code tricks to allow global variables

        blockList.append(tmpBlock)
    ###################################################################################

    weights = []

    for block in blockList:
        if len(s2idirectory.block[int(block.blockType)]["InTypes"]) == 0 and len(s2idirectory.block[int(block.blockType)]["OutTypes"]) != 0:
            tmpList = []
            tmpList.append(block)
            organizedChain = __apply_weights_on_connections(tmpList)
            while organizedChain != []:
                organizedChain = __apply_weights_on_connections(organizedChain)

    biggestWeight = -1
    for block in blockList:
        if block.weight >= biggestWeight:
            biggestWeight = block.weight

    for activeWeight in range(biggestWeight):
        activeWeight += 1
        for block in blockList:
            if block.weight == activeWeight:
                headers.append(block.header)
                images.append(block.imagesIO)
                functionCalls.append("//Weight: " + str(block.weight) + "\n")
                functionCalls.append(block.functionCall)
                deallocations.append(block.dealloc)
                outDeallocations.append(block.outDealloc)

    header = r"""// Auto-generated C Code - S2i Harpia
/*
*	In order to compile this source code run, in a terminal window, the following command:
*	gcc sourceCodeName.c `pkg-config --libs --cflags opencv` -o outputProgramName
*	
*	the `pkg-config ... opencv` parameter is a inline command that returns the path to both 
*	the libraries and the headers necessary when using opencv. The command also returns other necessary compiler options.
*/
// header:

#ifdef _CH_
#pragma package <opencv>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <opencv/cv.h>
#include <opencv/cxmisc.h>
#include <opencv/cxcore.h>
#include <opencv/ml.h>
#include <opencv/cvaux.h>
#include <opencv/cvwimage.h>
#include <opencv/highgui.h>
#include <math.h>

		"""

    for header_code in headers:
        header += header_code

    header += "\nint main(int argc, char ** argv)\n{"

    declaration = "\n\t//declaration block\n"

    for image in images:
        declaration += image

    if g_bLive:
        declaration += 'int end;  end = 0; int key; \n'
        for aCapture in g_bVideo:
            declaration += 'CvCapture * block' + aCapture[0] + '_capture = NULL; \n IplImage * block' + aCapture[
                0] + '_frame = NULL; \n block' + aCapture[0] + '_capture = cvCreateFileCapture("' + aCapture[
                               1] + '"); \n'
        for aCamera in g_bCameras:
            declaration += 'CvCapture * block' + aCamera[0] + '_capture = NULL; \n IplImage * block' + aCamera[
                0] + '_frame = NULL; \n block' + aCamera[0] + '_capture = cvCaptureFromCAM(' + aCamera[1] + '); \n'
        declaration += 'while(!end) \n {\t \n'

        for aCapture in g_bVideo:
            declaration += 'cvGrabFrame (block' + aCapture[0] + '_capture); \n block' + aCapture[
                0] + '_frame = cvRetrieveFrame (block' + aCapture[0] + '_capture); \n'

        for aCamera in g_bCameras:
            declaration += 'cvGrabFrame (block' + aCamera[0] + '_capture); \n block' + aCamera[
                0] + '_frame = cvRetrieveFrame (block' + aCamera[0] + '_capture); \n'

    execution = "\n\t//execution block\n"
    for x in functionCalls:
        execution += x
    if g_bLive:
        execution += '\n\tkey = cvWaitKey (' + str(int((1.0 / g_bFrameRate) * 1000.0)) + ');\n if(key != -1)\n end = 1;'
        deallocating = "\n\t//deallocation block\n"
        for x in deallocations:
            deallocating += x

        deallocating += "}"

    else:
        deallocating = "\n\t//deallocation block\n"

        for x in deallocations:
            deallocating += x

    closing = ""
    closing += "\n"
    for outDea in outDeallocations:
        closing += outDea
    if g_bLive:
        for aCapture in g_bVideo:
            closing += 'cvReleaseCapture(&block' + aCapture[0] + '_capture);\n'
        for aCamera in g_bCameras:
            closing += 'cvReleaseCapture(&block' + aCamera[0] + '_capture);\n'
    for vWriter in g_bSaveVideo:
        closing += 'cvReleaseVideoWriter(&block' + vWriter + '_vidWriter); // SaveVideo\n'
    closing += "return 0;\n } //closing main()\n"


    # Final code assembly
    entireCode = header + declaration + execution + deallocating + closing


    yield [_("Saving Code")]
    # saving code file
    os.chdir(tmpDir + dirName)
    codeFilename = dirName + '.c'
    codeFile = open(codeFilename, 'w')
    codeFile.write(entireCode)
    codeFile.close()

    yield [_("Building Makefile")]
    # Assembly of "necessary" makefiles
    # ...windows..
    makeFilename = 'Makefile' + dirName + '.bat'
    makeFileEntry = '"' + installDirName + '\\bin\\gcc.exe" ' + codeFilename + " -o " + codeFilename[:-2] + ".exe -lcv -lcxcore -lhighgui"
    makeFile = open(makeFilename, 'w')
    makeFile.write(makeFileEntry)
    makeFile.close()

    # ...posix..
    makeFilename = 'Makefile.' + dirName
    makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:" + installDirName + "/lib/; export PKG_CONFIG_PATH=" + installDirName + "/lib/pkgconfig/;g++ " + codeFilename + " -o " + codeFilename[
                                                                                                                                                                                       :-2] + " `pkg-config --cflags --libs opencv`"
    makeFile = open(makeFilename, 'w')
    makeFile.write(makeFileEntry)
    makeFile.close()

    yield [_("Compiling ...")]
    if os.name == "nt":
        i, o = os.popen4('Makefile' + dirName + '.bat')

        o.readlines()
        o.close()
        i.close()
        yield [_("Running ...")]
        i, o = os.popen4(codeFilename[:-2] + '.exe')

        ## ERROR LOG
        Error = ''
        errorList = o.readlines()
        for element in errorList:
            Error = Error + element

        __set_error_log(Error)

        o.readlines()
        o.close()
        i.close()
    else:
        i, o = os.popen4("sh " + makeFilename)

        ## appending compile errors too.. helps finding bugs! =]
        CompilingErrors = ''
        CerrorList = o.readlines()

        if len(CerrorList) <> 0:
            CompilingErrors += "Something was detected while compiling the source code.\n" + \
                               "There is a huge chance you've found a bug, please report to scotti@das.ufsc.br \n" + \
                               "sending the processing chain (.hrp), this error message and some description on what you were doing.\n" + \
                               "We appreciate your help!\n"
        for element in CerrorList:
            CompilingErrors += element

        o.close()
        i.close()

        if g_bLive:
            yield [_("Running, press any key (on the video output window) to terminate."), CompilingErrors]
        else:
            yield [_("Running ..."), CompilingErrors]

        t_oPrg = RunPrg("LD_LIBRARY_PATH=" + installDirName + "/lib/ ./" + codeFilename[:-2])
        t_oPrg.start()
        while t_oPrg.isAlive():
            t_oPrg.join(0.4)
            while gtk.events_pending():
                gtk.main_iteration(False)

        ## ERROR LOG
        o = open("RunErrorLog", "r")
        Error = ''
        errorList = o.readlines()
        for element in errorList:
            Error += element

        yield [_("Leaving.."), Error]
        __set_error_log(CompilingErrors + Error)

        o.close()
        i.close()
