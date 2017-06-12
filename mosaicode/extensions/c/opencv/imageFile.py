#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ImageFile class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class ImageFile(Plugin):
    """
    This class contains methods related the ImageFile class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.help = "Realiza a aquisição de uma imagem a " + \
            "partir de algum dispositivo, " + \
            "seja este uma mídia ou um dispositivo de " + \
            "aquisição de imagens (câmera, scanner)."
        self.label = "Image File"
        self.color = "50:100:200:150"
        self.out_ports = [{"type":"mosaicode.extensions.c.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Image Source"

        self.properties = [{"label": "File Name",
                            "name": "filename",
                            "type": MOSAICODE_OPEN_FILE,
                            "value":"/usr/share/mosaicode/images/lenna.png"
                            }
                           ]

        # ----------------------------C/OpenCv code-------------------------
        self.codes[1] = 'IplImage * block$id$_img_o0 = NULL;\n'
        self.codes[1] += 'block$id$_img_o0 = cvLoadImage("$prop[filename]$",-1);\n'
        self.codes[4] = "cvReleaseImage(&block$id$_img_o0);\n"


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
