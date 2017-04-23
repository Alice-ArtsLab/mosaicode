# -*- coding: utf-8 -*-
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
        self.command += "LD_LIBRARY_PATH=/lib/ $dir_name$./$filename$"

        self.code = r"""
// Auto-generated C Code - S2i Harpia
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

$single_code[0]$

int main(int argc, char ** argv){
        char key = ' ';
        //declaration block
        $code[1]$
        while((key = (char)cvWaitKey(FRAMERATE)) != 27){
            //execution block
            $code[2, connection]$

            //deallocation block
            $code[3]$

        } // End of while
    $code[4]$

return 0;

} //closing main()
"""


#----------------------------------------------------------------------
