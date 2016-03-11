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

import gtk

from harpia.GladeWindow import GladeWindow
from harpia.s2icommonproperties import S2iCommonProperties, APP, DIR

#i18n
import os
import gettext
from harpia.utils.XMLUtils import XMLParser

_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#----------------------------------------------------------------------
   
class Properties( GladeWindow, S2iCommonProperties ):

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/comment.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'COMMENTView'
            ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_comment_confirm_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        #load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        for Property in self.block_properties:

            #self.widgets['FILLBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "comment":
                self.m_sComment = str(value)

        self.configure()

        
        # #load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir+"help/comment"+ _("_en.help"))
        
        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.getTag("help").getTag("content").getTagContent()) ) )
    
        # self.widgets['HelpView'].set_buffer( t_oTextBuffer )
    def getHelp(self):
        return "Insere comentario"
		
        # Comment View
        
        t_sComment = gtk.TextBuffer()
        t_sComment.set_text(self.m_sComment)
        
        self.widgets['COMMENTView'].set_buffer(t_sComment)
        self.widgets['COMMENTView'].set_property('editable', True)
        
        self.widgets['COMMENTView'].set_cursor_visible(True)

    #----------------------------------------------------------------------

    def __del__(self):
        
	pass

    #----------------------------------------------------------------------
   
    def on_comment_confirm_clicked( self, *args ):

        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "comment":
               t_oText = self.widgets['COMMENTView'].get_buffer()
               t_oStart = t_oText.get_start_iter()
               t_oEnd = t_oText.get_end_iter()
               t_sComment = t_oText.get_text(t_oStart, t_oEnd)
               Property.setAttr("value", unicode(t_sComment ))


        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )
        
        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

    def on_COMMENTFillColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:

            self.widgets['COMMENTBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            # Sets the back color the same as the color selected for filling
            self.m_oBackColor[0] = t_oColor.red / 257
            self.m_oBackColor[1] = t_oColor.green / 257
            self.m_oBackColor[2] = t_oColor.blue / 257
  
#CommentProperties = Properties()
#CommentProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
   for propIter in blockTemplate.properties:
       if propIter[0] == 'comment':
           comment = propIter[1]
   blockTemplate.functionCall = '/*'+comment+'*/ \n'

# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
	return {"Label":_("Comment"),
         "Path":{"Python":"comment",
                 "Glade":"glade/comment.ui",
                 "Xml":"xml/comment.xml"},
         "Icon":"images/comment.png",
         "Color":"50:100:200:150",
				 "InTypes":"",
				 "OutTypes":"",
				 "Description":_("Insert a comment."),
				 "TreeGroup":_("General")
         }
