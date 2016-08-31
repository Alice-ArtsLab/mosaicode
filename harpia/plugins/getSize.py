#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class GetSize(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Extracts the input image size"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = 'IplImage * block$$_img_i1 = NULL;\n' + \
                                 'CvRect block$$_rect_o1 = cvRect( 0, 0, 1, 1);\n'

        blockTemplate.functionCall = '\nif(block$$_img_i1)\n{\n' + \
                                     '	block$$_rect_o1 = cvRect( 0, 0, block$$_img_i1->width, block$$_img_i1->height);\n' + \
                                     '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Get Size'),
            'Icon': 'images/getSize.xpm',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_RECT'},
            'Description': _('Extracts the input image size'),
            'TreeGroup': _('Experimental'),
            'TimeShifts': False
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

