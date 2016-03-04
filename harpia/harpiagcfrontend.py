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
# ----------------------------------------------------------------------


# Libraries
import shutil
import os
from glob import glob

import gobject
import gtk

from GladeWindow import GladeWindow
from harpia.utils.XMLUtils import XMLParser


# Harpia

# import s2ipngexport
import s2idirectory

import GcDiagram

import s2iSessionManager
import TipOfTheDay

# i18n
import gettext

APP = 'harpia'
DIR = '/usr/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


# ----------------------------------------------------------------------

# consts

BLOCK_SIZE_X = 100
BLOCK_SIZE_Y = 50


## Main window
class S2iHarpiaFrontend(GladeWindow):
    """
    Implements the main window frontend functionalities. Its derived from GladeWindow.
    This class connects all the signals in the harpia frontend main window and implements their functions.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        """
        Constructor. Initializes the GladeWindow object for signal connecting, creates a dictionary for the Blocks and BlocksProperties and loads the configurations.
        """

        self.exampleMenuItens = []

        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        filename = self.m_sDataDir + 'glade/harpia_gui-1.0.ui'

        widget_list = [
            'HarpiaFrontend',
            'SearchEntry',
            'SearchButton',
            'BlockDescription',
            'WorkArea',
            'BlocksTreeView',
            'StatusLabel',
            'ProcessImage',
            'ProcessToolBar',
            'CodeToolBar',
            'UpdateToolBar',
            'ViewSource',
            'toolbar1',
            'examples_menu',
            'fake_separator'
        ]

        handlers = [
            'on_NewMenuBar_activate', 'on_OpenMenuBar_activate',
            'on_SaveMenuBar_activate', 'on_SaveASMenuBar_activate',
            'on_QuitMenuBar_activate', 'on_CutMenuBar_activate',
            'on_CopyMenuBar_activate', 'on_PasteMenuBar_activate',
            'on_DeleteMenuBar_activate', 'on_AboutMenuBar_activate',
            'on_NewToolBar_clicked',
            'on_OpenToolBar_clicked',
            'on_SaveToolBar_clicked',
            'on_ProcessToolBar_clicked',
            'on_CodeToolBar_clicked',
            'on_ZoomOutToolBar_clicked', 'on_ZoomInToolBar_clicked',
            'on_SearchButton_clicked', 'on_BlocksTreeView_row_activated',
            'on_BlocksTreeView_cursor_changed', 'on_HarpiaFrontend_destroy',
            'on_ZoomDefaultToolBar_clicked', 'on_Preferences_clicked',
            'on_Export_clicked', 'on_CloseMenuBar_activate',
            'on_UpdateToolBar_clicked', 'on_tip_activate',
            'on_ViewSource_clicked',
            'on_reset_tip_activate'
        ]

        top_window = 'HarpiaFrontend'

        # Initializes the Gladewindow
        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.top_window.maximize()  # asking politely to maximize out app =]

        # Blocks
        self.Blocks = s2idirectory.groups

        for x in s2idirectory.block:
            self.Blocks[s2idirectory.block[x]["TreeGroup"]].append(s2idirectory.block[x]["Label"])

        # Blocks Properties
        self.BlocksProperties = dict()

        for x in s2idirectory.block:
            self.BlocksProperties[s2idirectory.block[x]["Label"]] = {"Inputs": len(s2idirectory.block[x]["InTypes"]),
                                                                     "Outputs": len(s2idirectory.block[x]["OutTypes"])}


        # cpscotti .. taking out more dumb code..


        self.widgets['HarpiaFrontend'].set_icon_from_file(self.m_sDataDir + "images/harpia_ave.png")

        self.m_oIconUpdate = gtk.Image()

        self.m_oIconUpdate.set_from_file(self.m_sDataDir + "images/system-software-update.png")

        self.m_oIconUpdate.show_all()

        self.widgets['UpdateToolBar'].set_icon_widget(self.m_oIconUpdate)

        self.g_sTreeViewPath = "0,0"

        if os.name == "nt":
            if not os.path.exists('../updhrp.bat'):
                self.widgets['toolbar1'].remove(self.widgets['UpdateToolBar'])
        else:
            if not os.path.exists('../updhrp.sh'):
                self.widgets['toolbar1'].remove(self.widgets['UpdateToolBar'])

        self.m_nStatus = 0

        self.SaveAs = False

        # Member Diagram references
        self.m_oGcDiagrams = {}

        self.m_oSessionIDs = {}

        self.m_oCopyBuffer = (-1, -1)  # tuple (fromPage, [listOfBlocks]) ...listOfConns?

        self.m_nCurrentIDSession = None

        self.LoadExamplesMenu()

        self.__InsertBlocks()

        self.on_CloseMenuBar_activate()  # removing the dummie page
        self.on_NewToolBar_clicked()  # creating blank page

        # Tip of The Day code
        tipOfTheDayWind = TipOfTheDay.TipOfTheDay()
        tipOfTheDayWind.run()

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def __InsertBlocks(self):
        """
        Inserts the blocks in the BlocksTree.
        """

        t_oTreeStore = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)

        t_oImage = gtk.CellRendererPixbuf()

        for t_sItem in self.Blocks.keys():

            t_oParent = t_oTreeStore.append(None, [t_sItem, t_oImage])

            for t_nIndex in range(len(self.Blocks[t_sItem])):
                t_oTreeStore.append(t_oParent, [self.Blocks[t_sItem][t_nIndex], t_oImage])

        self.widgets['BlocksTreeView'].set_model(t_oTreeStore)

        t_oTextRender = gtk.CellRendererText()

        t_oTextRender.set_property('editable', False)

        t_oColumn = gtk.TreeViewColumn(_("Available Blocks"), t_oTextRender, text=0)

        self.widgets['BlocksTreeView'].append_column(t_oColumn)

        #		TARGETS = [
        #			('MY_TREE_MODEL_ROW', gtk.TARGET_SAME_WIDGET, 0),
        #			('text/plain', 0, 1),
        #			('TEXT', 0, 2),
        #			('STRING', 0, 3),
        #			]

        # drag......
        self.widgets['BlocksTreeView'].enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
                                                                [('text/plain', gtk.TARGET_SAME_APP, 1)],
                                                                gtk.gdk.ACTION_DEFAULT |
                                                                gtk.gdk.ACTION_COPY)
        self.widgets['BlocksTreeView'].connect("drag-data-get", self.drag_data_get_cb)

        # ........'n'drop
        self.widgets['WorkArea'].connect("drag_data_received", self.drag_data_received)
        self.widgets['WorkArea'].drag_dest_set(
            gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
            [('text/plain', gtk.TARGET_SAME_APP, 1)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_COPY)

    def drag_data_received(self, widget, context, x, y, selection, targetType, time):
        # print("Shit Connected, Drop occurred at: (" + str(x) + "," + str(y) + ")")
        # erdtmann: dunno why 0, but it works (I suppose it's 'cos there's only one column in the tree)
        # path is the way to find the desired block on the treeview
        # g_iColumn = 0

        self.on_BlocksTreeView_row_activated_pos(self.widgets['BlocksTreeView'], self.g_sTreeViewPath, 0, x, y)

        return

    # ----------------------------------------------------------------------
    def drag_data_get_cb(self, treeview, context, selection, target_id, etime):
        treeselection = treeview.get_selection()
        model, iterac = treeselection.get_selected()
        self.g_sTreeViewPath = model.get_path(iterac)
        selection.set('text/plain', 8, "test")
        # necessary in order to the notebook receive the drag:
        return

    def make_pb(self, tvcolumn, cell, model, iter):
        stock = model.get_value(iter, 1)
        pb = self.widgets["BlocksTreeView"].render_icon(stock, gtk.ICON_SIZE_MENU, None)
        cell.set_property('pixbuf', pb)
        return

    def on_NewMenuBar_activate(self, *args):

        self.on_NewToolBar_clicked()

    # ----------------------------------------------------------------------

    def on_OpenMenuBar_activate(self, *args):

        self.on_OpenToolBar_clicked()

    # ----------------------------------------------------------------------

    def on_SaveMenuBar_activate(self, *args):

        self.on_SaveToolBar_clicked()

    # ----------------------------------------------------------------------

    def on_SaveASMenuBar_activate(self, *args):

        self.SaveAs = True

        self.on_SaveToolBar_clicked()

    # ----------------------------------------------------------------------

    def on_QuitMenuBar_activate(self, *args):
        """
        Callback function that destroys the windows when quit menu bar clicked.
        """

        self.on_HarpiaFrontend_destroy()

    # ----------------------------------------------------------------------

    def on_tip_activate(self, *args):
        tipOfTheDayWind = TipOfTheDay.TipOfTheDay()
        tipOfTheDayWind.run()

    def on_reset_tip_activate(self, *args):
        tipOfTheDayWind = TipOfTheDay.TipOfTheDay()
        tipOfTheDayWind.GenerateBlankConf()

    def on_CutMenuBar_activate(self, *args):
        """
        Callback function called when CutMenuBar is activated. Copy the block an removes from the diagram.
        """
        print "Cut functionality not implemented yet"

    # ----------------------------------------------------------------------

    def on_CopyMenuBar_activate(self, *args):
        """
        Callback function called when CopyMenuBar is activated. Just copy the block.
        """
        if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]

        self.m_oCopyBuffer = (
        self.widgets['WorkArea'].get_current_page(), t_oGcDiagram.GetBlockOnFocus())  ##apends tuple (pageN, blockN)
        print self.m_oCopyBuffer

    # ----------------------------------------------------------------------

    def on_PasteMenuBar_activate(self, *args):
        """
        Callback function called when PasteMenuBar is activated.
        Paste the copied block(s) in the diagram.
        """
        if self.m_oCopyBuffer[0] == -1:  # nothing copied
            return

        # print "pasting"

        if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]
            # print "destination exists"

            if self.m_oGcDiagrams.has_key(self.m_oCopyBuffer[0]):
                t_oFromDiagram = self.m_oGcDiagrams[self.m_oCopyBuffer[0]]
                # print "source exists"

                if t_oFromDiagram.m_oBlocks.has_key(self.m_oCopyBuffer[1]):
                    newBlockId = t_oGcDiagram.InsertBlock(t_oFromDiagram.m_oBlocks[self.m_oCopyBuffer[1]].m_nBlockType)
                    t_oGcDiagram.m_oBlocks[newBlockId].SetPropertiesXML_nID(
                        t_oFromDiagram.m_oBlocks[self.m_oCopyBuffer[1]].GetPropertiesXML())
                # print "setting props"

    # ----------------------------------------------------------------------

    def on_DeleteMenuBar_activate(self, *args):
        """
        Callback function called when DeleteMenuBar is activated. Deletes the selected item.
        """
        if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]
            blockId = t_oGcDiagram.GetBlockOnFocus()
            if t_oGcDiagram.m_oBlocks.has_key(blockId):
                t_oGcDiagram.DeleteBlock(blockId)

    # ----------------------------------------------------------------------

    def on_AboutMenuBar_activate(self, *args):
        """
        Callback function called when AboutMenuBar is activated. Loads the about window.
        """
        from harpia import about
        About = about.About()
        About.show(center=0)

    # ----------------------------------------------------------------------

    def on_NewToolBar_clicked(self, *args):
        """
        Callback function called when NewToolBar is clicked. Creates a new tab with an empty diagram.
        """

        # maybe pass to a s2iView base class
        t_oNewDiagram = GcDiagram.GcDiagram()  # created new diagram

        t_oTable = gtk.Table(2, 2, False)

        t_oFrame = gtk.Frame()

        t_oFrame.set_shadow_type(gtk.SHADOW_IN)

        t_oTable.attach(t_oFrame, 0, 1, 0, 1,
                        gtk.EXPAND | gtk.FILL | gtk.SHRINK,
                        gtk.EXPAND | gtk.FILL | gtk.SHRINK)

        t_oFrame.add(t_oNewDiagram)
        # t_oNewDiagram.set_scroll_region(0, 0, 400, 400) #diagrams handle this

        t_oVAdjustment = gtk.VScrollbar(t_oNewDiagram.get_vadjustment())
        t_oHAdjustment = gtk.HScrollbar(t_oNewDiagram.get_hadjustment())
        t_oTable.attach(t_oVAdjustment, 1, 2, 0, 1, gtk.FILL, gtk.EXPAND | gtk.FILL | gtk.SHRINK)
        t_oTable.attach(t_oHAdjustment, 0, 1, 1, 2, gtk.EXPAND | gtk.FILL | gtk.SHRINK, gtk.FILL)
        t_oTable.show_all()

        # tab label
        t_nCurrentPage = self.widgets['WorkArea'].get_current_page()

        t_oLabel = gtk.Label(_("Unnamed ") + str(t_nCurrentPage + 1) + "[*]")

        self.widgets['WorkArea'].set_show_tabs(True)
        self.widgets['WorkArea'].append_page(t_oTable, t_oLabel)

        t_nSelectedPage = self.widgets['WorkArea'].get_n_pages() - 1
        self.widgets['WorkArea'].set_current_page(t_nSelectedPage)

        self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()] = t_oNewDiagram

    # self.ShowGrid( self.m_bShowGrid )

    # self.SetGridInterval( self.m_nGridInterval )

    # ----------------------------------------------------------------------

    def on_OpenToolBar_clicked(self, *args):
        # Opens a dialog for file selection and opens the file.

        t_oDialog = gtk.FileChooserDialog(_("Open..."),
                                          None,
                                          gtk.FILE_CHOOSER_ACTION_OPEN,
                                          (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        t_oDialog.set_default_response(gtk.RESPONSE_OK)

        if os.name == 'posix':
            t_oDialog.set_current_folder(os.path.expanduser("~"))

        t_oFilter = gtk.FileFilter()
        t_oFilter.set_name(_("All Archives"))
        t_oFilter.add_pattern("*")
        t_oDialog.add_filter(t_oFilter)

        t_oFilter = gtk.FileFilter()
        t_oFilter.set_name(_("Harpia Files"))
        t_oFilter.add_pattern("*.hrp")
        t_oDialog.add_filter(t_oFilter)

        t_oResponse = t_oDialog.run()

        if t_oResponse == gtk.RESPONSE_OK:
            ##create a new workspace
            self.on_NewToolBar_clicked()

            t_nCurrentPage = self.widgets['WorkArea'].get_current_page()
            t_oGcDiagram = self.m_oGcDiagrams[t_nCurrentPage]

            if len(t_oDialog.get_filename()) > 0:
                t_oGcDiagram.SetFilename(t_oDialog.get_filename())

        t_oDialog.destroy()

        if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]
            if t_oGcDiagram.GetFilename() is not None:
                if t_oGcDiagram.Load():
                    t_nCurrentPage = self.widgets['WorkArea'].get_current_page()
                    t_oChild = self.widgets['WorkArea'].get_nth_page(t_nCurrentPage)
                    t_sNewLabel = t_oGcDiagram.GetFilename().split("/").pop()
                    t_oLabel = gtk.Label(str(t_sNewLabel))
                    self.widgets['WorkArea'].set_tab_label(t_oChild, t_oLabel)

    # ----------------------------------------------------------------------

    def on_SaveToolBar_clicked(self, *args):
        # Opens a dialog for file and path selection. Saves the file and if necessary updates the tab name.

        if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):

            t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]

            if t_oGcDiagram.GetFilename() is None or self.SaveAs:
                self.SaveAs = False

                t_oDialog = gtk.FileChooserDialog(_("Save..."),
                                                  None,
                                                  gtk.FILE_CHOOSER_ACTION_SAVE,
                                                  (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_SAVE, gtk.RESPONSE_OK))

                t_oDialog.set_default_response(gtk.RESPONSE_OK)

                if os.name == 'posix':
                    t_oDialog.set_current_folder(os.path.expanduser("~"))

                t_oFilter = gtk.FileFilter()
                t_oFilter.set_name(_("All Archives"))
                t_oFilter.add_pattern("*")
                t_oDialog.add_filter(t_oFilter)

                t_oFilter = gtk.FileFilter()
                t_oFilter.set_name(_("Harpia Files"))
                t_oFilter.add_pattern("*.hrp")
                t_oDialog.add_filter(t_oFilter)

                t_oResponse = t_oDialog.run()
                if t_oResponse == gtk.RESPONSE_OK:
                    t_oGcDiagram.SetFilename(t_oDialog.get_filename())

                t_oDialog.destroy()

            if t_oGcDiagram.GetFilename() is not None:
                if len(t_oGcDiagram.GetFilename()) > 0:
                    t_oGcDiagram.Save()

                    ##update tab name
                    t_nCurrentPage = self.widgets['WorkArea'].get_current_page()
                    t_oChild = self.widgets['WorkArea'].get_nth_page(t_nCurrentPage)
                    t_sNewLabelLen = int(len(t_oGcDiagram.GetFilename().split("/")) - 1)
                    t_sNewLabel = t_oGcDiagram.GetFilename().split("/")[t_sNewLabelLen]
                    t_oLabel = gtk.Label(str(t_sNewLabel))
                    self.widgets['WorkArea'].set_tab_label(t_oChild, t_oLabel)

    # ----------------------------------------------------------------------

    def UpdateStatus(self, a_nStatus):
        """
        Receives a status and shows in the StatusBar.
        """

        # a_nStatus
        # 0 - Connecting...
        # 1 - could not connect to server
        # 2 - Processing...
        # 3 - could not create a new session ID
        # 4 - could not send images to server
        # 5 - could not send process file to server
        # 6 - Process error
        # 7 - Process complete
        # 8 - Nothing to process
        # 9 - Save error
        # 10 - Code retrieved

        self.m_nStatus = a_nStatus

        t_oStatusMessage = {0: _("Processing..."),
                            # cpscotti.. connecting nao tem nada a ver com a ideia... tah outdated
                            1: _("Could not connect to server"),
                            2: _("Processing(2)..."),
                            3: _("Could not create a new session ID"),
                            4: _("Could not send images to server"),
                            5: _("Could not send process file to server"),
                            6: _("Processing error"),
                            7: _("Processing complete"),
                            8: _("Nothing to process"),
                            9: _("Save error"),
                            10: _("Code Saved")}

        # if a_nStatus == 7 or a_nStatus == 10:
        # self.widgets['ProcessImage'].set_from_stock( gtk.STOCK_YES, gtk.ICON_SIZE_MENU)
        # else:
        # self.widgets['ProcessImage'].set_from_stock( gtk.STOCK_NO, gtk.ICON_SIZE_MENU  )

        self.widgets['StatusLabel'].set_text(t_oStatusMessage[a_nStatus])

        while gtk.events_pending():
            gtk.main_iteration(False)

    # ----------------------------------------------------------------------
    def SetStatusMessage(self, a_sStatus, a_bGood):
        """
        Receives a status message and shows it in the StatusBar.
        """
        # print a_bGood
        if a_bGood:
            self.widgets['ProcessImage'].set_from_stock(gtk.STOCK_YES, gtk.ICON_SIZE_MENU)
        else:
            self.widgets['ProcessImage'].set_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_MENU)
        self.widgets['StatusLabel'].set_text(a_sStatus)
        while gtk.events_pending():
            gtk.main_iteration(False)

    # ----------------------------------------------------------------------


    def on_ProcessToolBar_clickedIneer(self):
        t_nPage = self.widgets['WorkArea'].get_current_page()
        t_bIsLive = False
        if self.m_oGcDiagrams.has_key(t_nPage):
            self.UpdateStatus(0)

            t_oGcDiagram = self.m_oGcDiagrams[t_nPage]
            #print "PROCESS CHAIN",t_oS2iDiagram.GetProcessChain()
            #t_oProcessXML = bt.bind_string("<harpia>" + \
            #                               str(t_oGcDiagram.GetProcessChain()) + \
            #                               "</harpia>")
            #print len(list(t_oProcessXML.harpia.properties.childNodes))


            t_oProcessXML = XMLParser("<harpia>" + \
                                           str(t_oGcDiagram.GetProcessChain()) + \
                                           "</harpia>", fromString=True)
            #print t_oProcessXML

            graph_size = len(list(t_oProcessXML.getTag("harpia").getTag("properties").getTagChildren()))

            if graph_size > 1:
                blocks = t_oProcessXML.getTag("harpia").getTag("properties").getChildTags("block")
                for t_oBlockProperties in blocks:
                    block_properties = t_oBlockProperties.getChildTags("property")
                    if int(t_oBlockProperties.type) == 00:  # 00 = acquisition block
                        inputType = 'file'
                        for t_oProperty in block_properties:
                            if t_oProperty.name == 'type':
                                print t_oProperty.name
                                inputType = t_oProperty.value

                            ###Just in case we need to know if we are dealing with a live feed or not this early
                            # if inputType == 'video' or inputType == 'live':
                            #	#if not t_bIsLive:
                            #		#t_bIsLive = True

                            # adoção do paradigma monolítico.. nada de ficar mandando imagens por sockets!!
                            if t_oProperty.name == 'filename' and inputType == 'file':
                                t_oProperty.value = os.path.expanduser(t_oProperty.value)
                                t_oProperty.value = os.path.realpath(t_oProperty.value)
                                if (not os.path.exists(t_oProperty.value)):
                                    errMsg = _("Bad Filename: ") + t_oProperty.value
                                    print(errMsg)
                                    self.SetStatusMessage(errMsg, 0)
                                    return

                    if int(t_oBlockProperties.type) == 01:  # 01 => save image
                        for t_oProperty in block_properties:
                            if t_oProperty.name == 'filename':
                                t_oProperty.value = os.path.realpath(t_oProperty.value)


                    # seguindo o paradigma de não mandar mais nada.. vamos testar com o haar =]
                    # não vamos mandar mais nada mas vamos traduzir o path do haarCascade pra algo real
                    if int(t_oBlockProperties.type) == 610:  # 610 => haar detector... passando a cascade .xml
                        for t_oProperty in block_properties:
                            if t_oProperty.name == 'cascade_name':
                                t_oProperty.value = os.path.realpath(t_oProperty.value)
                                if (not os.path.exists(t_oProperty.value)):
                                    errMsg = _("Bad Filename: ") + t_oProperty.value
                                    print(errMsg)
                                    self.SetStatusMessage(errMsg, 0)
                                    return

                # cpscotti standalone!!!
                t_lsProcessChain = []  # lista pra n precisar ficar copiando prum lado e pro otro o xml inteiro
                t_lsProcessChain.append(t_oProcessXML.getXML())

                t_Sm = s2iSessionManager.s2iSessionManager()

                ## pegando o novo ID (criado pela s2iSessionManager) e passando para o s2idiagram
                self.m_oGcDiagrams[t_nPage].SetIDBackendSession(t_Sm.m_sSessionId)

                # step sempre sera uma lista.. primeiro elemento eh uma mensagem, segundo eh o erro.. caso exista erro.. passar para o s2idiagram tb!
                self.m_oGcDiagrams[t_nPage].SetErrorLog('')
                t_bEverythingOk = True
                for step in t_Sm.NewInstance(t_lsProcessChain):
                    if len(step) > 1:
                        if step[1] != '' and step[1] != None:
                            self.m_oGcDiagrams[t_nPage].Append2ErrorLog(step[1])
                            t_bEverythingOk = False
                    self.SetStatusMessage(step[0], t_bEverythingOk)
                    # self.widgets['StatusLabel'].set_text()
                    # print t_bEverythingOk
                    print step[0]
                # yield step#util caso se resolva usar a interface "lenta" ou se descubra como atualizar rapidamente a GUI

        # falta pegar o retorno!!!!!!
        self.UpdateStatus(7)

    # ----------------------------------------------------------------------
    def on_ProcessToolBar_clicked(self, *args):
        """
        Callback function called when ProcessToolBar is clicked. Starts communication with Backend and process the Chain.
        """
        self.UpdateStatus(0)
        self.widgets['ProcessToolBar'].set_sensitive(False)
        self.widgets['CodeToolBar'].set_sensitive(False)

        #######################################################################
        # We have two choices here, we could run with delays so all the numb info is displayed in the GUI
        # id2 = gobject.timeout_add(200,self.on_ProcessToolBar_clickedGenerator(self).next) #remember to uncomment the yield at line 842
        #
        # OORR
        # we could just iterate through it as fast as possible
        self.on_ProcessToolBar_clickedIneer()
        self.widgets['ProcessToolBar'].set_sensitive(True)
        self.widgets['CodeToolBar'].set_sensitive(True)

    # ----------------------------------------------------------------------
    def on_CodeToolBar_clickedIneer(self):
        t_nPage = self.widgets['WorkArea'].get_current_page()
        if not self.m_oGcDiagrams.has_key(t_nPage):
            self.widgets['CodeToolBar'].set_sensitive(True)
            # message
            self.SetStatusMessage(_("Could not find current diagram"), 1)
            return

        t_oDialog = gtk.FileChooserDialog(_("Save Program Source..."),
                                          None,
                                          gtk.FILE_CHOOSER_ACTION_SAVE,
                                          (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        t_oDialog.set_default_response(gtk.RESPONSE_OK)

        if os.name == 'posix':
            t_oDialog.set_current_folder(os.path.expanduser("~"))

        t_oFilter = gtk.FileFilter()
        t_oFilter.set_name(_("C Code File (*.c)"))
        t_oFilter.add_pattern("*.c")
        t_oDialog.add_filter(t_oFilter)

        t_oFilter = gtk.FileFilter()
        t_oFilter.set_name(_("All Files"))
        t_oFilter.add_pattern("*")
        t_oDialog.add_filter(t_oFilter)

        t_oResponse = t_oDialog.run()

        if t_oResponse == gtk.RESPONSE_OK:
            t_sOutputName = t_oDialog.get_filename()

            if not t_sOutputName.endswith('.c'):
                t_sOutputName += '.c'

            t_sTmpName = "harpiaBETMP0" + str(self.m_oGcDiagrams[t_nPage].GetIDBackendSession())
            t_sBigCodePath = "/tmp/" + t_sTmpName + "/" + t_sTmpName + ".c"
            if not os.path.exists(t_sBigCodePath):
                # message regarding code absence
                self.SetStatusMessage(_("Could not save code"), 1)
            else:
                # t_oOriginalFile = open(t_sBigCodePath)#abrindo o arquivo original la no /tmp
                shutil.copy(t_sBigCodePath, t_sOutputName)
                self.UpdateStatus(10)
        t_oDialog.destroy()

    # ----------------------------------------------------------------------
    def on_CodeToolBar_clicked(self, *args):
        self.widgets['ProcessToolBar'].set_sensitive(False)
        self.widgets['CodeToolBar'].set_sensitive(False)
        #	self.on_ProcessToolBar_clicked(self, *args)

        self.SetStatusMessage(_("Saving the last generated code"), 0)
        if self.m_nStatus != 7:
            self.on_ProcessToolBar_clicked()

        self.on_CodeToolBar_clickedIneer()
        self.widgets['ProcessToolBar'].set_sensitive(True)
        self.widgets['CodeToolBar'].set_sensitive(True)

    # id3 = gobject.timeout_add(1000,self.on_CodeToolBar_clickedGenerator(self, *args).next)


    # ----------------------------------------------------------------------

    def on_ZoomOutToolBar_clicked(self, *args):
        """
        Just ZoomOut the current page. Exponentialy, thus preventing the "0 pixels_per_unit bug"
        """
        t_nPage = self.widgets['WorkArea'].get_current_page()
        if self.m_oGcDiagrams.has_key(t_nPage):
            t_oGcDiagram = self.m_oGcDiagrams[t_nPage]
            t_oGcDiagram.ZoomOut()

    # ----------------------------------------------------------------------

    def on_ZoomInToolBar_clicked(self, *args):
        """
        Just ZoomIn the current view.
        """
        t_nPage = self.widgets['WorkArea'].get_current_page()
        if self.m_oGcDiagrams.has_key(t_nPage):
            t_oGcDiagram = self.m_oGcDiagrams[t_nPage]
            t_oGcDiagram.ZoomIn()

    # ----------------------------------------------------------------------

    def on_ZoomDefaultToolBar_clicked(self, *args):
        """
        Just back to the default zoom view.
        """
        t_nPage = self.widgets['WorkArea'].get_current_page()
        if self.m_oGcDiagrams.has_key(t_nPage):
            t_oGcDiagram = self.m_oGcDiagrams[t_nPage]
            t_oGcDiagram.ZoomOrig()

    # ----------------------------------------------------------------------

    def on_UpdateToolBar_clicked(self, *args):
        """
        Callback function called when Update is clicked. Update this Harpia version with the last in the server.
        """
        pass

        # ----------------------------------------------------------------------

    def on_ViewSource_clicked(self, *args):
        """
        Callback function called when ViewSource is clicked.

        """
        win = gtk.Window()
        #		win.connect("delete-event", gtk.main_quit)
        sw = gtk.ScrolledWindow()
        win.add(sw)
        sw.show()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        textview.set_left_margin(10)
        textview.set_right_margin(10)
        textbuffer = textview.get_buffer()
        sw.add(textview)
        textview.show()
        win.show_all()
        win.resize(800, 600)

        t_nPage = self.widgets['WorkArea'].get_current_page()
        t_sTmpName = "harpiaBETMP0" + str(self.m_oGcDiagrams[t_nPage].GetIDBackendSession())
        t_sBigCodePath = "/tmp/" + t_sTmpName + "/" + t_sTmpName + ".c"
        temp_file = open(t_sBigCodePath, 'r')
        string = temp_file.read()
        temp_file.close()
        textbuffer.set_text(string)

    # ----------------------------------------------------------------------

    def on_Preferences_clicked(self, *args):
        """
        Callback function called when Preferences is clicked. Loads the preferences window.
        """
        from harpia import preferences
        Prefs = preferences.Preferences(self)
        Prefs.show(center=0)

    # execfile( "preferences.py", {"Editor":self} )

    # ----------------------------------------------------------------------

    def on_Export_clicked(self, *args):
        """
        Callback function called when Export is clicked. Calls the Execute function in s2ipngexport class, that saves a blocks diagram in a .png file.
        """

        if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):

            t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]
            t_oDialog = gtk.FileChooserDialog(_("Export Diagram to PNG..."),
                                              None,
                                              gtk.FILE_CHOOSER_ACTION_SAVE,
                                              (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                               gtk.STOCK_SAVE, gtk.RESPONSE_OK))

            t_oDialog.set_default_response(gtk.RESPONSE_OK)

            if os.name == 'posix':
                t_oDialog.set_current_folder(os.path.expanduser("~"))

            t_oFilter = gtk.FileFilter()
            t_oFilter.set_name(_("Png files"))
            t_oFilter.add_pattern("*.png")
            t_oDialog.add_filter(t_oFilter)

            t_oResponse = t_oDialog.run()

            filename = t_oDialog.get_filename()

            if not filename.endswith(".png"):
                filename += ".png"
            t_oDialog.destroy()

            while gtk.events_pending():
                gtk.main_iteration(False)

            if t_oResponse == gtk.RESPONSE_OK:
                del t_oResponse
                del t_oDialog
                while gtk.events_pending():
                    gtk.main_iteration(False)
                t_oGcDiagram.Export2Png(filename)

    # ----------------------------------------------------------------------

    def on_SearchButton_clicked(self, *args):
        """
        Callback function called when SearchButton is clicked. Search for block and shows it.

        """
        # Get the text
        t_sSearchValue = self.widgets['SearchEntry'].get_text().lower()

        if len(t_sSearchValue) == 0:
            return

        for t_nClassIndex, t_sClassName in enumerate(self.Blocks.keys()):

            t_sClassNameLow = t_sClassName.lower()

            if t_sClassNameLow.find(t_sSearchValue) != -1:
                self.widgets['BlocksTreeView'].collapse_all()

                self.widgets['BlocksTreeView'].expand_row((t_nClassIndex), True)

                self.widgets['BlocksTreeView'].set_cursor((t_nClassIndex))

                return

            for t_nBlockIndex, t_sBlockName in enumerate(self.Blocks[t_sClassName]):

                t_sBlockName = t_sBlockName.lower()

                if t_sBlockName.find(t_sSearchValue) != -1:
                    self.widgets['BlocksTreeView'].collapse_all()

                    self.widgets['BlocksTreeView'].expand_to_path((t_nClassIndex, t_nBlockIndex))

                    self.widgets['BlocksTreeView'].set_cursor((t_nClassIndex, t_nBlockIndex))

                    return

    # ----------------------------------------------------------------------


    # VERY WEIRD!!!!!
    # YES, I TRYED making on_BlocksTreeView_row_activated just calling on_BlocksTreeView_row_activated_pos(...,0,0) but it didn't worked.. so.. fuck it..

    def on_BlocksTreeView_row_activated(self, treeview, path, column):
        """
        Callback function called when BlocksTreeView_row is activated. Loads the block in the diagram.
        """
        t_oTreeViewModel = treeview.get_model()
        t_sBlockName = t_oTreeViewModel.get_value(t_oTreeViewModel.get_iter(path), 0)

        if t_sBlockName not in self.Blocks.keys():
            t_nPage = self.widgets['WorkArea'].get_current_page()

            if self.m_oGcDiagrams.has_key(t_nPage):
                t_oCurrentGcDiagram = self.m_oGcDiagrams[t_nPage]
                t_nBlockType = -1

                for t_oBlockTypeIter in s2idirectory.block.keys():
                    if s2idirectory.block[int(t_oBlockTypeIter)]["Label"] == t_sBlockName:
                        t_nBlockType = t_oBlockTypeIter
                        break
                t_oCurrentGcDiagram.InsertBlock(t_nBlockType)

    def on_BlocksTreeView_row_activated_pos(self, treeview, path, column, x, y):
        """
        Callback function called when BlocksTreeView_row is activated. Loads the block in the diagram.
        """
        t_oTreeViewModel = treeview.get_model()

        t_sBlockName = t_oTreeViewModel.get_value(t_oTreeViewModel.get_iter(path), 0)

        if t_sBlockName not in self.Blocks.keys():

            t_nPage = self.widgets['WorkArea'].get_current_page()

            if self.m_oGcDiagrams.has_key(t_nPage):

                t_oCurrentGcDiagram = self.m_oGcDiagrams[t_nPage]

                t_nBlockType = -1

                for t_oBlockTypeIter in s2idirectory.block.keys():

                    if s2idirectory.block[int(t_oBlockTypeIter)]["Label"] == t_sBlockName:
                        t_nBlockType = t_oBlockTypeIter

                        break
                t_oCurrentGcDiagram.InsertBlock(t_nBlockType, x, y)

    # ----------------------------------------------------------------------

    def on_BlocksTreeView_cursor_changed(self, treeview):
        """
        Callback function called when BlocksTreeView cursor changed. Updates the Description.
        """

        t_oTreeViewSelection = treeview.get_selection()

        (t_oTreeViewModel, t_oTreeViewIter) = t_oTreeViewSelection.get_selected()

        if t_oTreeViewIter != None:

            t_sBlockName = t_oTreeViewModel.get_value(t_oTreeViewIter, 0)

            for x in s2idirectory.block:
                if s2idirectory.block[x]["Label"] == t_sBlockName:
                    t_oTextBuffer = gtk.TextBuffer()
                    t_oTextBuffer.set_text(s2idirectory.block[x]["Description"])
                    self.widgets['BlockDescription'].set_buffer(t_oTextBuffer)
                    break

    # ----------------------------------------------------------------------

    def OnEvent(self, a_oView, a_oEvent):
        print "OnEvent( self, a_oView, a_oEvent ) not implemented (it is distributed among diagram objects)"

    # ----------------------------------------------------------------------

    def fixBlockPositions(self):  # this function removes all the blocks of unreacheable states
        print "fixBlockPositions not implemented (it is distributed among diagram objects)"

    # ----------------------------------------------------------------------

    def on_HarpiaFrontend_destroy(self, *args):
        """
        Destroys the Harpia Window.
        """
        gtk.main_quit()

    # ----------------------------------------------------------------------

    def __CopyBlock(self, a_oBlock):
        """
        Receives a block and copy.
        """
        print "Copy not implemented"

    # ----------------------------------------------------------------------

    def on_CloseMenuBar_activate(self, *args):
        """
        Callback funtion called when CloseMenuBar is activated. Close the current diagram tab.
        """

        t_nCurrentTabIndex = self.widgets['WorkArea'].get_current_page()

        if t_nCurrentTabIndex <> -1:

            self.widgets["WorkArea"].remove_page(t_nCurrentTabIndex)

            if self.m_oGcDiagrams.has_key(t_nCurrentTabIndex):
                del self.m_oGcDiagrams[t_nCurrentTabIndex]

            t_oGcDiagrams = {}

            for t_nTabIndex, t_nOldTabIndex in enumerate(self.m_oGcDiagrams.keys()):
                t_oGcDiagrams[t_nTabIndex] = self.m_oGcDiagrams[t_nOldTabIndex]

            self.m_oGcDiagrams = t_oGcDiagrams

    # ----------------------------------------------------------------------

    def ShowGrid(self, a_bShowGrid):
        """
        Shows the grid or not based on the boolean received as argument.
        """
        print "no grids"

    # ----------------------------------------------------------------------

    def SetGridInterval(self, a_nGridInterval):
        """
        Defines the Grid interval and sets the diacanvas.
        """
        print "no grids"

    # ----------------------------------------------------------------------

    def LoadExample(self, *args):
        for example in self.exampleMenuItens:
            if example[0] == args[0]:
                self.on_NewToolBar_clicked()  # abrindo nova pagina
                if self.m_oGcDiagrams.has_key(self.widgets['WorkArea'].get_current_page()):
                    t_oGcDiagram = self.m_oGcDiagrams[self.widgets['WorkArea'].get_current_page()]
                    t_oGcDiagram.SetFilename(example[1])
                    if t_oGcDiagram.GetFilename() is not None:
                        if t_oGcDiagram.Load():
                            t_nCurrentPage = self.widgets['WorkArea'].get_current_page()
                            t_oChild = self.widgets['WorkArea'].get_nth_page(t_nCurrentPage)
                            t_sNewLabel = t_oGcDiagram.GetFilename().split("/").pop()
                            t_oLabel = gtk.Label(str(t_sNewLabel))
                            self.widgets['WorkArea'].set_tab_label(t_oChild, t_oLabel)

                        # print example[1]

    def LoadExamplesMenu(self):
        t_lListOfExamples = glob(self.m_sDataDir + "examples/*")
        t_lListOfExamples.sort()

        ##ALG to prevent using filenames with _ on the menus
        # t_lNewL = []
        # for s in t_lListOfExamples:
        # t_lNewL.append(s.replace("_","-"))
        # t_lListOfExamples = t_lNewL

        self.widgets['fake_separator'].destroy()
        self.widgets.pop('fake_separator')

        for example in t_lListOfExamples:
            t_oMenuItem = gtk.MenuItem(example.split("/").pop())
            self.widgets['examples_menu'].append(t_oMenuItem)
            t_oMenuItem.connect("activate", self.LoadExample)
            self.widgets['examples_menu'].show_all()
            self.exampleMenuItens.append((t_oMenuItem, example))
