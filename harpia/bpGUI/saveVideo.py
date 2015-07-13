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
        
        filename = self.m_sDataDir+'glade/saveVideo.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'SAVEFilename',
            'SAVEType',
            'SAVEBackgroundColor',
            'SAVEFrameRate',
            'SAVEBorderColor',
            'codecSelection',
            'SAVEHelpView',
            'save_confirm'
            ]

        handlers = [
            'on_SAVEButtonSearch_clicked',
            'on_SAVEBackColorButton_clicked',
            'on_SAVEBorderColorButton_clicked',
            'on_save_cancel_clicked',
            'on_save_confirm_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        self.widgets['Properties'].set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")

        #load properties values
        for Property in self.m_oPropertiesXML.properties.block.property:

            if Property.name == "filename":
            	self.widgets['SAVEFilename'].set_text( os.path.expanduser(Property.value) );
            if Property.name == "framerate":
            	self.widgets['SAVEFrameRate'].set_value( float(Property.value) );
            if Property.name == "codecSelection":
            	if Property.value == "MPEG1":
            		self.widgets['codecSelection'].set_active(0)
            	elif Property.value == "mjpeg":
            		self.widgets['codecSelection'].set_active(1)
            	elif Property.value == "MPEG4.2":
            		self.widgets['codecSelection'].set_active(2)
            	elif Property.value == "MPEG4.3":
            		self.widgets['codecSelection'].set_active(3)
            	elif Property.value == "MPEG4":
            		self.widgets['codecSelection'].set_active(4)
            	elif Property.value == "H263":
            		self.widgets['codecSelection'].set_active(5)
            	elif Property.value == "H263I":
            		self.widgets['codecSelection'].set_active(6)
            	elif Property.value == "FLV1":
            		self.widgets['codecSelection'].set_active(7)

 #           if Property.name == "filetype":
 #               if Property.value == "png":
 #                   self.widgets['SAVEType'].set_active( int(0) )                    
 #               if Property.value == "jpeg":
 #                   self.widgets['SAVEType'].set_active( int(1) )


        #load border color
        self.m_oBorderColor = self.m_oS2iBlockProperties.GetBorderColor()

        t_nBorderRed   = self.m_oBorderColor[0] * 257
        t_nBorderGreen = self.m_oBorderColor[1] * 257
        t_nBorderBlue  = self.m_oBorderColor[2] * 257

        t_oBorderColor = gtk.gdk.Color(red=t_nBorderRed,green=t_nBorderGreen,blue=t_nBorderBlue)

        self.widgets['SAVEBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oBorderColor)        

        #load block color
        self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()

        t_nBackRed   = self.m_oBackColor[0] * 257
        t_nBackGreen = self.m_oBackColor[1] * 257
        t_nBackBlue  = self.m_oBackColor[2] * 257

        t_oBackColor = gtk.gdk.Color(red=t_nBackRed,green=t_nBackGreen,blue=t_nBackBlue)

        self.widgets['SAVEBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)
                             
        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/saveVideo"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['SAVEHelpView'].set_buffer( t_oTextBuffer )
        
    #----------------------------------------------------------------------

    def __del__(self):
        
	pass

    #---------------------------------------------------------------------- 

    def on_save_cancel_clicked( self, *args ):

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------
   
    def on_save_confirm_clicked( self, *args ):

        self.widgets['save_confirm'].grab_focus()

        for Property in self.m_oPropertiesXML.properties.block.property:
            
            if Property.name == "filename":
                Property.value = unicode( os.path.expanduser(self.widgets['SAVEFilename'].get_text()) )
            if Property.name == "framerate":
                Property.value = unicode( self.widgets['SAVEFrameRate'].get_value() )
            
            if Property.name == "codecSelection":
            	tCodec = int(self.widgets['codecSelection'].get_active())
            	if tCodec == 0:
            		Property.value = unicode("MPEG1")
            	elif tCodec == 1:
            		Property.value = unicode("mjpeg")
            	elif tCodec == 2:
            		Property.value = unicode("MPEG4.2")
            	elif tCodec == 3:
            		Property.value = unicode("MPEG4.3")
            	elif tCodec == 4:
            		Property.value = unicode("MPEG4")
            	elif tCodec == 5:
            		Property.value = unicode("H263")
            	elif tCodec == 6:
            		Property.value = unicode("H263I")
            	elif tCodec == 7:
            		Property.value = unicode("FLV1")

#            if Property.name == "filetype":
#
#               t_nActive = self.widgets['SAVEType'].get_active( )
#
#                if int(t_nActive) == 0:
#                    Property.value = unicode("png")
#                if int(t_nActive) == 1:
#                    Property.value = unicode("jpeg")

        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )
            
        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

    def on_SAVEBackColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['SAVEBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBackColor[0] = t_oColor.red / 257

            self.m_oBackColor[1] = t_oColor.green / 257

            self.m_oBackColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

    def on_SAVEBorderColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['SAVEBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBorderColor[0] = t_oColor.red / 257
            
            self.m_oBorderColor[1] = t_oColor.green / 257

            self.m_oBorderColor[2] = t_oColor.blue / 257
            
    #----------------------------------------------------------------------

    def on_SAVEButtonSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Salvar Video...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

        if os.name == 'posix':
          dialog.set_current_folder(os.path.expanduser("~"))

        filter = gtk.FileFilter()
        filter.set_name("Todos os arquivos")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("videos")
        filter.add_mime_type("*.mpeg")
        filter.add_mime_type("*.avi")
        filter.add_mime_type("*.mpg")
        filter.add_mime_type("*.wmv")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['SAVEFilename'].set_text(response);
        
    #----------------------------------------------------------------------
  
#SaveProperties = Properties()
#SaveProperties.show( center=0 )


