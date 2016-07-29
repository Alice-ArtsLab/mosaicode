#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *

class Not():

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "40"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Realiza a negação lógica de uma imagem. Corresponde à negativa da imagem."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = "\n //NOT input and output \n"
        blockTemplate.imagesIO += \
            'IplImage * block$$_img_i1 = NULL; // NOT input\n' + \
            'IplImage * block$$_img_o1 = NULL; // NOT output\n'
        blockTemplate.imagesIO += "\n\n"

        blockTemplate.functionCall = "\n\n // NOT Execution Block\n"
        blockTemplate.functionCall += 'if(block$$_img_i1){\n' + \
                                      'block$$_img_o1 = cvCreateImage(cvSize(block$$' + \
                                      '_img_i1->width,block$$_img_i1->height),block$$' + \
                                      '_img_i1->depth,block$$_img_i1->nChannels);\n'
        blockTemplate.functionCall += 'cvNot(block$$_img_i1, block$$_img_o1);\n}\n'

        blockTemplate.dealloc = '// NOT dealloc block '
        blockTemplate.dealloc += 'cvReleaseImage(&block$$_img_o1);\n'
        blockTemplate.dealloc += 'cvReleaseImage(&block$$_img_i1);\n'
        blockTemplate.dealloc = '\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Not"),
            "Icon": "images/not.png",
            "Color": "10:180:10:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Negate the image. It is equivalent to the negative image."),
            "TreeGroup": _("Arithmetic and logical operations")
            }
    # ----------------------------------------------------------------------
    def set_properties(self, data):
        pass

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

    # ----------------------------------------------------------------------
    def get_xml(self):
        return """
 <properties>
      <block type='"""+ str(self.type) + """' id='"""+ str(self.id) + """'>
      </block>
</properties>
    """
# ------------------------------------------------------------------------------
