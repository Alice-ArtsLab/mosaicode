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

from harpia.blockTemplate import BlockTemplate
from harpia.RunPrg import RunPrg
from harpia.constants import *
from harpia.s2idirectory import *

# i18n
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

FRAMERATE = 25

class CodeGenerator():

    #----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram
        self.dir_name = DIRNAME + str(time.time())
        self.old_path = os.path.realpath(os.curdir)
        if not len(self.diagram.blocks) > 1:
            harpia.s2idirectory.Log.log("Diagram is empty. Nothing to generate.")
            return

    #----------------------------------------------------------------------
    def __change_directory(self):
        try:
            os.makedirs(harpia.s2idirectory.properties.get_default_directory())
        except:
            pass
        os.chdir(harpia.s2idirectory.properties.get_default_directory())
        try:
            os.makedirs(self.dir_name)
        except:
            pass
        os.chdir(harpia.s2idirectory.properties.get_default_directory() + '/' + self.dir_name)

    #----------------------------------------------------------------------
    def __return_to_old_directory(self):
        os.chdir(self.old_path)

    #----------------------------------------------------------------------
    def generate_code(self):
        harpia.s2idirectory.Log.log("Parsing Code")
        blockList = []
        outDeallocations = []
        functionCalls = []
        headers = []
        declaration = []
        deallocations = []

        # Configura as propriedades dos blocos no blocktemplate
        for block_key in self.diagram.blocks:
            block = self.diagram.blocks[block_key]
            block_template = BlockTemplate(block.get_plugin())
            for connection in self.diagram.connectors:
                if connection.from_block != block.get_plugin().id:
                    continue
                connection.type = block.get_description()["OutTypes"][connection.from_block_out]
                block_template.myConnections.append(connection)

            block_template.generate_block_code()
            blockList.append(block_template)

        # ajusta o peso de cada bloco
        for block_template in blockList:
            if len(block_template.plugin.get_description()["InTypes"]) != 0:
                continue
            if len(block_template.plugin.get_description()["OutTypes"]) == 0:
                continue
            tmpList = []
            tmpList.append(block_template)
            organizedChain = self.__apply_weights_on_connections(tmpList, blockList)
            while organizedChain != []:
                organizedChain = self.__apply_weights_on_connections(organizedChain, blockList)

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
                    declaration.append(block.declaration)
                    functionCalls.append(block.functionCall)
                    functionCalls.append(block.connections)
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

        declaration_block = "\n//declaration block\n"

        for var in declaration:
            declaration_block += var

        declaration_block += 'while(((char)cvWaitKey(' + \
                str(int((1.0 / FRAMERATE) * 1000.0)) + \
                ')) != 27) \n {\t \n'

        execution = "\n\t//execution block\n"
        for x in functionCalls:
            execution += x

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
        return header + declaration_block + execution + deallocating + closing

    #----------------------------------------------------------------------
    def save_code(self):
        harpia.s2idirectory.Log.log("Saving Code to " + self.dir_name)
        self.__change_directory()
        codeFilename = self.dir_name + '.c'
        codeFile = open(codeFilename, 'w')
        code = self.generate_code()
        codeFile.write(code)
        codeFile.close()

        if os.name == "nt":
            makeFilename = 'Makefile' + self.dir_name + '.bat'
            makeFileEntry = '"/\\bin\\gcc.exe" ' + codeFilename + \
                    " -o " + codeFilename[:-2] + ".exe -lcv -lcxcore -lhighgui"
            makeFile = open(makeFilename, 'w')
            makeFile.write(makeFileEntry)
            makeFile.close()
        else:
            makeFilename = 'Makefile.' + self.dir_name
            makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib/;\n"
            makeFileEntry += "export PKG_CONFIG_PATH=/lib/pkgconfig/;\n"
            makeFileEntry += "g++ " + codeFilename + " -o " + \
                    codeFilename[:-2] + " `pkg-config --cflags --libs opencv`\n"
            makeFile = open(makeFilename, 'w')
            makeFile.write(makeFileEntry)
            makeFile.close()
        self.__return_to_old_directory()

    #----------------------------------------------------------------------
    def compile(self):
        harpia.s2idirectory.Log.log("Compilando")
        harpia.s2idirectory.Log.log("Executing Code")
        self.save_code()
        self.__change_directory()
        if os.name == "nt":
            i, o = os.popen4('Makefile' + self.dir_name + '.bat')

            o.readlines()
            o.close()
            i.close()
        else:
            i, o = os.popen4("sh " + 'Makefile.' + self.dir_name)

            ## appending compile errors too.. helps finding bugs! =]
            CompilingErrors = o.readlines()
            harpia.s2idirectory.Log.log("Errors "  +  str(CompilingErrors))

            o.close()
            i.close()

        self.__return_to_old_directory()

    #----------------------------------------------------------------------
    def execute(self):
        harpia.s2idirectory.Log.log("Executing Code")
        self.compile()
        self.__change_directory()
        if os.name == "nt":
            i, o = os.popen4(codeFilename[:-2] + '.exe')
            ## ERROR LOG
            Error = ''
            errorList = o.readlines()
            for element in errorList:
                Error = Error + element
            o.close()
            i.close()
        else:
            program = RunPrg("LD_LIBRARY_PATH=/lib/ ./" + self.dir_name)
            program.start()
            while program.isAlive():
                program.join(0.4)
                while Gtk.events_pending():
                    Gtk.main_iteration()

        try:
            o = open("RunErrorLog", "r")
            Error = ''
            errorList = o.readlines()
            for element in errorList:
                Error += element

            harpia.s2idirectory.Log.log("Leaving..")
            harpia.s2idirectory.Log.log(Error)
            o.close()
        except:
            pass
        self.__return_to_old_directory()

    #----------------------------------------------------------------------
    def __set_error_log(self, error):
        if os.name == 'nt':
            Error = file(harpia.s2idirectory.properties.get_error_log_file(), 'wb')
        else:
            Error = file(harpia.s2idirectory.properties.get_error_log_file(), 'w')
        harpia.s2idirectory.Log.log(error)
        Error.write(error)
        Error.close()

    #----------------------------------------------------------------------
    def __apply_weights_on_connections(self, listOfBlocks, blockList):
        returnList = []
        for block_template in listOfBlocks:
            ##Put the connections on returnList
            for connection in block_template.myConnections:
                ##and apply the weight on this connection
                for tmp_block_template in blockList:
                    if tmp_block_template.plugin.id == connection.to_block:
                        tmp_block_template.weight += block_template.weight
                        if tmp_block_template not in returnList:
                            returnList.append(tmp_block_template)
        return returnList


