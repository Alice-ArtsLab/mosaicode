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
from harpia import preferences
from harpia import about
from filefilters import *
from GUI.diagram import *
from diagramcontrol import DiagramControl 

import s2iSessionManager
import TipOfTheDay
import s2idirectory

# i18n
from constants import *
import gettext
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
        Constructor. Initializes the GladeWindow object for signal connecting, creates a dictionary for the Blocks and loads the configurations.
        """

        self.exampleMenuItens = []

        self.data_dir = os.environ['HARPIA_DATA_DIR']
        filename = self.data_dir + 'glade/harpia_gui-1.0.ui'

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
            'ViewSource',
            'toolbar1',
            'examples_menu',
            'fake_separator'
        ]

        handlers = [
            'on_NewMenuBar_activate',
            'on_OpenMenuBar_activate',
            'on_SaveMenuBar_activate',
            'on_SaveASMenuBar_activate',
            'on_QuitMenuBar_activate',
            'on_CutMenuBar_activate',
            'on_CopyMenuBar_activate',
            'on_PasteMenuBar_activate',
            'on_DeleteMenuBar_activate',
            'on_AboutMenuBar_activate',
            'on_NewToolBar_clicked',
            'on_OpenToolBar_clicked',
            'on_SaveToolBar_clicked',
            'on_ProcessToolBar_clicked',
            'on_CodeToolBar_clicked',
            'on_ZoomOutToolBar_clicked',
            'on_ZoomInToolBar_clicked',
            'on_SearchButton_clicked',
            'on_BlocksTreeView_row_activated',
            'on_BlocksTreeView_cursor_changed',
            'on_HarpiaFrontend_destroy',
            'on_ZoomDefaultToolBar_clicked',
            'on_Preferences_clicked',
            'on_Export_clicked',
            'on_CloseMenuBar_activate',
            'on_tip_activate',
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

        self.widgets['HarpiaFrontend'].set_icon_from_file(self.data_dir + "images/harpia_ave.png")
        self.tree_view_path = "0,0"

        self.status = 0
        self.SaveAs = False

        # Member Diagram references
        self.diagrams = {}
        self.copy_buffer = (-1, -1)  # tuple (fromPage, [listOfBlocks]) ...listOfConns?
        self.__load_examples_menu()
        self.__insert_blocks()
        self.on_CloseMenuBar_activate()  # removing the dummie page
        self.on_NewToolBar_clicked()  # creating blank page

        # Tip of The Day code
        tipOfTheDayWind = TipOfTheDay.TipOfTheDay()
        tipOfTheDayWind.run()

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def __insert_blocks(self):
        """
        Inserts the blocks in the BlocksTree.
        """

        tree_store = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
        image = gtk.CellRendererPixbuf()

        for item in self.Blocks.keys():
            parent = tree_store.append(None, [item, image])
            for index in range(len(self.Blocks[item])):
                tree_store.append(parent, [self.Blocks[item][index], image])

        self.widgets['BlocksTreeView'].set_model(tree_store)
        t_oTextRender = gtk.CellRendererText()
        t_oTextRender.set_property('editable', False)
        t_oColumn = gtk.TreeViewColumn(_("Available Blocks"), t_oTextRender, text=0)
        self.widgets['BlocksTreeView'].append_column(t_oColumn)


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
            [('text/plain', gtk.TARGET_SAME_APP, 1)],
            gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_COPY)

    # ----------------------------------------------------------------------
    def drag_data_received(self, widget, context, x, y, selection, targetType, time):
        # print("Shit Connected, Drop occurred at: (" + str(x) + "," + str(y) + ")")
        # erdtmann: dunno why 0, but it works (I suppose it's 'cos there's only one column in the tree)
        # path is the way to find the desired block on the treeview
        # g_iColumn = 0
        self.on_BlocksTreeView_row_activated_pos(self.widgets['BlocksTreeView'], self.tree_view_path, 0, x, y)
        return

    # ----------------------------------------------------------------------
    def drag_data_get_cb(self, treeview, context, selection, target_id, etime):
        treeselection = treeview.get_selection()
        model, iterac = treeselection.get_selected()
        self.tree_view_path = model.get_path(iterac)
        selection.set('text/plain', 8, "test")
        # necessary in order to the notebook receive the drag:
        return

    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    def on_reset_tip_activate(self, *args):
        tipOfTheDayWind = TipOfTheDay.TipOfTheDay()
        tipOfTheDayWind.GenerateBlankConf()

    # ----------------------------------------------------------------------
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
        if self.diagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            diagram = self.diagrams[self.widgets['WorkArea'].get_current_page()]
        self.copy_buffer = (self.widgets['WorkArea'].get_current_page(),
                              diagram.get_block_on_focus())
        print self.copy_buffer

    # ----------------------------------------------------------------------
    def on_PasteMenuBar_activate(self, *args):
        """
        Callback function called when PasteMenuBar is activated.
        Paste the copied block(s) in the diagram.
        """
        if self.copy_buffer[0] == -1:  # nothing copied
            return

        # print "pasting"

        if self.diagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            diagram = self.diagrams[self.widgets['WorkArea'].get_current_page()]

            if self.diagrams.has_key(self.copy_buffer[0]):
                t_oFromDiagram = self.diagrams[self.copy_buffer[0]]

                if t_oFromDiagram.blocks.has_key(self.copy_buffer[1]):
                    newBlockId = diagram.insert_block(t_oFromDiagram.blocks[self.copy_buffer[1]].get_type())
                    diagram.blocks[newBlockId].SetPropertiesXML_nID(
                        t_oFromDiagram.blocks[self.copy_buffer[1]].GetPropertiesXML())

    # ----------------------------------------------------------------------
    def on_DeleteMenuBar_activate(self, *args):
        """
        Callback function called when DeleteMenuBar is activated. Deletes the selected item.
        """
        if self.diagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            diagram = self.diagrams[self.widgets['WorkArea'].get_current_page()]
            blockId = diagram.get_block_on_focus()
            if diagram.blocks.has_key(blockId):
                diagram.delete_block(blockId)

    # ----------------------------------------------------------------------
    def on_AboutMenuBar_activate(self, *args):
        """
        Callback function called when AboutMenuBar is activated. Loads the about window.
        """
        About = about.About()
        About.show(center=0)

    # ----------------------------------------------------------------------
    def on_NewToolBar_clicked(self, *args):
        """
        Callback function called when NewToolBar is clicked. Creates a new tab with an empty diagram.
        """

        # maybe pass to a s2iView base class
        new_diagram = GcDiagram(self)  # created new diagram

        table = gtk.Table(2, 2, False)
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        table.attach(frame, 0, 1, 0, 1,
                        gtk.EXPAND | gtk.FILL | gtk.SHRINK,
                        gtk.EXPAND | gtk.FILL | gtk.SHRINK)

        frame.add(new_diagram)

        t_oVAdjustment = gtk.VScrollbar(new_diagram.get_vadjustment())
        t_oHAdjustment = gtk.HScrollbar(new_diagram.get_hadjustment())
        table.attach(t_oVAdjustment, 1, 2, 0, 1, gtk.FILL, gtk.EXPAND | gtk.FILL | gtk.SHRINK)
        table.attach(t_oHAdjustment, 0, 1, 1, 2, gtk.EXPAND | gtk.FILL | gtk.SHRINK, gtk.FILL)
        table.show_all()

        # tab label
        current_page = self.widgets['WorkArea'].get_current_page()

        label = gtk.Label(_("Unnamed ") + str(current_page + 1) + "[*]")

        self.widgets['WorkArea'].set_show_tabs(True)
        self.widgets['WorkArea'].append_page(table, label)

        t_nSelectedPage = self.widgets['WorkArea'].get_n_pages() - 1
        self.widgets['WorkArea'].set_current_page(t_nSelectedPage)

        self.diagrams[self.widgets['WorkArea'].get_current_page()] = new_diagram


    # ----------------------------------------------------------------------
    def on_OpenToolBar_clicked(self, *args):
        # Opens a dialog for file selection and opens the file.

        t_oDialog = gtk.FileChooserDialog(_("Open..."),
                                          None,
                                          gtk.FILE_CHOOSER_ACTION_OPEN,
                                          (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        t_oDialog.set_default_response(gtk.RESPONSE_OK)
        file_name = ''

        if os.name == 'posix':
            t_oDialog.set_current_folder(os.path.expanduser("~"))

        t_oDialog.add_filter(AllFileFilter())
        t_oDialog.add_filter(HarpiaFileFilter())

        t_oResponse = t_oDialog.run()

        if t_oResponse == gtk.RESPONSE_OK:
            self.on_NewToolBar_clicked()
            current_page = self.widgets['WorkArea'].get_current_page()
            diagram = self.diagrams[current_page]
            if len(t_oDialog.get_filename()) > 0:
                file_name = t_oDialog.get_filename()
        t_oDialog.destroy()

        self.open_diagram(file_name)

    # ----------------------------------------------------------------------
    def on_SaveToolBar_clicked(self, *args):
        # Opens a dialog for file and path selection. Saves the file and if necessary updates the tab name.

        if self.diagrams.has_key(self.widgets['WorkArea'].get_current_page()):

            diagram = self.diagrams[self.widgets['WorkArea'].get_current_page()]

            if diagram.get_file_name() is None or self.SaveAs:
                self.SaveAs = False

                t_oDialog = gtk.FileChooserDialog(_("Save..."),
                                                  None,
                                                  gtk.FILE_CHOOSER_ACTION_SAVE,
                                                  (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_SAVE, gtk.RESPONSE_OK))
                t_oDialog.set_default_response(gtk.RESPONSE_OK)

                if os.name == 'posix':
                    t_oDialog.set_current_folder(os.path.expanduser("~"))

                t_oDialog.add_filter(AllFileFilter())
                t_oDialog.add_filter(HarpiaFileFilter())

                t_oResponse = t_oDialog.run()
                if t_oResponse == gtk.RESPONSE_OK:
                    diagram.set_file_name(t_oDialog.get_filename())

                t_oDialog.destroy()

            if diagram.get_file_name() is not None:
                if len(diagram.get_file_name()) > 0:
                    DiagramControl(diagram).save()
                    new_label_len = int(len(diagram.get_file_name().split("/")) - 1)
                    new_label = diagram.get_file_name().split("/")[new_label_len]
                    self.__update_tab_name(new_label)

    # ----------------------------------------------------------------------
    def __update_tab_name(self, name):
        current_page = self.widgets['WorkArea'].get_current_page()
        child = self.widgets['WorkArea'].get_nth_page(current_page)
        label = gtk.Label(str(name))
        self.widgets['WorkArea'].set_tab_label(child, label)

    # ----------------------------------------------------------------------
    def UpdateStatus(self, a_nStatus):
        """
        Receives a status and shows in the StatusBar.
        """

        self.status = a_nStatus

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

        self.widgets['StatusLabel'].set_text(t_oStatusMessage[a_nStatus])

        while gtk.events_pending():
            gtk.main_iteration(False)

    # ----------------------------------------------------------------------
    def __set_status_message(self, a_sStatus, a_bGood):
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
        page = self.widgets['WorkArea'].get_current_page()
        if self.diagrams.has_key(page):
            self.UpdateStatus(0)

            diagram = self.diagrams[page]

            process_XML = XMLParser("<harpia>" + \
                                           str(DiagramControl(diagram).get_process_chain()) + \
                                           "</harpia>", fromString=True)

            graph_size = len(list(process_XML.getTag("harpia").getTag("properties").getTagChildren()))

            if graph_size > 1:
                blocks = process_XML.getTag("harpia").getTag("properties").getChildTags("block")
                for t_oBlockProperties in blocks:
                    block_properties = t_oBlockProperties.getChildTags("property")
                    if int(t_oBlockProperties.type) == 00:  # 00 = acquisition block
                        inputType = 'file'
                        for block_property in block_properties:
                            if block_property.name == 'type':
                                print block_property.name
                                inputType = block_property.value

                            # adoção do paradigma monolítico.. nada de ficar mandando imagens por sockets!!
                            if block_property.name == 'filename' and inputType == 'file':
                                block_property.value = os.path.expanduser(block_property.value)
                                block_property.value = os.path.realpath(block_property.value)
                                if (not os.path.exists(block_property.value)):
                                    errMsg = _("Bad Filename: ") + block_property.value
                                    print(errMsg)
                                    self.__set_status_message(errMsg, 0)
                                    return

                    if int(t_oBlockProperties.type) == 01:  # 01 => save image
                        for block_property in block_properties:
                            if block_property.name == 'filename':
                                block_property.value = os.path.realpath(block_property.value)


                    # seguindo o paradigma de não mandar mais nada.. vamos testar com o haar =]
                    # não vamos mandar mais nada mas vamos traduzir o path do haarCascade pra algo real
                    if int(t_oBlockProperties.type) == 610:  # 610 => haar detector... passando a cascade .xml
                        for block_property in block_properties:
                            if block_property.name == 'cascade_name':
                                block_property.value = os.path.realpath(block_property.value)
                                if (not os.path.exists(block_property.value)):
                                    errMsg = _("Bad Filename: ") + block_property.value
                                    print(errMsg)
                                    self.__set_status_message(errMsg, 0)
                                    return

                # cpscotti standalone!!!
                process_chain = []  # lista pra n precisar ficar copiando prum lado e pro otro o xml inteiro
                process_chain.append(process_XML.getXML())

                session_manager = s2iSessionManager.s2iSessionManager()

                ## pegando o novo ID (criado pela s2iSessionManager) e passando para o s2idiagram
                self.diagrams[page].set_session_id(session_manager.session_id)

                # step sempre sera uma lista.. primeiro elemento eh uma mensagem, segundo eh o erro.. caso exista erro.. passar para o s2idiagram tb!
                self.diagrams[page].set_error_log('')
                t_bEverythingOk = True
                for step in session_manager.new_instance(process_chain):
                    if len(step) > 1:
                        if step[1] != '' and step[1] != None:
                            self.diagrams[page].append_error_log(step[1])
                            t_bEverythingOk = False
                    self.__set_status_message(step[0], t_bEverythingOk)
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
        page = self.widgets['WorkArea'].get_current_page()
        if not self.diagrams.has_key(page):
            self.widgets['CodeToolBar'].set_sensitive(True)
            # message
            self.__set_status_message(_("Could not find current diagram"), 1)
            return

        t_oDialog = gtk.FileChooserDialog(_("Save Program Source..."),
                                          None,
                                          gtk.FILE_CHOOSER_ACTION_SAVE,
                                          (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        t_oDialog.set_default_response(gtk.RESPONSE_OK)

        if os.name == 'posix':
            t_oDialog.set_current_folder(os.path.expanduser("~"))

        t_oDialog.add_filter(AllFileFilter())
        t_oDialog.add_filter(CCodeFileFilter())


        t_oResponse = t_oDialog.run()

        if t_oResponse == gtk.RESPONSE_OK:
            t_sOutputName = t_oDialog.get_filename()

            if not t_sOutputName.endswith('.c'):
                t_sOutputName += '.c'

            t_sTmpName = "harpiaBETMP0" + str(self.diagrams[page].get_session_id())
            t_sBigCodePath = "/tmp/" + t_sTmpName + "/" + t_sTmpName + ".c"
            if not os.path.exists(t_sBigCodePath):
                # message regarding code absence
                self.__set_status_message(_("Could not save code"), 1)
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

        self.__set_status_message(_("Saving the last generated code"), 0)
        if self.status != 7:
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
        page = self.widgets['WorkArea'].get_current_page()
        if self.diagrams.has_key(page):
            diagram = self.diagrams[page]
            diagram.set_zoom(ZOOM_OUT)

    # ----------------------------------------------------------------------
    def on_ZoomInToolBar_clicked(self, *args):
        """
        Just ZoomIn the current view.
        """
        page = self.widgets['WorkArea'].get_current_page()
        if self.diagrams.has_key(page):
            diagram = self.diagrams[page]
            diagram.set_zoom(ZOOM_IN)

    # ----------------------------------------------------------------------
    def on_ZoomDefaultToolBar_clicked(self, *args):
        """
        Just back to the default zoom view.
        """
        page = self.widgets['WorkArea'].get_current_page()
        if self.diagrams.has_key(page):
            diagram = self.diagrams[page]
            diagram.set_zoom(ZOOM_ORIGINAL)

    # ----------------------------------------------------------------------
    def on_ViewSource_clicked(self, *args):
        """
        Callback function called when ViewSource is clicked.

        """
        win = gtk.Window()
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

        page = self.widgets['WorkArea'].get_current_page()
        t_sTmpName = "harpiaBETMP0" + str(self.diagrams[page].get_session_id())
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
        Prefs = preferences.Preferences(self)
        Prefs.show(center=0)

    # ----------------------------------------------------------------------
    def on_Export_clicked(self, *args):
        """
        Callback function called when Export is clicked. Calls the Execute function in s2ipngexport class, that saves a blocks diagram in a .png file.
        """

        if self.diagrams.has_key(self.widgets['WorkArea'].get_current_page()):

            diagram = self.diagrams[self.widgets['WorkArea'].get_current_page()]
            t_oDialog = gtk.FileChooserDialog(_("Export Diagram to PNG..."),
                                              None,
                                              gtk.FILE_CHOOSER_ACTION_SAVE,
                                              (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                               gtk.STOCK_SAVE, gtk.RESPONSE_OK))

            t_oDialog.set_default_response(gtk.RESPONSE_OK)

            if os.name == 'posix':
                t_oDialog.set_current_folder(os.path.expanduser("~"))

            t_oDialog.add_filter(PNGFileFilter())
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
                DiagramControl(diagram).export_png(filename)

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

            for t_nBlockIndex, block_name in enumerate(self.Blocks[t_sClassName]):
                block_name = block_name.lower()
                if block_name.find(t_sSearchValue) != -1:
                    self.widgets['BlocksTreeView'].collapse_all()
                    self.widgets['BlocksTreeView'].expand_to_path((t_nClassIndex, t_nBlockIndex))
                    self.widgets['BlocksTreeView'].set_cursor((t_nClassIndex, t_nBlockIndex))
                    return

    # ----------------------------------------------------------------------
    def on_BlocksTreeView_row_activated(self, treeview, path, column):
        """
        Callback function called when BlocksTreeView_row is activated. Loads the block in the diagram.
        """
        tree_view_model = treeview.get_model()
        block_name = tree_view_model.get_value(tree_view_model.get_iter(path), 0)

        if block_name not in self.Blocks.keys():
            page = self.widgets['WorkArea'].get_current_page()

            if self.diagrams.has_key(page):
                t_oCurrentGcDiagram = self.diagrams[page]
                t_nBlockType = -1

                for t_oBlockTypeIter in s2idirectory.block.keys():
                    if s2idirectory.block[int(t_oBlockTypeIter)]["Label"] == block_name:
                        t_nBlockType = t_oBlockTypeIter
                        break
                t_oCurrentGcDiagram.insert_block(t_nBlockType)

    # ----------------------------------------------------------------------
    def on_BlocksTreeView_row_activated_pos(self, treeview, path, column, x, y):
        """
        Callback function called when BlocksTreeView_row is activated. Loads the block in the diagram.
        """
        tree_view_model = treeview.get_model()
        block_name = tree_view_model.get_value(tree_view_model.get_iter(path), 0)

        if block_name not in self.Blocks.keys():
            page = self.widgets['WorkArea'].get_current_page()
            if self.diagrams.has_key(page):
                t_oCurrentGcDiagram = self.diagrams[page]
                t_nBlockType = -1
                for t_oBlockTypeIter in s2idirectory.block.keys():
                    if s2idirectory.block[int(t_oBlockTypeIter)]["Label"] == block_name:
                        t_nBlockType = t_oBlockTypeIter
                        break
                t_oCurrentGcDiagram.insert_block(t_nBlockType, x, y)

    # ----------------------------------------------------------------------
    def on_BlocksTreeView_cursor_changed(self, treeview):
        """
        Callback function called when BlocksTreeView cursor changed. Updates the Description.
        """

        t_oTreeViewSelection = treeview.get_selection()
        (tree_view_model, t_oTreeViewIter) = t_oTreeViewSelection.get_selected()
        if t_oTreeViewIter != None:
            block_name = tree_view_model.get_value(t_oTreeViewIter, 0)
            for x in s2idirectory.block:
                if s2idirectory.block[x]["Label"] == block_name:
                    t_oTextBuffer = gtk.TextBuffer()
                    t_oTextBuffer.set_text(s2idirectory.block[x]["Description"])
                    self.widgets['BlockDescription'].set_buffer(t_oTextBuffer)
                    break

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
        current_tab_index = self.widgets['WorkArea'].get_current_page()
        if current_tab_index <> -1:
            self.widgets["WorkArea"].remove_page(current_tab_index)
            if self.diagrams.has_key(current_tab_index):
                del self.diagrams[current_tab_index]
            diagrams = {}
            for t_nTabIndex, t_nOldTabIndex in enumerate(self.diagrams.keys()):
                diagrams[t_nTabIndex] = self.diagrams[t_nOldTabIndex]
            self.diagrams = diagrams

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
    def __load_example(self, *args):
        for example in self.exampleMenuItens:
            if example[0] == args[0]:
                self.on_NewToolBar_clicked()  # abrindo nova pagina
                self.open_diagram(example[1])

    # ----------------------------------------------------------------------
    def open_diagram(self, diagram_name):
        if self.diagrams.has_key(self.widgets['WorkArea'].get_current_page()):
            diagram = self.diagrams[self.widgets['WorkArea'].get_current_page()]
            diagram.set_file_name(diagram_name)
            if DiagramControl(diagram).load():
                new_label = diagram.get_file_name().split("/").pop()
                self.__update_tab_name(new_label)

    # ----------------------------------------------------------------------
    def __load_examples_menu(self):
        list_of_examples = glob(self.data_dir + "examples/*")
        list_of_examples.sort()

        self.widgets['fake_separator'].destroy()
        self.widgets.pop('fake_separator')

        for example in list_of_examples:
            menu_item = gtk.MenuItem(example.split("/").pop())
            self.widgets['examples_menu'].append(menu_item)
            menu_item.connect("activate", self.__load_example)
            self.widgets['examples_menu'].show_all()
            self.exampleMenuItens.append((menu_item, example))
