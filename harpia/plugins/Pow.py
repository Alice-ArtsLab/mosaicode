#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *

class Pow():

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "60"
        self.exponent = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Eleva cada ponto de uma imagem a um valor fixo de potência."
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                'block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width, ' + \
                'block$$_img_i1->height),block$$_img_i1->depth,block$$_img_i1->nChannels);' + \
                '\ncvPow(block$$_img_i1, block$$_img_o1,' + str(self.exponent) + ');}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'
        blockTemplate.functionCall += '\n // Valney esteve aqui \n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type":"41",
            "Label": _("Pow"),
            "Icon": "images/pow.png",
            "Color": "230:230:60:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Power each pixel value to a fixed value."),
            "TreeGroup": _("Math Functions")
            }
    # ----------------------------------------------------------------------
    def set_properties(self, data):
        self.exponent = data["exponent"]

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"exponent":{"name": "Exponent",
                            "type": HARPIA_INT,
                            "value": self.exponent,
                            "lower":1,
                            "upper":10,
                            "step":1
                            }
                }

    # ----------------------------------------------------------------------
    def get_xml(self):
        return """
 <properties>
      <block type='"""+ str(self.type) + """' id='"""+ str(self.id) + """'>
        <property name='exponent' value='""" + str(self.exponent) +"""' />
      </block>
</properties>
    """
# ------------------------------------------------------------------------------

