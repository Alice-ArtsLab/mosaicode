# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
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


from tips import TIPS
from tips import TIPS_VER

import os.path
import gtk
import random

from amara import binderytools as bt

#i18n
import gettext
APP='harpia'
DIR='/usr/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#
# Class for tip-of-the-day dialogs.
#
class TipOfTheDay(gtk.MessageDialog): #, Observable):
		OBS_TIP = 0
		OBS_TOGGLED = 1

		def __init__(self):

				self.confFile = None
				self.confFilePath = "~/.harpiaConf.xml"
				self.btXML = None
				
				self.showTips = True
				
				self.avTips = {}
				self.nOfOkTips = -1
				
				self.__index = 0
				
				self.__loadConfFile()
				self.__index = self.__getTipFromConf()
				
				if self.__index == -1:
					self.showTips = False
					return

				gtk.MessageDialog.__init__(self, None, gtk.DIALOG_MODAL,
																		gtk.MESSAGE_INFO, gtk.BUTTONS_NONE,
																		"Harpia")
				self.set_title(_("Tip of the Day"))

				self.connect("response", self.__on_closeBtn)

				self.__label = self.vbox.get_children()[0].get_children()[1]
				# HACK HACK HACK -- make it work with gtk+-2.6.x
				if (not isinstance(self.__label, gtk.Label)):
						self.__label.remove(self.__label.get_children()[1])
						self.__label = self.__label.get_children()[0]

				self.__checkbox = gtk.CheckButton(_("Show tips at startup"))
				self.__checkbox.set_active(True)
				self.__checkbox.connect("toggled", self.__on_toggleAll)
				self.__checkbox.show()
				self.vbox.pack_end(self.__checkbox, 0, 0, 0)

				self.__thcheckbox = gtk.CheckButton(_("Never Show This Tip Again"))
				self.__thcheckbox.set_active(False)
				self.__thcheckbox.connect("toggled", self.__on_toggleThis)
				self.__thcheckbox.show()
				self.vbox.pack_end(self.__thcheckbox, 0, 0, 0)

				self.btn_prev = gtk.Button(stock = gtk.STOCK_GO_BACK)
				self.btn_prev.connect("clicked", self.prev_tip)
				self.btn_prev.show()

				self.btn_next = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
				self.btn_next.connect("clicked", self.next_tip)
				self.btn_next.show()

				btn_close = gtk.Button(stock = gtk.STOCK_CLOSE)
				btn_close.connect("clicked", self.__on_close)
				btn_close.show()

				self.action_area.add(self.btn_prev)
				self.action_area.add(self.btn_next)
				self.action_area.add(btn_close)

				# make the close button the default button
				btn_close.set_flags(gtk.CAN_DEFAULT)
				self.set_default(btn_close)
				self.set_focus(btn_close)
				
				self.__show_currTip()

		def run(self):
			if self.showTips:
				gtk.MessageDialog.run(self)

		def __show_currTip(self):
			self.__boundIndex2Dict()
			self.__getNofTips()
			self.__label.set_markup(_(TIPS[self.__index]).strip())
			
			self.__thcheckbox.set_active(not self.avTips[self.__index])
			self.__checkbox.set_active(self.showTips)
			if self.nOfOkTips <= 1:
				self.btn_next.set_sensitive(False)
				self.btn_prev.set_sensitive(False)

		def __on_close(self, src):
				self.__saveConfFile()
				self.hide()

		def __on_closeBtn(self, dialog, response):
			self.__saveConfFile()
			self.hide()

		def __boundIndex2Dict(self):
			if (self.__index >= len(TIPS)):
				self.__index = 0
			if (self.__index < 0):
				self.__index = len(TIPS)-1

		def __getNofTips(self):
			self.nOfOkTips = 0
			for tipInstance in self.avTips.keys():
				if self.avTips[tipInstance]:
					self.nOfOkTips += 1


		def __on_toggleThis(self, src):
				value = src.get_active()
				self.avTips[self.__index] = not value
				#self.__getNofTips()
				#self.update_observer(self.OBS_TOGGLED, value)

		def __on_toggleAll(self, src):

				value = src.get_active()
				self.showTips = value
				#self.update_observer(self.OBS_TOGGLED, value)

		def next_tip(self, *args):
			self.__index += 1
			self.__boundIndex2Dict()
			while(not self.avTips[self.__index]):
				self.__index += 1
				self.__boundIndex2Dict()
			self.__show_currTip()


		def prev_tip(self, *args):
			self.__index -= 1
			self.__boundIndex2Dict()
			while(not self.avTips[self.__index]):
				self.__index -= 1
				self.__boundIndex2Dict()
			self.__show_currTip()

		def __getTipFromConf(self):
			okTipList = []
			for tipInstance in self.avTips.keys():
				if self.avTips[tipInstance] == True:
					okTipList.append(tipInstance)
			if(len(okTipList) == 0):
				randTipId = -1
			else:
				#randTipId = random.randint(0,len(okTipList)-1)#random tip
				randTipId = okTipList[0]#next tip in the list
			return randTipId
		
		
		
		def __loadConfFile(self):
			if(not os.path.exists(os.path.expanduser(self.confFilePath))):
				self.GenerateBlankConf()
			self.btXML = bt.bind_file(os.path.expanduser(self.confFilePath))
			if self.btXML.tipsOfTheDay.version != TIPS_VER:
				self.btXML = None
				self.GenerateBlankConf()
				self.btXML = bt.bind_file(os.path.expanduser(self.confFilePath))

			self.showTips = (self.btXML.tipsOfTheDay.show == "True")
			if self.showTips:
				for tip in self.btXML.tipsOfTheDay.tip:
					self.avTips[int(tip.id)] = (tip.enabled == "True")

		def __saveConfFile(self):
			newConf = bt.create_document()
			tipsList = []
			
			for tipInstance in self.avTips.keys():
				tipsList.append(newConf.xml_element(u"tip",attributes={u"enabled":unicode(self.avTips[tipInstance]), u"id":unicode(tipInstance)}))

			tipsEl = newConf.xml_element(u"tipsOfTheDay",content=tipsList,attributes={u"show":unicode(self.showTips), u"version":unicode(TIPS_VER)})
			newConf.xml_append(tipsEl)
			
			self.confFile = file(os.path.expanduser(self.confFilePath),'w')
			self.confFile.write(newConf.xml(indent=u'yes'))
			self.confFile.close()
			
		def GenerateBlankConf(self):
			newConf = bt.create_document()
			tipsList = []
			
			for tipInstance in range(len(TIPS)):
				tipsList.append(newConf.xml_element(u"tip",attributes={u"enabled":u"True", u"id":unicode(tipInstance)}))
			tipsEl = newConf.xml_element(u"tipsOfTheDay",content=tipsList,attributes={u"show":u"True", u"version":unicode(TIPS_VER)})
			newConf.xml_append(tipsEl)
			self.confFile = file(os.path.expanduser(self.confFilePath),'w')
			self.confFile.write(newConf.xml(indent=u'yes'))
			#print newConf.xml(indent=u'yes')
			self.confFile.close()
