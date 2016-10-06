#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin
import os
from glob import glob

class Capture(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
      OpenCVPlugin.__init__(self)
      self.camera = "/dev/video0"
      self.help = "Realiza a aquisição de uma imagem a partir de algum dispositivo," + \
     " seja este uma mídia ou um dispositivo de aquisição de imagens (câmera, scanner)."

      self.description = {
          "Label":"Capture",
          "Icon":"images/acquisition.png",
          "Color":"50:100:200:150",
          "InTypes":"",
          "OutTypes":{0:"HRP_IMAGE"},
          "TreeGroup":"Image Source"
      }

      self.properties = {
          "Label":"Capture",
          "Icon":"images/acquisition.png",
          "Color":"50:100:200:150",
          "InTypes":"",
          "OutTypes":{0:"HRP_IMAGE"},
          "TreeGroup":"Image Source"
      }

      #---------------------C/OpenCv code-------------------------------------
      self.vars = \
           'IplImage * block$id$_img_o0 = NULL; //Capture\n' + \
           'CvCapture* block$id$_capture = NULL; \n' + \
           'IplImage* block$id$_frame = NULL; \n' + \
           'int counter$id$ = 0;\n'

      self.function_call = ""

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description 

    # ----------------------------------------------------------------------
    def get_properties(self):
        available_cams = 4
        device_list = []

        if os.name == 'posix':
            device_list = glob("/dev/video*")

        return self.properties

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        camera = self.camera[10:]
        return \
           'if (counter$id$ == 0){\n' + \
           'block$id$_capture = cvCaptureFromCAM(' + camera + '); \n' + \
           'if( !cvGrabFrame( block$id$_capture )){ printf("Cannot Grab Image from camera '+ camera +'"); }\n' + \
           'block$id$_frame = cvRetrieveFrame( block$id$_capture ); \n' + \
           'block$id$_img_o0 = cvCloneImage( block$id$_frame );\n' + \
           'counter$id$++;\n' + \
           '}\n'

# ------------------------------------------------------------------------------
