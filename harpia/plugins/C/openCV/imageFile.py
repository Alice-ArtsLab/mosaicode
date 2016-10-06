#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class ImageFile(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = "/usr/share/harpia/images/lenna.png"

        self.help = "Realiza a aquisição de uma imagem a partir de algum dispositivo," + \
        " seja este uma mídia ou um dispositivo de aquisição de imagens (câmera, scanner)."
        
        self.description = {
            "Label":"Image File",
            "Icon":"images/acquisition.png",
            "Color":"50:100:200:150",
            "InTypes":"",
            "OutTypes":{0:"HRP_IMAGE"},
            "TreeGroup":"Image Source"
        }
        
        self.properties = {
            "filename":{
                "name": "File Name",
                "type": HARPIA_OPEN_FILE
            }
        }

        #------------------------------C/OpenCv code---------------------------
        self.vars = 'block$id$_img_o0 = cvLoadImage("$filename$",-1);\n'

        self.function_call = ""
        
        self.dealloc = ""

        self.out_dealloc = "cvReleaseImage(&block$id$_img_o0);\n"


    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties 

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return OpenCVPlugin.generate_vars(self) + self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc
        
    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return self.out_dealloc

# ------------------------------------------------------------------------------
