#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class MatchTem(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.method = 'CV_TM_SQDIFF'
        self.scaleFactor = 6

    # ----------------------------------------------------------------------
    def get_help(self):
        return "operação de filtragem destinada a suavizar uma imagem."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_t0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tdouble width$id$ = block$id$_img_i0->width - block$id$_img_i1->width +1;\n' + \
            '\tdouble height$id$ = block$id$_img_i0->height - block$id$_img_i1->height +1;\n'+ \
            '\tCvSize size$id$ = cvSize(width$id$,height$id$);\n' + \
            '\tblock$id$_img_t0 = cvCreateImage(size$id$,32,1);\n' + \
            '\tblock$id$_img_o0 = cvCreateImage(size$id$,8,1);\n' + \
            '\tcvMatchTemplate(block$id$_img_i0 , block$id$_img_i1, block$id$_img_t0, $method$);\n' + \
            '\tcvConvertScale(block$id$_img_t0, block$id$_img_o0, ' + str(
            10 ** -(int(float(self.scaleFactor)))) + ',0);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return 'cvReleaseImage(&block$id$_img_o0);\n' + \
               'cvReleaseImage(&block$id$_img_t0);\n' + \
               'cvReleaseImage(&block$id$_img_i1);\n' + \
               'cvReleaseImage(&block$id$_img_i0);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Match Template"),
            "Icon": "images/matchTem.png",
            "Color": "180:180:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Output shows the matching relation between image (input1) and template (input2)"),
            "TreeGroup": _("Feature Detection")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

            "scaleFactor":{"name": "Scale Factor",
                    "type": HARPIA_INT,
                    "value": self.scaleFactor,
                    "lower":0,
                    "upper":99,
                    "step":1
                    },

        "method":{"name": "Method",
                    "type": HARPIA_COMBO,
                    "value": self.method,
                    "values": ["CV_TM_CCOEFF_NORMED", "CV_TM_CCOEFF",
                                "CV_TM_CCORR_NORMED", "CV_TM_CCORR",
                                "CV_TM_SQDIFF_NORMED", "CV_TM_SQDIFF"
                    ]
                    }

        }

# ------------------------------------------------------------------------------

