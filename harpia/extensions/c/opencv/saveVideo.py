#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the SaveVideo class.
"""
from harpia.GUI.fieldtypes import *
from harpia.extensions.c.opencv.opencvplugin import OpenCVPlugin


class SaveVideo(OpenCVPlugin):
    """
    This class contains methods related the SaveVideo class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = "~/Output.mpeg"
        self.framerate = 25.0
        self.codecSelection = "MPEG1"

        # Appearance
        self.help = "Save Video needs its description."
        self.label = "Save Video"
        self.color = "120:20:20:150"
        self.in_types = ["harpia.extensions.c.ports.image"]
        self.out_types = ["harpia.extensions.c.ports.image"]
        self.group = "General"

        self.properties = [{"name": "File Name",
                            "label": "filename",
                            "type": HARPIA_SAVE_FILE
                            },
                           {"name": "Frame Rate",
                            "label": "framerate",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 99,
                            "step": 1
                            },
                           {"name": "Encoding Codec",
                            "label": "codecSelection",
                            "type": HARPIA_COMBO,
                            "values": ["MPEG1", "mjpeg", "MPEG4.2", "MPEG4.3",
                                       "MPEG4", "H263", "H263I", "FLV1"]
                            }
                           ]

        # --------------------C/OpenCv code------------------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'CvVideoWriter* block$id$_vidWriter = NULL;\n'

        self.codes[3] = 'cvReleaseImage' + \
            '(&block$id$_img_i0); // SaveVideo Dealloc\n'

        self.codes[4] = 'cvReleaseVideoWriter' + \
            '(&block$id$_vidWriter); // SaveVideo\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        codecMacro = 'CV_FOURCC(\'P\',\'I\',\'M\',\'2\')'
        if self.codecSelection == "MPEG1":
            codecMacro = 'CV_FOURCC(\'P\',\'I\',\'M\',\'2\')'
        if self.codecSelection == "mjpeg":
            codecMacro = 'CV_FOURCC(\'M\',\'J\',\'P\',\'G\')'
        if self.codecSelection == "MPEG4.2":
            codecMacro = 'CV_FOURCC(\'M\',\'P\',\'4\',\'2\')'
        if self.codecSelection == "MPEG4.3":
            codecMacro = 'CV_FOURCC(\'D\',\'I\',\'V\',\'3\')'
        if self.codecSelection == "MPEG4":
            codecMacro = 'CV_FOURCC(\'D\',\'I\',\'V\',\'X\')'
        if self.codecSelection == "H263":
            codecMacro = 'CV_FOURCC(\'U\',\'2\',\'6\',\'3\')'
        if self.codecSelection == "H263I":
            codecMacro = 'CV_FOURCC(\'I\',\'2\',\'6\',\'3\')'
        if self.codecSelection == "FLV1":
            codecMacro = 'CV_FOURCC(\'F\',\'L\',\'V\',\'1\')'
        return \
            '\nif(block$id$_img_i0){\n' + \
            '   if(block$id$_vidWriter == NULL)' + \
            '//video writer not started up yet!\n' + \
            '       block$id$_vidWriter = cvCreateVideoWriter' + \
            '( "$filename$", ' + \
            codecMacro + ',$framerate$' + \
            ', cvGetSize(block$id$_img_i0), 1 );\n' + \
            '   cvWriteFrame( block$id$_vidWriter, block$id$_img_i0);\n' + \
            '   block$id$_img_o0 = block$id$_img_i0;\n' + \
            '}\n'

# ------------------------------------------------------------------------------
