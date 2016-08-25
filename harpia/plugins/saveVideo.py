#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class SaveVideo(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "11"
        self.filename = "~/Output.mpeg"
        self.framerate = 25.0
        self.codecSelection = "MPEG1"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Save Video needs its description"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
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

        blockTemplate.imagesIO = 'IplImage * block$$_img_i1 = NULL;\n' + \
                                 'IplImage * block$$_img_o1 = NULL;\n' + \
                                 'CvVideoWriter* block$$_vidWriter = NULL;\n'

        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     '	if(block$$_vidWriter == NULL)//video writer not started up yet!\n' + \
                                     '		block$$_vidWriter = cvCreateVideoWriter( "' + self.filename + '", ' + codecMacro + ',' + self.frameRate + ', cvGetSize(block$$_img_i1), 1 );\n' + \
                                     '	cvWriteFrame( block$$_vidWriter, block$$_img_i1);\n' + \
                                     '	block$$_img_o1 = block$$_img_i1;\n' + \
                                     '}\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_i1); // SaveVideo Dealloc\n'

        blockTemplate.outDealloc = 'cvReleaseVideoWriter(&block$$_vidWriter); // SaveVideo\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Save Video'),
            'Icon': 'images/saveVideo.png',
            'Color': '120:20:20:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'Description': _('Save Video needs its description'),
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
