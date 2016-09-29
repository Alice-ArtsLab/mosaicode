#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Canny(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.apertureSize = 3
        self.threshold1 = 16
        self.threshold2 = 33

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Operacão de filtragem que implementa o algoritmo Canny para detecção de contornos e bordas.\nPropriedades\nLimiar 1 e Limiar 2: os dois valores de limiar são utilizados em conjunto. O menor valor é utilizado para a realizar a conexão de cantos e bordas. O maior valor é utilizado para encontrar segmentos iniciais das bordas mais significativas."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n'+ \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int block$id$_int_i1 = $threshold2$;\n' + \
            'int block$id$_int_i3 = $apertureSize$;\n' + \
            'int block$id$_int_i2 = $threshold1$;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        self.apertureSize = int(self.apertureSize)
        self.threshold1 = int(self.threshold1)
        self.threshold2 = int(self.threshold2)
        return  '''
if(block$id$_img_i0){ //Canny Code
    if (block$id$_int_i1 < 1) block$id$_int_i1 = 1;
    if (block$id$_int_i2 < 1) block$id$_int_i2 = 1;
    if (block$id$_int_i3 < 1) block$id$_int_i3 = 1;
    if (block$id$_int_i1 > 10) block$id$_int_i1 = 10;
    if (block$id$_int_i2 > 100) block$id$_int_i2 = 100;
    if (block$id$_int_i3 > 100) block$id$_int_i3 = 100;
    block$id$_img_o0 = cvCloneImage(block$id$_img_i0);
    IplImage * tmpImg$id$ = cvCreateImage(cvGetSize(block$id$_img_i0),8,1);
    if(block$id$_img_i0->nChannels == 3){
        cvCvtColor(block$id$_img_i0, tmpImg$id$ ,CV_RGB2GRAY);
    }else{
        tmpImg$id$ = block$id$_img_i0 = NULL;
    }
    cvCanny(tmpImg$id$, tmpImg$id$, block$id$_int_i2, block$id$_int_i1, block$id$_int_i3);
    if(block$id$_img_i0->nChannels == 3){
        cvCvtColor(tmpImg$id$, block$id$_img_o0,CV_GRAY2RGB);
    }else{
        cvCopyImage(tmpImg$id$, block$id$_img_o0);
    }
    cvReleaseImage(&tmpImg$id$);
} // End Canny Code
'''

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Canny",
            "Icon": "images/canny.png",
            "Color": "250:180:80:150",
            "InTypes": {0: "HRP_IMAGE", 1:"HRP_INT", 2:"HRP_INT", 3:"HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Gradients, Edges and Corners"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"apertureSize":{"name": "Aperture Size",
                            "type": HARPIA_INT,
                            "value": self.apertureSize,
                            "lower":1,
                            "upper":10,
                            "step":1
                            },
            "threshold1":{"name": "Threshold 1",
                            "type": HARPIA_INT,
                            "value": self.threshold1,
                            "lower":1,
                            "upper":100,
                            "step":1
                            },
            "threshold2":{"name": "Threshold 2",
                            "type": HARPIA_INT,
                            "value": self.threshold2,
                            "lower":1,
                            "upper":100,
                            "step":1
                            }
                }

# ------------------------------------------------------------------------------
