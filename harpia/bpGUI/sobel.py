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
        
        filename = self.m_sDataDir+'glade/sobel.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'SOBEXOrder',
            'SOBEYOrder',
            'SOBEMaskSize',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
            ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_sobel_confirm_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        self.OrderLimit = 6
        #load properties values
        for Property in self.m_oPropertiesXML.properties.block.property:

            if Property.name == "xorder":
                self.widgets['SOBEXOrder'].set_value( int(Property.value) )
 
            if Property.name == "yorder":
                self.widgets['SOBEYOrder'].set_value( int(Property.value) )

            if Property.name == "masksize":
                if Property.value == "1":
                    self.widgets['SOBEMaskSize'].set_active( int(0) )
                if Property.value == "3":
                    self.widgets['SOBEMaskSize'].set_active( int(1) )
                if Property.value == "5":
                    self.widgets['SOBEMaskSize'].set_active( int(2) )
                if Property.value == "7":
                    self.widgets['SOBEMaskSize'].set_active( int(3) )

        self.configure()

        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/sobel"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['HelpView'].set_buffer( t_oTextBuffer )
        
    #----------------------------------------------------------------------

    def __del__(self):
        
	pass

    #----------------------------------------------------------------------
   
    def on_sobel_confirm_clicked( self, *args ):

        for Property in self.m_oPropertiesXML.properties.block.property:
     
            if Property.name == "masksize":
                Active = self.widgets['SOBEMaskSize'].get_active( )
                if int(Active) == 0:
                    Property.value = unicode("1")
                    self.OrderLimit = 1
                if int(Active) == 1:
                    Property.value = unicode("3")
                    self.OrderLimit = 2
                if int(Active) == 2:
                    Property.value = unicode("5")
                    self.OrderLimit = 4
                if int(Active) == 3:
                    Property.value = unicode("7")
                    self.OrderLimit = 6

					
		#Property.value = unicode( str( int(self.widgets['SOBEXOrder'].get_value( )) ) )
            if Property.name == "xorder":                
                Value = self.widgets['SOBEXOrder'].get_value( )
                if (Value >= self.OrderLimit):
                    Value = self.OrderLimit
                Property.value = unicode( str( int(Value) ) ) 

            if Property.name == "yorder":                
                Value = self.widgets['SOBEYOrder'].get_value( )
                if (Value >= self.OrderLimit):
                    Value = self.OrderLimit
                Property.value = unicode( str( int(Value) ) ) 
                                
        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

#SobelProperties = Properties()
#SobelProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
   for propIter in blockTemplate.properties:
       if propIter[0] == 'xorder':
           xOrderValue = propIter[1]
       if propIter[0] == 'yorder':
           yOrderValue = propIter[1]
       if propIter[0] == 'masksize':
           masksizeValue = propIter[1]
   blockTemplate.imagesIO = \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n' + \
                 'IplImage * block' + blockTemplate.blockNumber + '_img_t = NULL;\n'
   blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                     'block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                      '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_32F,block'+ \
	    blockTemplate.blockNumber + '_img_i1->nChannels);\n'+\
                     'cvSobel(block' + blockTemplate.blockNumber + '_img_i1, block' + blockTemplate.blockNumber + '_img_o1 ,' + xOrderValue +','+ yOrderValue +','+masksizeValue+' );}\n'
   blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                  'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t);\n'

# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
	return {"Label":_("Sobel"),
         "Path":{"Python":"sobel",
                 "Glade":"glade/sobel.ui",
                 "Xml":"xml/sobel.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/sobel.png",
         "Color":"250:180:80:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Filtering operation that uses the Sobel mask to enhance edges on the image."),
				 "TreeGroup":_("Gradients, Edges and Corners")
         }
