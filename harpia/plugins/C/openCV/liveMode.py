#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin
import os
from glob import glob
class LiveMode(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.camera = "/dev/video0"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Realiza a aquisição de uma imagem a partir de câmera."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        camera = self.camera[10:]

        return \
             '// Live Mode Cam \n' + \
             'CvCapture * block$id$_capture = NULL;\n' + \
             'block$id$_capture = cvCaptureFromCAM(' + camera + ');\n' + \
             'IplImage * block$id$_frame = NULL;\n' + \
             'IplImage * block$id$_img_o0 = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '// Live Mode \n' + \
            'int value = cvGrabFrame(block$id$_capture);\n' + \
            'block$id$_frame = cvRetrieveFrame(block$id$_capture);\n' + \
            'if(!block$id$_frame){\ncontinue;\n}\n'+\
            'block$id$_img_o0 = cvCloneImage(block$id$_frame);\n'

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return 'cvReleaseCapture(&block$id$_capture);\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label":_("Live Mode"),
                "Icon":"images/acquisition.png",
                "Color":"50:100:200:150",
                "InTypes":"",
                "OutTypes":{0:"HRP_IMAGE"},
                "TreeGroup":_("Image Source"),
                "IsSource":True
         }

    # ----------------------------------------------------------------------
    def get_properties(self):

        available_cams = 4
        device_list = []

        if os.name == 'posix':
            device_list = glob("/dev/video*")

        return {
        "camera":{"name": "Camera",
                    "type": HARPIA_COMBO,
                    "value": self.camera,
                    "values": device_list
                    }
               }
# ------------------------------------------------------------------------------
