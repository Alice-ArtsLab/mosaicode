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
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


from harpia.connection import connection
from harpia.blockTemplate import blockTemplate
from harpia.RunPrg import RunPrg
from harpia.utils.XMLUtils import XMLParser
from harpia.constants import *
import s2idirectory

from harpia.control.diagramcontrol import DiagramControl 
import s2iSessionManager

# i18n
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

# Global variable to indicate overall behavior of the code generator
g_bLive = []
g_bFrameRate = 0.1
ErrorLog = 'ErrorLog'

if os.name == "nt":
    tmpDir = os.path.join(os.path.expanduser("~"), "tmp\\")
    if not (os.path.exists(tmpDir)):
        os.makedirs(tmpDir, mode=0700)
else:
    tmpDir = "/tmp/"


#----------------------------------------------------------------------
def gerar(diagram):
    process_XML = XMLParser("<harpia>" + \
                                   str(DiagramControl(diagram).get_process_chain()) + \
                                   "</harpia>", fromString=True)

    print process_XML
    graph_size = len(list(process_XML.getTag("harpia").getTag("properties").getTagChildren()))

    if graph_size > 1:
        blocks = process_XML.getTag("harpia").getTag("properties").getChildTags("block")
        for t_oBlockProperties in blocks:
            block_properties = t_oBlockProperties.getChildTags("property")
            if int(t_oBlockProperties.type) == 00:  # 00 = acquisition block
                inputType = 'file'
                for block_property in block_properties:
                    if block_property.name == 'type':
                        print block_property.name
                        inputType = block_property.value

                    # adoção do paradigma monolítico.. nada de ficar mandando imagens por sockets!!
                    if block_property.name == 'filename' and inputType == 'file':
                        block_property.value = os.path.expanduser(block_property.value)
                        block_property.value = os.path.realpath(block_property.value)
                        if (not os.path.exists(block_property.value)):
                            errMsg = _("Bad Filename: ") + block_property.value
                            print(errMsg)
                            return

            if int(t_oBlockProperties.type) == 01:  # 01 => save image
                for block_property in block_properties:
                    if block_property.name == 'filename':
                        block_property.value = os.path.realpath(block_property.value)

            # seguindo o paradigma de não mandar mais nada.. vamos testar com o haar =]
            # não vamos mandar mais nada mas vamos traduzir o path do haarCascade pra algo real
            if int(t_oBlockProperties.type) == 610:  # 610 => haar detector... passando a cascade .xml
                for block_property in block_properties:
                    if block_property.name == 'cascade_name':
                        block_property.value = os.path.realpath(block_property.value)
                        if (not os.path.exists(block_property.value)):
                            errMsg = _("Bad Filename: ") + block_property.value
                            print(errMsg)
                            return

        # cpscotti standalone!!!
        process_chain = []  # lista pra n precisar ficar copiando prum lado e pro otro o xml inteiro
        process_chain.append(process_XML.getXML())

        session_manager = s2iSessionManager.s2iSessionManager()

        ## pegando o novo ID (criado pela s2iSessionManager) e passando para o s2idiagram
        diagram.set_session_id(session_manager.session_id)

        # step sempre sera uma lista.. primeiro elemento eh uma mensagem, segundo eh o erro.. caso exista erro.. passar para o s2idiagram tb!
        diagram.set_error_log('')
        t_bEverythingOk = True
        for step in session_manager.new_instance(process_chain):
            if len(step) > 1:
                if step[1] != '' and step[1] != None:
                    diagram.append_error_log(step[1])
                    t_bEverythingOk = False
            print step[0]
        # yield step#util caso se resolva usar a interface "lenta" ou se descubra como atualizar rapidamente a GUI



#----------------------------------------------------------------------
def __set_error_log(a_sError):
    if os.name == 'nt':
        Error = file(ErrorLog, 'wb')
    else:
        Error = file(ErrorLog, 'w')
    Error.write(a_sError)
    Error.close()

