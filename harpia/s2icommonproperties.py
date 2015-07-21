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

# Imported Libraries
import gtk
import gobject


#i18n
import gettext
APP='harpia'
DIR='/usr/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


#----------------------------------------------------------------------
## Block Properties base class
class S2iCommonProperties:
	"""
	This class implements the base properties for the blocks.
	In the Harpia current version, it only implements the color selection that is used to change the block back color and border color.
	"""

	#----------------------------------------------------------------------

	m_oColorSelectionDlg = None
	
	#----------------------------------------------------------------------
	
	def __init__( self, *args ):

		pass

	#----------------------------------------------------------------------

	def __del__(self):
		pass

	#----------------------------------------------------------------------

	def RunColorSelection(self,*args):
		"""
		This function creates a window for Color selection. This function is used to change the block back color and the border color.
		"""

		if self.m_oColorSelectionDlg == None:
			
			self.m_oColorSelectionDlg = gtk.ColorSelectionDialog(_("Color selection"))

		t_oColorSelection = self.m_oColorSelectionDlg.colorsel
		
		t_oResponse = self.m_oColorSelectionDlg.run()

		if t_oResponse == gtk.RESPONSE_OK:

			t_oColor = t_oColorSelection.get_current_color()

			self.m_oColorSelectionDlg.hide()

			return t_oColor

		else:
			self.m_oColorSelectionDlg.hide()

			return None
			
	#----------------------------------------------------------------------
	
	def on_cancel_clicked( self, *args ):
		self.widgets['Properties'].destroy()
		

    #----------------------------------------------------------------------

	def on_BackColorButton_clicked(self,*args):
		t_oColor = self.RunColorSelection()
		if t_oColor <> None:
			self.widgets['BackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
			self.m_oBackColor[0] = t_oColor.red / 257
			self.m_oBackColor[1] = t_oColor.green / 257
			self.m_oBackColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

	def on_BorderColorButton_clicked(self,*args):
		t_oColor = self.RunColorSelection()
		if t_oColor <> None:
			self.widgets['BorderColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
			self.m_oBorderColor[0] = t_oColor.red / 257
			self.m_oBorderColor[1] = t_oColor.green / 257
			self.m_oBorderColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

	def configure(self):
		self.widgets['Properties'].set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")

		#load properties values
		#there is no properties

		#load border color
		self.m_oBorderColor = self.m_oS2iBlockProperties.GetBorderColor()

		t_nBorderRed   = self.m_oBorderColor[0] * 257
		t_nBorderGreen = self.m_oBorderColor[1] * 257
		t_nBorderBlue  = self.m_oBorderColor[2] * 257

		t_oBorderColor = gtk.gdk.Color(red=t_nBorderRed,green=t_nBorderGreen,blue=t_nBorderBlue)

		self.widgets['BorderColor'].modify_bg(gtk.STATE_NORMAL,t_oBorderColor)        

		#load block color
		self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()

		t_nBackRed   = self.m_oBackColor[0] * 257
		t_nBackGreen = self.m_oBackColor[1] * 257
		t_nBackBlue  = self.m_oBackColor[2] * 257

		t_oBackColor = gtk.gdk.Color(red=t_nBackRed,green=t_nBackGreen,blue=t_nBackBlue)

		self.widgets['BackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)

    #----------------------------------------------------------------------

