#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin
import os
from glob import glob


class Capture(OpenCVPlugin):

    # ------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.camera = "/dev/video0"

        # Appearance
        self.help = "Realiza a aquisição de uma imagem " + \
            "a partir de algum dispositivo," + \
            " seja este uma mídia ou um dispositivo " + \
            "de aquisição de imagens (câmera, scanner)."
        self.label = "Capture"
        self.icon = "images/acquisition.png"
        self.color = "50:100:200:150"
        self.out_types = ["HRP_IMAGE"]
        self.group = "Image Source"

        # ---------------------C/OpenCv code-----------------------------------
        self.vars = \
            'IplImage * block$id$_img_o0 = NULL; //Capture\n' + \
            'CvCapture* block$id$_capture = NULL; \n' + \
            'IplImage* block$id$_frame = NULL; \n' + \
            'int counter$id$ = 0;\n'

    # ----------------------------------------------------------------------
    def get_properties(self):
        available_cams = 4
        device_list = []

        if os.name == 'posix':
            device_list = glob("/dev/video*")

        return {
            "camera": {
                "name": "Camera",
                "type": HARPIA_COMBO,
                "values": device_list
            }
        }

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        camera = self.camera[10:]
        return \
            'if (counter$id$ == 0){\n' + \
            'block$id$_capture = cvCaptureFromCAM(' + camera + '); \n' + \
            'if( !cvGrabFrame( block$id$_capture ))' + \
            '{ printf("Cannot Grab Image from camera ' + camera + '"); }\n' + \
            'block$id$_frame = cvRetrieveFrame( block$id$_capture ); \n' + \
            'block$id$_img_o0 = cvCloneImage( block$id$_frame );\n' + \
            'counter$id$++;\n' + \
            '}\n'

# ------------------------------------------------------------------------------
