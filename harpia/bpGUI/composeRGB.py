# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
#----------------------------------------------------------------------

from harpia.GladeWindow import GladeWindow
from harpia.amara import binderytools as bt
import gtk
from harpia.s2icommonproperties import S2iCommonProperties, APP, DIR
#i18n
import os
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#----------------------------------------------------------------------
   
class Properties( GladeWindow, S2iCommonProperties ):

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/composeRGB.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
            ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_composeRGB_confirm_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        self.configure()

        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/composeRGB"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['HelpView'].set_buffer( t_oTextBuffer )

    #----------------------------------------------------------------------

    def __del__(self):
        
	pass

    #----------------------------------------------------------------------
   
    def on_composeRGB_confirm_clicked( self, *args ):

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()

            
    #----------------------------------------------------------------------
  
#ComposeRGBProperties = Properties()
#ComposeRGBProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
   blockTemplate.imagesIO = \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_i2 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_i3 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_t1 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_t2 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_t3 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
   blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                     'block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                      '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + '_img_i1->depth, block' + \
                      blockTemplate.blockNumber + '_img_i1->nChannels);\n'+\
                      'block' + blockTemplate.blockNumber + '_img_t1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                      '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + '_img_i1->depth, 1);\n'+\
                      'block' + blockTemplate.blockNumber + '_img_t2 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                      '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + '_img_i1->depth, 1);\n'+\
                      'block' + blockTemplate.blockNumber + '_img_t3 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                      '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + '_img_i1->depth, 1);\n'+\
                      'cvSplit(block' + blockTemplate.blockNumber + '_img_i1 ,block' + blockTemplate.blockNumber + '_img_t1  ,NULL, NULL , NULL);\n' + \
                      'cvSplit(block' + blockTemplate.blockNumber + '_img_i2 ,NULL ,block' + blockTemplate.blockNumber + '_img_t2, NULL, NULL);\n' + \
                      'cvSplit(block' + blockTemplate.blockNumber + '_img_i3 ,NULL ,NULL, block' + blockTemplate.blockNumber + '_img_t3 , NULL);\n' + \
                      'cvMerge(block' + blockTemplate.blockNumber + '_img_t3 ,block' + blockTemplate.blockNumber + '_img_t2 ,block'+ blockTemplate.blockNumber + '_img_t1 , NULL, block'+ \
                      blockTemplate.blockNumber + '_img_o1);}\n'
   blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t1);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t2);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t3);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i2);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i3);\n'

# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
	return {"Label":_("Compose RGB"),
         "Path":{"Python":"composeRGB",
                 "Glade":"glade/composeRGB.ui",
                 "Xml":"xml/composeRGB.xml"},
         "Inputs":3,
         "Outputs":1,
         "Icon":"images/composeRGB.png",
         "Color":"50:125:50:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE",2:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Compose three color channels  (R, G and B)  into one color image."),
				 "TreeGroup":_("Filters and Color Conversion")
         }
