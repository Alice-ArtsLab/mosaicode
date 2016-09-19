#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Canny(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.apertureSize = 3
        self.threshold1 = 16
        self.threshold2 = 33

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Operacão de filtragem que implementa o algoritmo Canny para detecção de contornos e bordas.\nPropriedades\nLimiar 1 e Limiar 2: os dois valores de limiar são utilizados em conjunto. O menor valor é utilizado para a realizar a conexão de cantos e bordas. O maior valor é utilizado para encontrar segmentos iniciais das bordas mais significativas."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i1 = NULL;\n'+ \
            'IplImage * block$id$_img_o1 = NULL;\n' + \
            'int block$id$_int_i2 = $threshold2$;\n' + \
            'int block$id$_int_i4 = $apertureSize$;\n' + \
            'int block$id$_int_i3 = $threshold1$;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        self.apertureSize = int(self.apertureSize)
        self.threshold1 = int(self.threshold1)
        self.threshold2 = int(self.threshold2)
        return  '''
if(block$id$_img_i1){ //Canny Code
    if (block$id$_int_i2 < 1) block$id$_int_i2 = 1;
    if (block$id$_int_i3 < 1) block$id$_int_i3 = 1;
    if (block$id$_int_i4 < 1) block$id$_int_i4 = 1;
    if (block$id$_int_i2 > 10) block$id$_int_i2 = 10;
    if (block$id$_int_i3 > 100) block$id$_int_i3 = 100;
    if (block$id$_int_i4 > 100) block$id$_int_i4 = 100;
    block$id$_img_o1 = cvCloneImage(block$id$_img_i1);
    IplImage * tmpImg$id$ = cvCreateImage(cvGetSize(block$id$_img_i1),8,1);
    if(block$id$_img_i1->nChannels == 3){
        cvCvtColor(block$id$_img_i1,tmpImg$id$ ,CV_RGB2GRAY);
    }else{
        tmpImg$id$ = block$id$_img_i1 = NULL;
    }
    cvCanny(tmpImg$id$, tmpImg$id$, block$id$_int_i3, block$id$_int_i2, block$id$_int_i4);
    if(block$id$_img_i1->nChannels == 3){
        cvCvtColor(tmpImg$id$, block$id$_img_o1,CV_GRAY2RGB);
    }else{
        cvCopyImage(tmpImg$id$, block$id$_img_o1);
    }
    cvReleaseImage(&tmpImg$id$);
} // End Canny Code
'''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Canny"),
            "Icon": "images/canny.png",
            "Color": "250:180:80:150",
            "InTypes": {0: "HRP_IMAGE", 1:"HRP_INT", 2:"HRP_INT", 3:"HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Filtering operation that employs the Canny algorithm to detect edges."),
            "TreeGroup": _("Gradients, Edges and Corners")
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
