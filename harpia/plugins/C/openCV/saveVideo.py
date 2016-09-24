#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class SaveVideo(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = "~/Output.mpeg"
        self.framerate = 25.0
        self.codecSelection = "MPEG1"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Save Video needs its description"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'CvVideoWriter* block$id$_vidWriter = NULL;\n'

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
            '	if(block$id$_vidWriter == NULL)//video writer not started up yet!\n' + \
            '		block$id$_vidWriter = cvCreateVideoWriter( "$filename$", ' + \
            codecMacro + ',$framerate$' + \
            ', cvGetSize(block$id$_img_i0), 1 );\n' + \
            '	cvWriteFrame( block$id$_vidWriter, block$id$_img_i0);\n' + \
            '	block$id$_img_o0 = block$id$_img_i0;\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return 'cvReleaseImage(&block$id$_img_i0); // SaveVideo Dealloc\n'

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return 'cvReleaseVideoWriter(&block$id$_vidWriter); // SaveVideo\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': _('Save Video'),
            'Icon': 'images/saveVideo.png',
            'Color': '120:20:20:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'TreeGroup': _('General')
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
                "filename":{"name": "File Name",
                            "type": HARPIA_SAVE_FILE,
                            "value": self.filename},

            "framerate":{"name": "Frame Rate",
                    "type": HARPIA_INT,
                    "value": self.framerate,
                    "lower":1,
                    "upper":99,
                    "step":1
                    },

        "codecSelection":{"name": "Encoding Codec",
                    "type": HARPIA_COMBO,
                    "value": self.codecSelection,
                    "values": ["MPEG1", "mjpeg", "MPEG4.2", "MPEG4.3", "MPEG4", "H263", "H263I", "FLV1"]
                    }

        }

# ------------------------------------------------------------------------------
