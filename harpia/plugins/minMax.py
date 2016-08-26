#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class MinMax(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "606"
        self.minX = 0
        self.maxX = 500
        self.minY = 0
        self.maxY = 500
        self.minVal = 0
        self.maxVal = 500
        self.minORmax = "min"
        self.criteria = "pos"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Finds min or max from input image and judges it according to a custom criteria."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'double block$$_double_o1;\n' + \
            'CvPoint block$$_point_o2 = cvPoint(0,0);\n'

        blockTemplate.functionCall = '\nif(block$$_img_i1)\n{\n' + \
                            '	double minVal,maxVal;\n' + \
                            '	CvPoint minP,maxP;\n' + \
                            '	block$$_double_o1 = 0;\n' + \
                            '	cvMinMaxLoc(block$$_img_i1, &minVal, &maxVal, &minP, &maxP, NULL);\n'
        if self.minORmax == 'max':
            blockTemplate.functionCall += '	minP = maxP;\n' + \
                    '	minVal = maxVal;\n'

        blockTemplate.functionCall += '	block$$_point_o2 = minP;\n'

        if self.criteria == "pos":
            blockTemplate.functionCall += '	if(minP.x >= ' + str(self.minX) + \
                        ' && minP.x <= ' + str(self.maxX) + ')\n' + \
                        '        if(minP.y >= ' + str(self.minY) + \
                        ' && minP.y <= ' + str(self.maxY) + ')\n' + \
                        '        	block$$_double_o1 = 1.0;\n'
        elif self.criteria == "val":
            blockTemplate.functionCall += '	if(minVal >= ' + str(self.minVal) + \
                        ' && minVal <= ' + str(self.maxVal) + ')\n' + \
                        '        block$$_double_o1 = 1.0;\n'
        blockTemplate.functionCall += '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Find Min or Max"),
            "Icon": "images/minMax.png",
            "Color": "50:50:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_DOUBLE", 1: "HRP_POINT"},
            "Description": _("Finds min or max from input image and judges it according to a custom criteria."),
            "TreeGroup": _("Feature Detection")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        
        "minX":{"name": "Min X",
                    "type": HARPIA_INT,
                    "value": self.minX,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },

        "maxX":{"name": "Max X",
                    "type": HARPIA_INT,
                    "value": self.maxX,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },

        "minY":{"name": "Min Y",
                    "type": HARPIA_INT,
                    "value": self.minY,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },

        "maxY":{"name": "Max Y",
                    "type": HARPIA_INT,
                    "value": self.maxY,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },

        "minVal":{"name": "Min Val",
                    "type": HARPIA_INT,
                    "value": self.minVal,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },

        "maxVal":{"name": "Max Val",
                    "type": HARPIA_INT,
                    "value": self.maxVal,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },

        "minORmax":{"name": "Min Or Max",
                    "type": HARPIA_COMBO,
                    "value": self.minORmax,
                    "values": ["min", "max"]
                    },

        "criteria":{"name": "Criteria",
                    "type": HARPIA_COMBO,
                    "value": self.criteria,
                    "values": ["pos", "val"]
                    }
        }

# ------------------------------------------------------------------------------
