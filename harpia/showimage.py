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


# Libraries 
import os
import gtk
from GladeWindow import GladeWindow

#i18n
import gettext
APP='harpia'
DIR='/usr/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#----------------------------------------------------------------------
## Shows an image
class ShowImage(GladeWindow):
    """
    Shows an image by creating a new window and requesting for the processed image.
    Its called when occurs a double click left in a BlockShow.
    """

    #----------------------------------------------------------------------

    def __init__( self, a_ImagePath, a_ErrorLog ):
        """
        Creates a window and shows the processed image.
        """

        self.m_oImagePath = a_ImagePath
        self.m_sErrorLog = a_ErrorLog

        self.m_sDefaultExt = ".png"
        self.m_fSizeIncrement = 0.2
        self.m_iMinSize=5
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/showwindow.ui'

        widget_list = [ 'processed_image',  'ShowWindow'    ]

        handlers = [ 'on_btnShowSave_clicked',    'on_btnShowClose_clicked',
                     'on_btnShowZoomIn_clicked',  'on_btnShowZoomOut_clicked',
                     'on_btnShowZoomDefault_clicked'    ]

        top_window = 'ShowWindow'
        
        # Initializes the Gladewindow
        if (self.m_oImagePath == None) or (not os.path.exists(self.m_oImagePath)):
            print "No Image"
            self.Window = gtk.Window()
            self.Window.set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")
            self.Window.set_position(gtk.WIN_POS_CENTER)        
            self.Window.resize(320,240)
            self.Window.set_title(_("Processed Image"))
            self.Label = gtk.Label()
            ## Error Loading
            if self.m_sErrorLog == '' or self.m_sErrorLog == None:
                self.m_sErrorLog = _("Chain not yet processed, Live Session or unknown error. \n Please try to process active chain again.")
            t_sErrorText = _("No image found. \n\tLog Error: \n\n") + self.m_sErrorLog
            
            self.Label.set_text(t_sErrorText)
            self.Label.show()
            self.Window.add(self.Label)
            self.Window.show()


        else:
            GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
            #self.glade = gtk.glade.XML("../etc/GladeFiles/showwindow.glade")
            self.Window = self.widgets['ShowWindow']
            #self.Image = self.glade.get_widget("processed_image")
            self.Image = self.widgets['processed_image']
            self.Window.set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")
            self.Window.set_position(gtk.WIN_POS_CENTER)        
            self.Window.resize(640,480)
            self.Label = gtk.Label()
            self.m_oImage = gtk.gdk.pixbuf_new_from_file(self.m_oImagePath)
            self.m_oOriginalImage = gtk.gdk.pixbuf_new_from_file(self.m_oImagePath)
            self.Image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self.m_oImagePath))
            FileReader = file(self.m_oImagePath, "r")
            self.m_sFileRead = FileReader.read()
            FileReader.close()

            self.CurrentHeight = self.m_oOriginalImage.get_height()
            self.CurrentWidth = self.m_oOriginalImage.get_width()
        
        
    #----------------------------------------------------------------------

    def __del__(self):
        pass

    #----------------------------------------------------------------------

    def show(self):
        pass
        #self.Window.show_all()

    def on_btnShowSave_clicked(self, *args):
        #self.SaveAs = False
    
        t_oDialog = gtk.FileChooserDialog("Save...",
                                    None,
                                    gtk.FILE_CHOOSER_ACTION_SAVE,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    
        t_oDialog.set_default_response(gtk.RESPONSE_OK)
        
        t_oFilter = gtk.FileFilter()
        t_oFilter.set_name("All Archives")
        t_oFilter.add_pattern("*")
        t_oDialog.add_filter(t_oFilter)

        t_oFilter = gtk.FileFilter()
        t_oFilter.set_name("images")
        t_oFilter.add_mime_type("*.jpg")
        t_oFilter.add_mime_type("*.bmp")
        t_oFilter.add_mime_type("*.png")
        t_oFilter.add_mime_type("*.gif")
        t_oDialog.add_filter(t_oFilter)
    
        t_oResponse = t_oDialog.run()
    
        if t_oResponse == gtk.RESPONSE_OK:
            
            a_sFilename = t_oDialog.get_filename()

            if a_sFilename[-4] != '.':
                FileHandle = file( str(a_sFilename) + str(self.m_sDefaultExt), "w" )
                FileHandle.write( self.m_sFileRead )
                FileHandle.close()
            else:
                FileHandle = file( str(a_sFilename) , "w" )
                #FileReader = file(self.FilePath, "r")
                FileHandle.write( self.m_sFileRead  )
                FileHandle.close()
                
                
        if t_oResponse == gtk.RESPONSE_CANCEL:
            t_oDialog.destroy()
            
        t_oDialog.destroy()


    
    def on_btnShowClose_clicked(self, *args):
        self.Window.hide()    
        
    def on_btnShowZoomIn_clicked(self, *args):

        t_iMaxHeight = 4*self.m_oOriginalImage.get_height()
        t_iMaxWidth  = 4*self.m_oOriginalImage.get_height()
        self.CurrentHeight = min(self.CurrentHeight * (1+self.m_fSizeIncrement),t_iMaxHeight)
        self.CurrentWidth = min(self.CurrentWidth * (1+self.m_fSizeIncrement),t_iMaxWidth)
        
        self.m_oImage = self.m_oOriginalImage.scale_simple(self.CurrentWidth,self.CurrentHeight,gtk.gdk.INTERP_BILINEAR)
        self.Image.set_from_pixbuf(self.m_oImage)
        
        
    def on_btnShowZoomOut_clicked(self, *args):
        
        self.CurrentHeight = max(self.CurrentHeight * (1-self.m_fSizeIncrement),self.m_iMinSize)
        self.CurrentWidth = max(self.CurrentWidth * (1-self.m_fSizeIncrement),self.m_iMinSize)
        
        self.m_oImage = self.m_oOriginalImage.scale_simple(self.CurrentWidth,self.CurrentHeight,gtk.gdk.INTERP_BILINEAR)
        self.Image.set_from_pixbuf(self.m_oImage)
        
        
    def on_btnShowZoomDefault_clicked(self, *args):

        self.CurrentHeight = self.m_oOriginalImage.get_height()
        self.CurrentWidth = self.m_oOriginalImage.get_width()
        self.Image.set_from_pixbuf(self.m_oOriginalImage)

