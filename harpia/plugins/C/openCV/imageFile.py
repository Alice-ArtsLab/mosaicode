#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class ImageFile(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = "/usr/share/harpia/images/lenna.png"

        # Appearance
        self.help = "Realiza a aquisição de uma imagem a " + \
            "partir de algum dispositivo, " + \
            "seja este uma mídia ou um dispositivo de " + \
            "aquisição de imagens (câmera, scanner)."
        self.label = "Image File"
        self.icon = "images/acquisition.png"
        self.color = "50:100:200:150"
        self.out_types = ["HRP_IMAGE"]
        self.group = "Image Source"

        self.properties = {
            "filename": {
                "name": "File Name",
                "type": HARPIA_OPEN_FILE
            }
        }

        # ----------------------------C/OpenCv code-------------------------
        self.vars = 'IplImage * block$id$_img_o0 = NULL;\n'
        self.vars += 'block$id$_img_o0 = cvLoadImage("$filename$",-1);\n'
        self.out_dealloc = "cvReleaseImage(&block$id$_img_o0);\n"

# -----------------------------------------------------------------------------
