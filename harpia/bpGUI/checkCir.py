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
        
        filename = self.m_sDataDir+'glade/checkCir.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'dpSel',
						'distSel',
						'threshSel',
						'qualySel',
						'minX',
						'maxX',
						'minY',
						'maxY',
						'minRad',
						'maxRad',
						'numOfCircs',
						'PosCirc',
						'NumCirc',
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
					if Property.name == "dpSel":
						self.widgets['dpSel'].set_value( float(Property.value) );
					if Property.name == "distSel":
						self.widgets['distSel'].set_value( float(Property.value) );
					if Property.name == "threshSel":
						self.widgets['threshSel'].set_value( float(Property.value) );
					if Property.name == "qualySel":
						self.widgets['qualySel'].set_value( float(Property.value) );
					if Property.name == "minX":
						self.widgets['minX'].set_value( float(Property.value) );
					if Property.name == "maxX":
						self.widgets['maxX'].set_value( float(Property.value) );
					if Property.name == "minY":
						self.widgets['minY'].set_value( float(Property.value) );
					if Property.name == "maxY":
						self.widgets['maxY'].set_value( float(Property.value) );
					if Property.name == "minRad":
						self.widgets['minRad'].set_value( float(Property.value) );
					if Property.name == "maxRad":
						self.widgets['maxRad'].set_value( float(Property.value) );
					if Property.name == "numOfCircs":
						self.widgets['numOfCircs'].set_value( float(Property.value) );
					if Property.name == "criteria":
						if Property.value == "pos":
							self.widgets['PosCirc'].set_active( True );
						elif Property.value == "num":
							self.widgets['NumCirc'].set_active( True );

        self.configure()

        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/checkCir"+ _("_en.help"))
        
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
				if Property.name == "dpSel":
					Property.value = unicode(self.widgets['dpSel'].get_value())
				if Property.name == "distSel":
					Property.value = unicode(self.widgets['distSel'].get_value())
				if Property.name == "threshSel":
					Property.value = unicode(self.widgets['threshSel'].get_value())
				if Property.name == "qualySel":
					Property.value = unicode(self.widgets['qualySel'].get_value())
				if Property.name == "minX":
					Property.value = unicode(self.widgets['minX'].get_value())
				if Property.name == "maxX":
					Property.value = unicode(self.widgets['maxX'].get_value())
				if Property.name == "minY":
					Property.value = unicode(self.widgets['minY'].get_value())
				if Property.name == "maxY":
					Property.value = unicode(self.widgets['maxY'].get_value())
				if Property.name == "minRad":
					Property.value = unicode(self.widgets['minRad'].get_value())
				if Property.name == "maxRad":
					Property.value = unicode(self.widgets['maxRad'].get_value())
				if Property.name == "numOfCircs":
					Property.value = unicode(self.widgets['numOfCircs'].get_value())
				if Property.name == "criteria":
					if self.widgets['NumCirc'].get_active():
						Property.value = u"num"
					elif self.widgets['PosCirc'].get_active():
						Property.value = u"pos"
				
			self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )
			

			self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )
			self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )
			self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

    
##propProperties = Properties()()
#propProperties.show( center=0 )


