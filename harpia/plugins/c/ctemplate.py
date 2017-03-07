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
"""
This module contains the CTemplate class.
"""

from harpia.model.codetemplate import CodeTemplate

class CTemplate(CodeTemplate):
    """
    This class contains methods related the CTemplate class.
    """

    def __init__(self):
        CodeTemplate.__init__(self)
        self.name = "opencv"
        self.language = "c"
        self.description = "c / opencv code template"
        self.extension = '.c'
        self.command = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib/;\n"
        self.command += "export PKG_CONFIG_PATH=/lib/pkgconfig/;\n"
        self.command += "g++ $filename$$extension$  -o $filename$ `pkg-config --cflags --libs opencv`\n"
        self.command += "LD_LIBRARY_PATH=/lib/ $dir_name$./$filename$  2> Error $error_log_file$"

        self.code = r"""// Auto-generated C Code - S2i Harpia
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

#define FRAMERATE 1000.0 / 25.0

$originalheader$

int main(int argc, char ** argv){
        char key = ' ';
        //declaration block
        $declaration$
        while((key = (char)cvWaitKey(FRAMERATE)) != 27){
            //execution block
            $execution$

            //deallocation block
            $deallocating$

        } // End of while
    $closing$

return 0;

} //closing main()
"""


#----------------------------------------------------------------------
