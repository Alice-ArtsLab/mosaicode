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
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


from harpia.connection import Connection
from harpia.blockTemplate import BlockTemplate
from harpia.RunPrg import RunPrg
from harpia.constants import *
import s2idirectory

from harpia.control.diagramcontrol import DiagramControl 

# i18n
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

# Global variable to indicate overall behavior of the code generator
g_bLive = []
FRAMERATE = 25
ErrorLog = 'ErrorLog'



#----------------------------------------------------------------------
def gerar(diagram):

    if not len(diagram.blocks) > 1:
        print "Nothing to generate"
        return

    dir_name = "harpiaBETMP0" + str(time.time())
    old_path = os.path.realpath(os.curdir)
    os.chdir(TMPDIR)
    os.mkdir(dir_name)
    os.chdir(TMPDIR + '/' + dir_name)
   
    print "Starting"
    entireCode = __parseAndGenerate(dir_name, diagram)
    print "Parse And Generate Ok"
    codeFilename = __save_code(dir_name, entireCode)
    print "Save Code Ok"
    __build_makefile(dir_name, codeFilename)
    print "Build Makefile Ok"
    __execute_code(dir_name, codeFilename)
    print "Compile Code Ok"

    os.chdir(old_path)

#----------------------------------------------------------------------
def __parseAndGenerate(dirName, diagram):
    blockList = []
    outDeallocations = []
    functionCalls = []
    headers = []
    images = []
    deallocations = []
    global g_bLive
    g_bLive = []

    # Configura as propriedades dos blocos no blocktemplate
    for block_key in diagram.blocks:
        block = diagram.blocks[block_key]
        block_template = BlockTemplate(block.plugin)
        for connection in diagram.connectors:
            if connection.from_block != block.plugin.id:
                continue
            tmpConnection = Connection()
            tmpConnection.sourceOutput = int (connection.from_block_out) + 1
            tmpConnection.destinationInput = int(connection.to_block_in ) + 1
            tmpConnection.destinationNumber = connection.to_block
            tmpConnection.connType = block.plugin.get_description()["OutTypes"][connection.from_block_out]
            block_template.myConnections.append(tmpConnection)

        block_template.generate_block_code()
        blockList.append(block_template)

    # ajusta o peso de cada bloco
    for block in blockList:
        if len(block.plugin.get_description()["InTypes"]) != 0:
            continue
        if len(block.plugin.get_description()["OutTypes"]) == 0:
            continue
        tmpList = []
        tmpList.append(block)
        organizedChain = __apply_weights_on_connections(tmpList, blockList)
        while organizedChain != []:
            organizedChain = __apply_weights_on_connections(organizedChain, blockList)

    # encontro o maior peso
    biggestWeight = -1
    for block in blockList:
        if block.weight >= biggestWeight:
            biggestWeight = block.weight

    # Gero o código do menor peso para o maior
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
            'block' + str(value[0]) + '_frame = cvRetrieveFrame (block' + str(value[0]) + '_capture);\n'

    execution = "\n\t//execution block\n"
    for x in functionCalls:
        execution += x

    execution += 'key = cvWaitKey (' + str(int((1.0 / FRAMERATE) * 1000.0)) + ');\n'
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
    return header + declaration + execution + deallocating + closing

#----------------------------------------------------------------------
def __save_code(dirName, entireCode):
    os.chdir(TMPDIR + dirName)
    codeFilename = dirName + '.c'
    codeFile = open(codeFilename, 'w')
    codeFile.write(entireCode)
    codeFile.close()
    return codeFilename

#----------------------------------------------------------------------
def __build_makefile(dirName, codeFilename):
    # Assembly of "necessary" makefiles
    # ...windows..
    makeFilename = 'Makefile' + dirName + '.bat'
    makeFileEntry = '"/\\bin\\gcc.exe" ' + codeFilename + " -o " + codeFilename[:-2] + ".exe -lcv -lcxcore -lhighgui"
    makeFile = open(makeFilename, 'w')
    makeFile.write(makeFileEntry)
    makeFile.close()

    # ...posix..
    makeFilename = 'Makefile.' + dirName
    makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib/;\n"
    makeFileEntry += "export PKG_CONFIG_PATH=/lib/pkgconfig/;\n"
    makeFileEntry += "g++ " + codeFilename + " -o " + codeFilename[:-2] + " `pkg-config --cflags --libs opencv`\n"
    makeFile = open(makeFilename, 'w')
    makeFile.write(makeFileEntry)
    makeFile.close()


#----------------------------------------------------------------------
def __execute_code(dirName, codeFilename):
    if os.name == "nt":
        i, o = os.popen4('Makefile' + dirName + '.bat')

        o.readlines()
        o.close()
        i.close()

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
        i, o = os.popen4("sh " + 'Makefile.' + dirName)

        ## appending compile errors too.. helps finding bugs! =]
        CompilingErrors = o.readlines()
        print "Errors" , CompilingErrors

        o.close()
        i.close()

    print "Running"
    t_oPrg = RunPrg("LD_LIBRARY_PATH=/lib/ ./" + codeFilename[:-2])
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

    print _("Leaving.."), Error
    __set_error_log(str(CompilingErrors) + Error)

    o.close()
    i.close()
        
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
                if tmpBlock.plugin.id == connection.destinationNumber:
                    tmpBlock.weight += block.weight
                    if tmpBlock not in returnList:
                        # if tmpBlock not in RollinList:
                        returnList.append(tmpBlock)
                    # RollinList.append(tmpBlock)
    return returnList


