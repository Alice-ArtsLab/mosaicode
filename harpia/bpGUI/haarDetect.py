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
        
        filename = self.m_sDataDir+'glade/haarDetect.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties
        
        widget_list = [
            'Properties',
            'ACQULabelFilename',
            'ACQUFilename',
            'min_neighbors',
            'ACQUButtonSearch',
            'ACQUBackgroundColor',
            'ACQUBorderColor',
            'ACQUHelpView',
						'acquisition_confirm'
            ]

        handlers = [
            'on_ACQUButtonSearch_clicked',
            'on_ACQUBackColorButton_clicked',
            'on_ACQUBorderColorButton_clicked',            
            'on_acquisition_confirm_clicked',
            'on_acquisition_cancel_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.widgets['Properties'].set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")

        self.m_sCurrentActive = 'file'
        #load properties values        
        for Property in self.m_oPropertiesXML.properties.block.property:
            if Property.name == "cascade_name":
                self.widgets['ACQUFilename'].set_text( Property.value );
            if Property.name == "min_neighbors":
                self.widgets['min_neighbors'].set_value( int(float(Property.value)) );

        #load block state 
        t_bState = self.m_oS2iBlockProperties.GetState()

        #load border color
        self.m_oBorderColor = self.m_oS2iBlockProperties.GetBorderColor()

        t_nBorderRed   = self.m_oBorderColor[0] * 257
        t_nBorderGreen = self.m_oBorderColor[1] * 257
        t_nBorderBlue  = self.m_oBorderColor[2] * 257

        t_oBorderColor = gtk.gdk.Color(red=t_nBorderRed,green=t_nBorderGreen,blue=t_nBorderBlue)

        self.widgets['ACQUBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oBorderColor)        

        #load block color
        self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()

        t_nBackRed   = self.m_oBackColor[0] * 257
        t_nBackGreen = self.m_oBackColor[1] * 257
        t_nBackBlue  = self.m_oBackColor[2] * 257

        t_oBackColor = gtk.gdk.Color(red=t_nBackRed,green=t_nBackGreen,blue=t_nBackBlue)

        self.widgets['ACQUBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)

        #load help text
        #t_oS2iHelp = bt.bind_file("../etc/acquisition/acquisition.help")
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/haarDetect"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['ACQUHelpView'].set_buffer( t_oTextBuffer )

    #----------------------------------------------------------------------

    def __del__(self):
        pass

    #---------------------------------------------------------------------- 

    def on_acquisition_cancel_clicked( self, *args ):

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------
   
    def on_acquisition_confirm_clicked( self, *args ):
        self.widgets['acquisition_confirm'].grab_focus()
        t_sFilename = unicode(self.widgets['ACQUFilename'].get_text())

        for Property in self.m_oPropertiesXML.properties.block.property:
            #file selected
            if Property.name == "cascade_name":
                Property.value = unicode(t_sFilename)
            if Property.name == 'min_neighbors':
                Property.value = unicode(self.widgets['min_neighbors'].get_value())
            
        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()
        
    #----------------------------------------------------------------------
    
    def on_ACQUBackColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['ACQUBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBackColor[0] = t_oColor.red / 257

            self.m_oBackColor[1] = t_oColor.green / 257

            self.m_oBackColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

    def on_ACQUBorderColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['ACQUBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBorderColor[0] = t_oColor.red / 257
            
            self.m_oBorderColor[1] = t_oColor.green / 257

            self.m_oBorderColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------
 
    def on_ACQUButtonSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Abrir...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

#-------------
#Scotti
        if os.name == 'posix':
          dialog.set_current_folder("/home/" + str(os.getenv('USER')) + "/Desktop")
#Scotti

        filter = gtk.FileFilter()
        filter.set_name("Haar Cascade")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("images")
        filter.add_mime_type("*.xml")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['ACQUFilename'].set_text(response);

    #----------------------------------------------------------------------

    def on_ACQURadioFile_pressed( self, *args ):
        self.widgets['ACQULabelFilename'].set_sensitive( True )
        self.widgets['ACQUFilename'].set_sensitive( True )
        self.widgets['ACQUButtonSearch'].set_sensitive( True )

    #----------------------------------------------------------------------
  
#AcquisitionProperties = Properties( )
#AcquisitionProperties.show( center=0 )



