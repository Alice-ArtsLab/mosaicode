#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *

class Exp():

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "61"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
      return "aplica a função exponencial a uma imagem, ou seja,\
      eleva a constante neperiana ao valor de intensidade luminosa de cada ponto da imagem."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
       blockTemplate.imagesIO = \
                   'IplImage * block$$_img_i1 = NULL;\n' + \
                   'IplImage * block$$_img_o1 = NULL;\n' + \
			      		'IplImage * block$$_img_t = NULL;\n'
       blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                   'block$$_img_t = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), IPL_DEPTH_32F,block$$_img_i1->nChannels);\n'+\
                   'block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height),block$$_img_i1->depth,block$$_img_i1->nChannels);\n' + \
					    'cvConvertScale(block$$_img_i1,block$$_img_t,(1/255.0),0);\n' + \
       				'cvExp(block$$_img_t, block$$_img_t);\n' + \
        				'cvConvertScale(block$$_img_t,block$$_img_o1,(double)93.8092,0);\n}\n'
       blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                   'cvReleaseImage(&block$$_img_i1);\n' + \
                   'cvReleaseImage(&block$$_img_t);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Exp"),
         "Icon":"images/exp.png",
         "Color":"230:230:60:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Return the image made from the neperian constant (e) powered to each one of the image pixels."),
				 "TreeGroup":_("Math Functions")
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

