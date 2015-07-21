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
from harpia.s2icommonproperties import S2iCommonProperties
#i18n
import os
import gettext
APP='harpia'
DIR=os.environ['HARPIA_DATA_DIR']+'po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#----------------------------------------------------------------------
   
class Properties( GladeWindow, S2iCommonProperties ):

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/rotate.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
						'isAtCenter',
						'isAtPoint',
						'isScalling',
						'isFilling',
						'xC',
						'yC',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
						'prop_confirm'
            ]

        handlers = [
            'on_cancel_clicked',
            'on_prop_confirm_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        #load properties values
        for Property in self.m_oPropertiesXML.properties.block.property:
					if Property.name == "xC":
						self.widgets['xC'].set_value( float(Property.value) );
					if Property.name == "yC":
						self.widgets['yC'].set_value( float(Property.value) );

					if Property.name == "isFilling":
						if Property.value == "true":
							self.widgets['isFilling'].set_active( True );
						else:
							self.widgets['isFilling'].set_active( False );

					if Property.name == "isScalling":
						if Property.value == "true":
							self.widgets['isScalling'].set_active( True );
						else:
							self.widgets['isScalling'].set_active( False );

					if Property.name == "isCenter":
						if Property.value == "true":
							self.widgets['isAtCenter'].set_active( True );
						else:
							self.widgets['isAtPoint'].set_active( True );

        self.configure()
        
        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/rotate"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['HelpView'].set_buffer( t_oTextBuffer )
        
    #----------------------------------------------------------------------

    def __del__(self):
				pass

    #----------------------------------------------------------------------
   
    def on_prop_confirm_clicked( self, *args ):

			self.widgets['prop_confirm'].grab_focus()

			for Property in self.m_oPropertiesXML.properties.block.property:
				if Property.name == "xC":
					Property.value = unicode(self.widgets['xC'].get_value())
				if Property.name == "yC":
					Property.value = unicode(self.widgets['yC'].get_value())
				
				if Property.name == "isCenter":
					if self.widgets['isAtCenter'].get_active():
						Property.value = u"true"
					else:
						Property.value = u"false"

				if Property.name == "isFilling":
					if self.widgets['isFilling'].get_active():
						Property.value = u"true"
					else:
						Property.value = u"false"

				if Property.name == "isScalling":
					if self.widgets['isScalling'].get_active():
						Property.value = u"true"
					else:
						Property.value = u"false"

				
			self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )
			

			self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )
			self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )
			self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

#propProperties = Properties()()
#propProperties.show( center=0 )


