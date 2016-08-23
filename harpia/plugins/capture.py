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
class Capture(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "18"
        self.camera = "/dev/video0"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Realiza a aquisição de uma imagem a partir de algum dispositivo,\
        seja este uma mídia ou um dispositivo de aquisição de imagens (câmera, scanner)."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        camera = self.camera[10:]


        blockTemplate.imagesIO = 'IplImage * block$$_img_o1 = NULL; //Capture\n' + \
           'CvCapture* block$$_capture = NULL; \n' + \
           'IplImage* block$$_frame = NULL; \n' + \
           'int counter = 0;\n'
           
        blockTemplate.functionCall = \
           'if (counter == 0){\n' + \
           'block$$_capture = cvCaptureFromCAM(' + camera + '); \n' + \
           'if( !cvGrabFrame( block$$_capture ) ) \n{ printf("Cannot Grab Image from camera '+ camera +'"); }\n' + \
           'block$$_frame = cvRetrieveFrame( block$$_capture ); \n' + \
           'block$$_img_o1 = cvCloneImage( block$$_frame );\n' + \
           'counter++;\n' + \
           '}\n'

        blockTemplate.outDeallocations = 'cvReleaseImage(&block$$_img_o1);\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Capture"),
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":"",
                 "OutTypes":{0:"HRP_IMAGE"},
                 "Description":_("Create a new image from a camera."),
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
