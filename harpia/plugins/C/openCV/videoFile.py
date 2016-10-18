#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class VideoFile(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = "/usr/share/harpia/images/vLeft.mpg"
        self.key = 'a'

        self.help = "Realiza a aquisição de uma imagem a partir " + \
            "de algum dispositivo," + \
            "seja este uma mídia ou um dispositivo " + \
            "de aquisição de imagens (câmera, scanner)."

        self.description = {
            "Label": "Video File",
            "Icon": "images/acquisition.png",
            "Color": "50:100:200:150",
            "InTypes": "",
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Image Source"
        }

        self.properties = {
            "filename": {
                "name": "File Name",
                "type": HARPIA_OPEN_FILE
            },
            "key": {
                "name": "Reset Key",
                "type": HARPIA_STRING
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'CvCapture * block$id$_capture = NULL;\n' + \
            'IplImage * block$id$_frame = NULL;\n' + \
            'block$id$_capture = cvCreateFileCapture("$filename$");\n' + \
            'IplImage * block$id$_img_o0 = NULL; //Capture\n'

        self.function_call = \
            '// Video Mode \n' + \
            'if(key == \'$key$\'){\n' +\
            '\tcvSetCaptureProperty(block$id$_capture, ' + \
            'CV_CAP_PROP_POS_AVI_RATIO , 0);\n' + \
            '}\n' + \
            'cvGrabFrame(block$id$_capture);\n' + \
            'block$id$_frame = cvRetrieveFrame (block$id$_capture);\n' + \
            'if(!block$id$_frame){\n' +\
            '\tcvSetCaptureProperty(block$id$_capture, ' + \
            'CV_CAP_PROP_POS_AVI_RATIO , 0);\n' + \
            '\tcontinue;\n' + \
            '}\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_frame);\n'

        self.out_dealloc = 'cvReleaseCapture(&block$id$_capture);\n'

# -----------------------------------------------------------------------------
