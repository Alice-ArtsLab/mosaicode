#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the LiveDelay class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin


class LiveDelay(Plugin):
    """
    This class contains methods related the liveDelay class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.frameNumber = 5

        # Appearance
        self.help = "Inserts a delay inside a live stream."
        self.label = "Live Delay"
        self.color = "250:20:30:150"
        self.in_types = ["harpia.extensions.c.ports.image"]
        self.out_types = ["harpia.extensions.c.ports.image"]
        self.group = "General"

        self.properties = [{"name": "Time (in frames)",
                            "label": "frameNumber",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 200,
                            "step": 1
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------
        self.codes[2] = '''
            if(block$id$_img_i0){
                cvReleaseImage(&(block$id$_buffer[i_$id$]));
                block$id$_buffer[i_$id$] = cvCloneImage(block$id$_img_i0);
                i_$id$++;
                i_$id$ %= $frameNumber$;
                block$id$_img_o0 = block$id$_buffer[i_$id$];
            }
            '''
        self.codes[3] = 'cvReleaseImage(&block$id$_img_i0);\n'

        self.codes[4] = '''
            for(i_$id$=0; i_$id$<$frameNumber$; i_$id$++)
                if(block$id$_buffer[i_$id$] != NULL)
                    cvReleaseImage(&(block$id$_buffer[i_$id$]));
            '''

    # ----------------------------------------------------------------------
    def generate_vars(self):
        self.frameNumber = int(round(float(self.frameNumber)))
        value = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int i_$id$ = 0;\n' + \
            'IplImage * block$id$_buffer[$frameNumber$] = {'
        for idx in range(self.frameNumber):
            value += 'NULL'
            if idx != self.frameNumber - 1:
                value += ','
        value += '};\n'

        for idx in range(self.frameNumber):
            value += 'block$id$_buffer[' + str(
                idx) + '] = cvCreateImage( cvSize(640,480), 8, 3);\n'
            value += 'cvSetZero(block$id$_buffer[' + str(idx) + ']);\n'
        value += 'block$id$_img_o0 = block$id$_buffer[' + \
            str(self.frameNumber - 1) + '];\n'

        return value


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
