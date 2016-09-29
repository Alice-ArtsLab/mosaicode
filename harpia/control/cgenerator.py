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
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.system import System as System
from codegenerator import CodeGenerator

FRAMERATE = 25

class CGenerator(CodeGenerator):

    #----------------------------------------------------------------------
    def __init__(self, diagram):
        CodeGenerator.__init__(self, diagram)

    #----------------------------------------------------------------------
    def generate_code(self):
        System.log("Parsing Code")

        self.sort_blocks()
        self.generate_parts()

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
        for header_code in self.headers:
            if header_code not in temp_header:
                temp_header.append(header_code)

        for header_code in temp_header:
            header += header_code

        header += "\nint main(int argc, char ** argv){\n"
        header += "char key = ' ';\n"
        declaration_block = "\n//declaration block\n"

        for var in self.declarations:
            declaration_block += var

        declaration_block += 'while((key = (char)cvWaitKey(' + \
                str(int((1.0 / FRAMERATE) * 1000.0)) + \
                ')) != 27) \n {\t \n'

        execution = "\n\t//execution block\n"
        for x,y in zip(self.functionCalls, self.connections):
            execution += x
            execution += y

        deallocating = "\n\t//deallocation block\n"
        for x in self.deallocations:
            deallocating += x

        deallocating += "}"

        closing = ""
        closing += "\n"
        for outDea in self.outDeallocations:
            closing += outDea

        closing += "return 0;\n } //closing main()\n"

        # Final code assembly
        return header + declaration_block + execution + deallocating + closing

    #----------------------------------------------------------------------
    def save_code(self):
        System.log("Saving Code to " + self.dir_name + self.filename)
        self.change_directory()
        codeFilename = self.filename + '.c'
        codeFile = open(codeFilename, 'w')
        code = self.generate_code()
        codeFile.write(code)
        codeFile.close()

        if os.name == "nt":
            makeFilename = self.filename +'.Makefile.bat'
            makeFileEntry = '"/\\bin\\gcc.exe" ' + codeFilename + \
                    " -o " + codeFilename[:-2] + ".exe -lcv -lcxcore -lhighgui"
            makeFile = open(makeFilename, 'w')
            makeFile.write(makeFileEntry)
            makeFile.close()
        else:
            makeFilename = self.filename +'.Makefile'
            makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib/;\n"
            makeFileEntry += "export PKG_CONFIG_PATH=/lib/pkgconfig/;\n"
            makeFileEntry += "g++ " + codeFilename + " -o " + \
                    self.filename + " `pkg-config --cflags --libs opencv`\n"
            makeFile = open(makeFilename, 'w')
            makeFile.write(makeFileEntry)
            makeFile.close()
        self.return_to_old_directory()

    #----------------------------------------------------------------------
    def compile(self):
        System.log("Compilando")
        System.log("Executing Code")
        self.save_code()
        self.change_directory()
        if os.name == "nt":
            i, o = os.popen4(self.filename +'.Makefile.bat')

            o.readlines()
            o.close()
            i.close()
        else:
            i, o = os.popen4("sh " + self.filename +'.Makefile')

            CompilingErrors = o.readlines()
            System.log("Errors "  +  str(CompilingErrors))

            o.close()
            i.close()

        self.return_to_old_directory()

    #----------------------------------------------------------------------
    def execute(self):
        System.log("Executing Code")
        self.compile()
        self.change_directory()
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
            command = "LD_LIBRARY_PATH=/lib/ ./" + self.filename + " 2> Error" + self.error_log_file
            program = Thread(target=os.system, args=(command,))
            program.start()
            while program.isAlive():
                program.join(0.4)
                while Gtk.events_pending():
                    Gtk.main_iteration()

        try:
            o = open("Run" + self.error_log_file, "r")
            Error = ''
            errorList = o.readlines()
            for element in errorList:
                Error += element

            System.log("Leaving..")
            System.log(Error)
            o.close()
        except:
            pass
        self.return_to_old_directory()


#----------------------------------------------------------------------
