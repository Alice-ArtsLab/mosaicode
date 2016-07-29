#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *

class Show():

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "02"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Mostra uma imagem da cadeia de processamento de imagens."
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        import harpia.gerador
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        if (len(harpia.gerador.g_bLive) > 0):
            blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                             'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
                             'cvNamedWindow("block$$_img_o1",CV_WINDOW_AUTOSIZE );\n' + \
                             'cvShowImage("block$$_img_o1",block$$_img_i1);\n} \n'
        else:
            blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                            'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
                            'cvSaveImage("block$$_OUT.png" ,block$$_img_i1);\n}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Show Image"),
            "Icon": "images/show.png",
            "Color": "50:100:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Shows the input image on a new window."),
            "TreeGroup": _("General")
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

