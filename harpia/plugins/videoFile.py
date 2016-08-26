#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class VideoFile(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "16"
        self.filename = "/usr/share/harpia/images/vLeft.mpg"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Realiza a aquisição de uma imagem a partir de algum dispositivo,\
        seja este uma mídia ou um dispositivo de aquisição de imagens (câmera, scanner)."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):

        blockTemplate.imagesIO = 'CvCapture * block$$_capture = NULL;\n'+ \
                'IplImage * block$$_frame = NULL;\n' + \
                'block$$_capture = cvCreateFileCapture("' + self.filename + '");\n'

        blockTemplate.imagesIO += 'IplImage * block$$_img_o1 = NULL; //Capture\n'

        blockTemplate.functionCall = '// Video Mode \n' + \
                'cvGrabFrame(block$$_capture);\n' + \
                'block$$_frame = cvRetrieveFrame (block$$_capture);\n' + \
                'if(!block$$_frame){\n'+\
                'cvSetCaptureProperty(block$$_capture, CV_CAP_PROP_POS_AVI_RATIO , 0);\n' + \
                'continue;\n' + \
                '}\n' + \
                'block$$_img_o1 = cvCloneImage(block$$_frame);\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n'

        blockTemplate.outDealloc = 'cvReleaseCapture(&block$$_capture);\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Video File"),
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":"",
                 "OutTypes":{0:"HRP_IMAGE"},
                 "Description":_("Create a new image or load image from a source, such as file, camera, frame grabber."),
                 "TreeGroup":_("Image Source"),
                 "IsSource":True
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"filename":{"name": "File Name",
                            "type": HARPIA_OPEN_FILE,
                            "value": self.filename}
                }

# ------------------------------------------------------------------------------
