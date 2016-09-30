#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class ImageFile(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = "/usr/share/harpia/images/lenna.png"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Realiza a aquisição de uma imagem a partir de algum dispositivo,\
        seja este uma mídia ou um dispositivo de aquisição de imagens (câmera, scanner)."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return OpenCVPlugin.generate_vars(self) + 'block$id$_img_o0 = cvLoadImage("$filename$",-1);\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""
        
    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return "cvReleaseImage(&block$id$_img_o0);\n"

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label":"Image File",
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
         "InTypes":"",
         "OutTypes":{0:"HRP_IMAGE"},
         "TreeGroup":"Image Source"
         }


    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"filename":{"name": "File Name",
                            "type": HARPIA_OPEN_FILE,
                            "value": self.filename}
                }
# ------------------------------------------------------------------------------
