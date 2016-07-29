#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *

class Save():

# ------------------------------------------------------------------------------
    def __init__(self):
        self.file_name = ""
        self.id = -1

# ------------------------------------------------------------------------------
    def get_description(self):
        return {"Id":"01",
                "Label": "Save Image",
                "Path": {"Python": "save"},
                "Icon": "images/save.png",
                "Color": "50:100:200:150",
                "InTypes": {0: "HRP_IMAGE"},
                "OutTypes": {0: "HRP_IMAGE"},
                "Description": "Save image on a file indicated by the user.",
                "TreeGroup": "General"
                }

# ------------------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = \
            'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
            '\nif(block$$_img_i1)\n' + \
            'cvSaveImage("' + self.file_name + '" ,block$$_img_i1);\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

# ------------------------------------------------------------------------------
    def set_properties(self, data):
        self.file_name = data["filename"]

# ------------------------------------------------------------------------------
    def get_properties(self):
        return {"filename":{"name": "File Name",
                            "type": HARPIA_STRING,
                            "value": self.file_name}
                }

# ------------------------------------------------------------------------------
    def get_help(self):
        return "Operacão de filtragem que implementa o algoritmo Canny para detecção de contornos e bordas.\nPropriedades\nLimiar 1 e Limiar 2: os dois valores de limiar são utilizados em conjunto. O menor valor é utilizado para a realizar a conexão de cantos e bordas. O maior valor é utilizado para encontrar segmentos iniciais das bordas mais significativas."

# ------------------------------------------------------------------------------
    def get_xml(self):
        return """
         <properties>
      <block type='01' id='"""+ str(self.id) + """'>
        <property name='filename' value='""" + str(self.file_name) +"""' />
      </block>
        </properties>
    """
# ------------------------------------------------------------------------------
