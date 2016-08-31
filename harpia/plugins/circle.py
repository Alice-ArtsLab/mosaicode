#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Circle(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.x0 = 100
        self.y0 = 100
        self.color = "#0000ffff0000"

    # --------------------------Help Text--------------------------------------------
    def get_help(self):#Função que chama a help
        return "Desenha Circulos"

    # ------------------------------------------------------------------------------
    def generate(self, blockTemplate):
        red = self.color[1:5]
        green = self.color[5:9]
        blue = self.color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257

        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'int block$$_int_i2 = ' + str(self.x0) + ';\n' + \
            'int block$$_int_i3 = ' + str(self.y0) + ';\n' 

        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
		'CvPoint center = cvPoint(block$$_int_i2, block$$_int_i3);\n' + \
                'CvScalar color = cvScalar('+ str(blue) +','+ str(green) +','+ str(red) + ',0);\n' + \
		'cvCircle(block$$_img_i1, center, 10, color, 1, 8, 0);\n' +\
		'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
				'}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ------------------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
                "Label": "Circle",
                "Icon": "images/opening.png",
                "Color": "255:0:0:150",
                "InTypes": {0: "HRP_IMAGE", 1:"HRP_INT", 2:"HRP_INT"},
                "OutTypes": {0: "HRP_IMAGE"},
                "Description": "Draw Circles.",
                "TreeGroup": "Basic Shapes"
                }

    # ------------------------------------------------------------------------------
    def get_properties(self):
        return {"x0":{"name": "x0",
                            "type": HARPIA_INT,
                            "value": self.x0,
                            "lower":0,
                            "upper":800,
                            "step":1
                            },
            "y0":{"name": "y0",
                            "type": HARPIA_INT,
                            "value": self.y0,
                            "lower":0,
                            "upper":1000,
                            "step":1
                            },
            "color":{"name": "Color",
                     "type": HARPIA_COLOR,
                     "value": self.color
                    }
                }

# ------------------------------------------------------------------------------
