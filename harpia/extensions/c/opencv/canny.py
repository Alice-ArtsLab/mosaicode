#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Canny class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin


class Canny(Plugin):
    """
    This class contains methods related the Canny class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.help = "Operacão de filtragem que implementa o algoritmo " + \
            "Canny para detecção de contornos e bordas." + \
            "\nPropriedades\nLimiar 1 e Limiar 2: os dois valores" + \
            " de limiar são utilizados em conjunto." + \
            "O menor valor é utilizado para a realizar a " + \
            "conexão de cantos e bordas." + \
            "O maior valor é utilizado para encontrar" + \
            " segmentos iniciais das bordas mais significativas."
        self.label = "Canny"
        self.color = "50:180:80:150"
        self.in_ports = [{"type":"harpia.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"},
                          {"type":"harpia.extensions.c.ports.int",
                          "name":"apertureSize",
                          "label":"Aperture Size"},
                          {"type":"harpia.extensions.c.ports.int",
                          "name":"threshold1",
                          "label":"Threshold 1"},
                          {"type":"harpia.extensions.c.ports.int",
                          "name":"threshold2",
                          "label":"Threshold 2"}
                         ]
        self.out_ports = [{"type":"harpia.extensions.c.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Gradients, Edges and Corners"

        self.properties = [{"label": "Aperture Size",
                            "name": "apertureSize",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 10,
                            "value":3,
                            "step": 1
                            },
                           {"label": "Threshold 1",
                            "name": "threshold1",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 100,
                            "value": 16,
                            "step": 1
                            },
                           {"label": "Threshold 2",
                            "name": "threshold2",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 100,
                            "value": 33,
                            "step": 1
                            }
                           ]

        # -------------------------C/OpenCV code----------------------------
        self.codes[1] = \
            '// $id$ Canny\n' + \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int block$id$_int_i1 = $prop[apertureSize]$;\n' + \
            'int block$id$_int_i2 = $prop[threshold1]$;\n' + \
            'int block$id$_int_i3 = $prop[threshold2]$;\n'

        self.codes[2] = \
            "if(block$id$_img_i0){ //Canny Code\n" + \
            "\tif (block$id$_int_i1 < 1) block$id$_int_i1 = 1;\n" + \
            "\tif (block$id$_int_i2 < 1) block$id$_int_i2 = 1;\n" + \
            "\tif (block$id$_int_i3 < 1) block$id$_int_i3 = 1;\n" + \
            "\tif (block$id$_int_i1 > 10) block$id$_int_i1 = 10;\n" + \
            "\tif (block$id$_int_i2 > 100) block$id$_int_i2 = 100;\n" + \
            "\tif (block$id$_int_i3 > 100) block$id$_int_i3 = 100;\n" + \
            "\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n" + \
            "\tIplImage * tmpImg$id$ =" + \
            " cvCreateImage(cvGetSize(block$id$_img_i0),8,1);\n" + \
            "\tif(block$id$_img_i0->nChannels == 3){\n" + \
            "    \t\tcvCvtColor(block$id$_img_i0," + \
            " tmpImg$id$ ,CV_RGB2GRAY);\n" + \
            "\t}else{\n" + \
            "    \t\ttmpImg$id$ = block$id$_img_i0 = NULL;\n" + \
            "}\n" + \
            "cvCanny(tmpImg$id$, tmpImg$id$, block$id$_int_i2," + \
            " block$id$_int_i1, block$id$_int_i3);\n" + \
            "\tif(block$id$_img_i0->nChannels == 3){\n" + \
            "    \t\tcvCvtColor(tmpImg$id$, " + \
            "block$id$_img_o0,CV_GRAY2RGB);\n" + \
            "\t}else{\n" + \
            "    \t\tcvCopyImage(tmpImg$id$, block$id$_img_o0);\n" + \
            "\t}\n" + \
            "\tcvReleaseImage(&tmpImg$id$);\n" + \
            "} // End Canny Code\n"

        self.codes[3] = "cvReleaseImage(&block$id$_img_i0);\n" + \
                       "cvReleaseImage(&block$id$_img_o0);\n"
        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