#----------------------------------------------------------------------
def __apply_weights_on_connections(listOfBlocks, blockList):
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
    blockList = []
    outDeallocations = []
    functionCalls = []
    headers = []
    images = []
    deallocations = []
    global g_bLive
    g_bLive = []
    global g_bFrameRate
    g_bFrameRate = 0.1

    yield [_("Starting Up Generator")]
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
        tmpBlock = blockTemplate(blockIter.type, blockIter.id)
        try:
            block_properties = blockIter.getChildTags("property")
            for propIter in block_properties:
                tmpBlock.properties[propIter.name] = propIter.value
        except AttributeError:
            pass
        tmpBlock.getBlockOutputTypes()

        net_blocks = doc.getTag("harpia").getTag("network").getChildTags("block")
        for block in net_blocks:
            if (block.id != blockIter.id):
                continue
            outputs = block.getTag("outputs").getChildTags("output")
            for output in outputs:
                tmpConnection = connection()
                if output.inBlock != '--':
                    tmpConnection.sourceOutput = output.id
                    tmpConnection.destinationInput = output.input
                    tmpConnection.destinationNumber = output.inBlock
                    tmpConnection.connType = tmpBlock.outTypes[int(tmpConnection.sourceOutput) - 1]
                    tmpBlock.myConnections.append(tmpConnection)
                else:
                    tmpConnection.destinationNumber = '--'
                    tmpBlock.myConnections.append(tmpConnection)
        #######################################################################
        ##Please, do not change the sequence
        tmpBlock.blockCodeWriter()
        tmpBlock.connectorCodeWriter()
        blockList.append(tmpBlock)
        #######################################################################

    weights = []

    for block in blockList:
        if len(s2idirectory.block[block.blockType]().get_description()["InTypes"]) == 0 and len(s2idirectory.block[block.blockType]().get_description()["OutTypes"]) != 0:
            tmpList = []
            tmpList.append(block)
            organizedChain = __apply_weights_on_connections(tmpList, blockList)
            while organizedChain != []:
                organizedChain = __apply_weights_on_connections(organizedChain, blockList)

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

    # Adds only if it does not contains
    temp_header = []
    for header_code in headers:
        if header_code not in temp_header:
            temp_header.append(header_code)

    for header_code in temp_header:
        header += header_code

    header += "\nint main(int argc, char ** argv)\n{"

    declaration = "\n//declaration block\n"

    for image in images:
        declaration += image

    declaration += 'int end = 0;\n'
    declaration += 'int key;\n'
    declaration += 'while(!end) \n {\t \n'

    for value in g_bLive:
        declaration += 'cvGrabFrame(block' + value[0] + '_capture);\n' + \
            'block' + value[0] + '_frame = cvRetrieveFrame (block' + value[0] + '_capture);\n'

    execution = "\n\t//execution block\n"
    for x in functionCalls:
        execution += x

    execution += 'key = cvWaitKey (' + str(int((1.0 / g_bFrameRate) * 1000.0)) + ');\n'
    execution += 'if(key != -1)\n'
    execution += 'end = 1;\n'

    deallocating = "\n\t//deallocation block\n"
    for x in deallocations:
        deallocating += x

    deallocating += "}"

    closing = ""
    closing += "\n"
    for outDea in outDeallocations:
        closing += outDea

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
    makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:" + installDirName + "/lib/;"
    makeFileEntry += "export PKG_CONFIG_PATH=" + installDirName + "/lib/pkgconfig/;"
    makeFileEntry += "g++ " + codeFilename + " -o " + codeFilename[:-2] + " `pkg-config --cflags --libs opencv`"
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

        if len(CerrorList) != 0:
            CompilingErrors += "Something was detected while compiling the source code.\n" + \
                               "There is a huge chance you've found a bug, please report to scotti@das.ufsc.br \n" + \
                               "sending the processing chain (.hrp), this error message and some description on what you were doing.\n" + \
                               "We appreciate your help!\n"
        for element in CerrorList:
            CompilingErrors += element

        o.close()
        i.close()

        if len(g_bLive) > 0:
            yield [_("Running, press any key (on the video output window) to terminate."), CompilingErrors]
        else:
            yield [_("Running ..."), CompilingErrors]

        t_oPrg = RunPrg("LD_LIBRARY_PATH=" + installDirName + "/lib/ ./" + codeFilename[:-2])
        t_oPrg.start()
        while t_oPrg.isAlive():
            t_oPrg.join(0.4)
            while Gtk.events_pending():
                Gtk.main_iteration()

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
