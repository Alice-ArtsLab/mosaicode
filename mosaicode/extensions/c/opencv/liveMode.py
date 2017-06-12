#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the LiveMode class.
"""
import os
from glob import glob
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class LiveMode(Plugin):
    """
    This class contains methods related the LiveMode class.
    """
    # --------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.camera = "/dev/video0"

        # Appearance
        self.help = "Realiza a aquisição de uma imagem a partir de câmera."
        self.label = "Live Mode"
        self.color = "50:100:200:150"
        self.out_types = ["mosaicode.extensions.c.ports.image"]
        self.group = "Image Source"

        # ------------------------------C/OpenCv code--------------------------
        self.codes[2] = \
            '// Live Mode \n' + \
            'int value = cvGrabFrame(block$id$_capture);\n' + \
            'block$id$_frame = cvRetrieveFrame(block$id$_capture);\n' + \
            'if(!block$id$_frame){\ncontinue;\n}\n' +\
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_frame);\n'

        self.codes[4] = 'cvReleaseCapture(&block$id$_capture);\n'

    # ----------------------------------------------------------------------
    def get_properties(self):

        available_cams = 4
        device_list = []

        if os.name == 'posix':
            device_list = glob("/dev/video*")

        return [{"name": "Camera",
                 "type": MOSAICODE_COMBO,
                 "values": device_list}]

    # ----------------------------------------------------------------------
    def generate_vars(self):
        camera = self.camera[10:]

        return \
            '// Live Mode Cam \n' + \
            'CvCapture * block$id$_capture = NULL;\n' + \
            'block$id$_capture = cvCaptureFromCAM(' + camera + ');\n' + \
            'IplImage * block$id$_frame = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'
        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
