#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin
import os
from glob import glob
class LiveMode(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "17"
        self.camera = "/dev/video0"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Realiza a aquisição de uma imagem a partir de câmera."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        import harpia.gerador
        camera = self.camera[10:]
        tmpPack = [] #contendo [ blockNumber , camNum ]
        tmpPack.append(blockTemplate.plugin.id)
        harpia.gerador.g_bLive.append(tmpPack)

        blockTemplate.imagesIO += 'CvCapture * block$$_capture = NULL;\n' + \
                'IplImage * block$$_frame = NULL;\n' + \
                'block$$_capture = cvCaptureFromCAM(' + camera + ');\n'

        blockTemplate.imagesIO += 'IplImage * block$$_img_o1 = NULL; //Capture\n'

        blockTemplate.functionCall = '// Live Mode \n' + \
           'block$$_img_o1 = cvCloneImage( block$$_frame );\n'

        blockTemplate.outDealloc += 'cvReleaseCapture(&block$$_capture);\n'


        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Live Mode"),
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":"",
                 "OutTypes":{0:"HRP_IMAGE"},
                 "Description":_("Load image from a camera."),
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
