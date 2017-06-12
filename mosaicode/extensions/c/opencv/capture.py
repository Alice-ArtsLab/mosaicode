#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Capture class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin
import os
from glob import glob


class Capture(Plugin):
    """
    This class contains methods related the Capture class.
    """
    # ------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.help = "Realiza a aquisição de uma imagem " + \
            "a partir de algum dispositivo," + \
            " seja este uma mídia ou um dispositivo " + \
            "de aquisição de imagens (câmera, scanner)."
        self.label = "Capture"
        self.color = "50:100:200:150"
        self.out_ports = [{"type":"mosaicode.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"}
                          ]
        self.group = "Image Source"
        self.language = "c"
        self.framework = "opencv"
        self.properties = [{"name": "camera",
                 "label": "Camera",
                 "type": MOSAICODE_INT,
                 "value":"0",
                 "lower": 0,
                 "upper": 4}]

        self.codes[1] = \
            'IplImage * block$id$_img_o0 = NULL; //Capture\n' + \
            'CvCapture* block$id$_capture = NULL; \n' + \
            'IplImage* block$id$_frame = NULL; \n' + \
            'int counter$id$ = 0;\n'

        self.codes[2] = \
            'if (counter$id$ == 0){\n' + \
            'block$id$_capture = cvCaptureFromCAM($camera$); \n' + \
            'if( !cvGrabFrame( block$id$_capture ))' + \
            '{ printf("Cannot Grab Image from camera $camera$"); }\n' + \
            'block$id$_frame = cvRetrieveFrame( block$id$_capture ); \n' + \
            'block$id$_img_o0 = cvCloneImage( block$id$_frame );\n' + \
            'counter$id$++;\n' + \
            '}\n'
        self.codes[3] = "cvReleaseImage(&block$id$_img_o0);\n"
# -----------------------------------------------------------------------------
