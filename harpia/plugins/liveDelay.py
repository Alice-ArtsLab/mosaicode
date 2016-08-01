#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class LiveDelay(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = ""
        self.frameNumber = 5

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Inserts a delay inside a live stream"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = 'IplImage * block$$_img_i1 = NULL;\n' + \
                                 'IplImage * block$$_img_o1 = NULL;\n' + \
                                 'int block$$_t_idx = 0;\n' + \
                                 'IplImage * block$$_buffer[' + str(self.frameNumber) + '] = {'
        for idx in range(self.frameNumber):
            blockTemplate.imagesIO += 'NULL'
            if idx <> self.frameNumber - 1:
                blockTemplate.imagesIO += ','
        blockTemplate.imagesIO += '};\n'

        for idx in range(self.frameNumber):
            blockTemplate.imagesIO += 'block$$_buffer[' + str(
                idx) + '] = cvCreateImage( cvSize(640,480), 8, 3);\n'
            blockTemplate.imagesIO += 'cvSetZero(block$$_buffer[' + str(idx) + ']);\n'

        blockTemplate.imagesIO += 'block$$_img_o1 = block$$_buffer[' + str(self.frameNumber - 1) + '];\n'

        blockTemplate.functionCall = '\nif(block$$_img_i1)\n{\n' + \
                                     '	cvReleaseImage(&(block$$_buffer[block$$_t_idx]));\n' + \
                                     '	block$$_buffer[block$$_t_idx] = cvCloneImage(block$$_img_i1);\n' + \
                                     '	block$$_t_idx++;\n' + \
                                     '	block$$_t_idx %= ' + str(self.frameNumber) + ';\n' + \
                                     '	block$$_img_o1 = block$$_buffer[block$$_t_idx];\n' + \
                                     '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_i1);\n'
        blockTemplate.outDealloc = 'for(block$$_t_idx=0;block$$_t_idx<' + str(
            self.frameNumber) + ';block$$_t_idx++)\n' + \
                                   '	if(block$$_buffer[block$$_t_idx] != NULL)\n' + \
                                   '		cvReleaseImage(&(block$$_buffer[block$$_t_idx]));\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Live Delay'),
            'Icon': 'images/liveDelay.png',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'Description': _('Inserts a delay inside a live stream'),
            'TreeGroup': _('General'),
            'TimeShifts': True
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "frameNumber":{"name": "Time (in frames)",
                        "type": HARPIA_INT,
                        "value": self.frameNumber,
                        "lower":1,
                        "upper":200,
                        "step":1
                            }
        }

# ------------------------------------------------------------------------------

