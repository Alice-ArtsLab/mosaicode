#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class LiveDelay(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.frameNumber = 5

        self.help = "Inserts a delay inside a live stream."

        self.description = {
            'Label': 'Live Delay',
            'Icon': 'images/liveDelay.png',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'TreeGroup': 'General',
        }

        self.properties = {
            "frameNumber": {
                "name": "Time (in frames)",
                "type": HARPIA_INT,
                "lower": 1,
                "upper": 200,
                "step": 1
            }
        }
        # ------------------------------C/OpenCv code--------------------------
        self.vars = ""

        self.function_call = '''
            if(block$id$_img_i0){
                cvReleaseImage(&(block$id$_buffer[i_$id$]));
                block$id$_buffer[i_$id$] = cvCloneImage(block$id$_img_i0);
                i_$id$++;
                i_$id$ %= $frameNumber$;
                block$id$_img_o0 = block$id$_buffer[i_$id$];
            }
            '''
        self.dealloc = 'cvReleaseImage(&block$id$_img_i0);\n'

        self.out_dealloc = '''
            for(i_$id$=0; i_$id$<$frameNumber$; i_$id$++)
                if(block$id$_buffer[i_$id$] != NULL)
                    cvReleaseImage(&(block$id$_buffer[i_$id$]));
            '''

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

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

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return self.out_dealloc

# -----------------------------------------------------------------------------
