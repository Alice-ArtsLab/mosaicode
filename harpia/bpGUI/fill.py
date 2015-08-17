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
from harpia.utils.XMLUtils import XMLParser
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#----------------------------------------------------------------------
   
class Properties( GladeWindow, S2iCommonProperties ):

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/fill.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'FILLFillColor'
            ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_FILLFillColorButton_clicked',
            'on_cancel_clicked',
            'on_fill_confirm_clicked'
            ]

        top_window = 'Properties'

        self.m_oFillColor = [0,0,0]

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        

        #load block color
        self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()
        
        #load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        for Property in self.block_properties:

            #self.widgets['FILLBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
            
            name = Property.getAttr("name")
            value = Property.getAttr("value")
            
            if name == "red":
                self.m_oBackColor[0] = float(value)
                self.m_oFillColor[0] = float(value)
                
            if name == "green":
                self.m_oBackColor[1] = float(value)
                self.m_oFillColor[1] = float(value)
                
            if name == "blue":
                self.m_oBackColor[2] = float(value)
                self.m_oFillColor[2] = float(value)

        t_nBackRed   = self.m_oBackColor[0] * 257
        t_nBackGreen = self.m_oBackColor[1] * 257
        t_nBackBlue  = self.m_oBackColor[2] * 257

        t_oBackColor = gtk.gdk.Color(red=int(t_nBackRed),green=int(t_nBackGreen),blue=int(t_nBackBlue))


        self.configure()
        
        #########################
        # Sets the Fill Color the same as the background color in inicialization
        self.widgets['FILLFillColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)

        #load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir+"help/fill"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.getTag("help").getTag("content").getTagContent()) ) )
    
        self.widgets['HelpView'].set_buffer( t_oTextBuffer )

    #----------------------------------------------------------------------

    def __del__(self):
      pass

    #----------------------------------------------------------------------

    def on_fill_confirm_clicked( self, *args ):

        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "red":
                Property.setAttr("value", unicode(self.m_oFillColor[0]))

            if name == "green":
                Property.setAttr("value",unicode(self.m_oFillColor[1]))

            if name == "blue":
                Property.setAttr("value",unicode(self.m_oFillColor[2]))

        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )
        
        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()

            
    #----------------------------------------------------------------------

    def on_FILLFillColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            # Updates both the Back color and the fill color
            self.widgets['BackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
            self.widgets['FILLFillColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
            
            self.m_oFillColor[0] = t_oColor.red / 257
            self.m_oFillColor[1] = t_oColor.green / 257
            self.m_oFillColor[2] = t_oColor.blue / 257
            
            # Sets the back color the same as the color selected for filling
            self.m_oBackColor[0] = t_oColor.red / 257
            self.m_oBackColor[1] = t_oColor.green / 257
            self.m_oBackColor[2] = t_oColor.blue / 257

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
	for propIter in blockTemplate.properties:
		if propIter[0] == 'red':
			red = propIter[1]
		elif propIter[0] == 'green':
			green = propIter[1]
		elif propIter[0] == 'blue':
			blue = propIter[1]
	blockTemplate.imagesIO = \
		'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
		'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
	blockTemplate.functionCall = \
		'\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
		'block' + blockTemplate.blockNumber + '_img_o1 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_i1);\n' + \
		'\nCvScalar color = cvScalar('+blue +','+ green +','+ red+',0);\n' + \
		'\ncvSet(block' + blockTemplate.blockNumber + '_img_o1,color,NULL);}\n'
	blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
      'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'

# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
	return {"Label":_("Fill image"),
      "Path":{"Python":"fill",
              "Glade":"glade/fill.ui",
              "Xml":"xml/fill.xml"},
      "Inputs":1,
      "Outputs":1,
      "Icon":"images/fill.png",
      "Color":"50:100:200:150",
			 "InTypes":{0:"HRP_IMAGE"},
			 "OutTypes":{0:"HRP_IMAGE"},
			 "Description":_("Fill an image with the desired color."),
			 "TreeGroup":_("General")
      }

