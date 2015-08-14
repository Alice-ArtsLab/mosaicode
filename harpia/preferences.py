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
from GladeWindow import GladeWindow
from amara import binderytools as bt
import shutil
import os



# ----------------------------------------------------------------------
## Implements the preferences window
class Preferences(GladeWindow):
    """
        This class shows the preferences, and handles the signals.
        Is derived from GladeWindow and allows the user to edit their preferences.
        The preferences are stored in a harpia.conf file and this file is loaded when harpia is initialized.
    """

    # The s2iharpiafrontend object (Editor)


    # ----------------------------------------------------------------------

    def __init__(self, Editor):
        """
            The Constructor. Loads the glade object, and initializes the GladeWindow object for signal connecting.
        """

        self.m_oEditor = Editor
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']

        ## Imports the Glade file
        filename = self.m_sDataDir + 'glade/preferences.ui'

        # The widget list
        widget_list = ['preferences',
                       'PREFGridInt',
                       'PREFShowGrid',
                       'PREFServer',
                       'PREFPort']

        # Signal Handlers from the Buttons Confirm and Cancel
        handlers = ['on_preferences_confirm_clicked',
                    'on_preferences_cancel_clicked']

        # The Top window widget
        top_window = 'preferences'

        # Starts the GladeWindow, calling his __init__ method.
        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        # Set the preferences Icon
        self.widgets['preferences'].set_icon_from_file(self.m_sDataDir + "images/harpia_ave.png")

        ## The Homefolder where the preferences will be stored.
        if os.name == "nt":
            self.HomeFolder = os.path.join(os.path.expanduser("~"), "harpiaFiles\\")
        else:
            self.HomeFolder = os.path.expanduser("~/harpiaFiles/")
        #        self.HomeFolder = "/tmp/.harpia/"

        ## The Config File Path
        self.configfile = self.HomeFolder + "harpia.conf"

        # If the path do not exist, creates one.
        if not (os.path.exists(self.HomeFolder)):
            os.makedirs(self.HomeFolder, mode=0700)

        # If the path do not exist, creates one copyint the default harpia.conf.
        if not (os.path.exists(self.configfile)):
            shutil.copy("harpia.conf", self.HomeFolder)

        print "TESTE" + self.configfile
        ## A binderytool object, with the preferences stored
        self.m_oPreferencesXML = bt.bind_file(self.configfile)


        # ---------------------------------


        # Load Preferences
        for Preference in self.m_oPreferencesXML.harpia.editor.property:

            if Preference.name == "show-grid":
                if Preference.value == "false":
                    state = "False"
                else:
                    state = "True"
                self.widgets['PREFShowGrid'].set_active(eval(state))

            if Preference.name == "grid-int":
                self.widgets['PREFGridInt'].set_value(int(Preference.value))

            if Preference.name == "server":
                self.widgets['PREFServer'].set_text(unicode(Preference.value))

            if Preference.name == "port":
                self.widgets['PREFPort'].set_value(int(Preference.value))


                # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    # Confirm Button handler function
    def on_preferences_confirm_clicked(self, *args):
        """
        This function is called whenever the confirm button on the preferences window is clicked.
        It stores the preferences in the configfile.
        """
        for Preference in self.m_oPreferencesXML.harpia.editor.property:
            if Preference.name == "show-grid":
                if self.widgets['PREFShowGrid'].get_active():
                    Preference.value = unicode("true")
                    self.m_oEditor.ShowGrid(True)
                else:
                    Preference.value = unicode("false")
                    self.m_oEditor.ShowGrid(False)

            if Preference.name == "grid-int":
                Preference.value = unicode(str(int(self.widgets['PREFGridInt'].get_value())))
                self.m_oEditor.SetGridInterval(int(Preference.value))

            if Preference.name == "server":
                Preference.value = unicode(self.widgets['PREFServer'].get_text())

            if Preference.name == "port":
                Preference.value = unicode(str(int(self.widgets['PREFPort'].get_value())))


                # -------------------------------------------

            #         Editor = "\n<editor>" + "\n</editor>\n"
            #         Block = "\n<block>" + "\n</block>\n"
            #         Connector = "\n<connector>" + "\n</connector>\n"
            #         Harpia = "<harpia>" + Editor + Block + Connector + "</harpia>"

        # Opens the configFile for writing
        FileHandle = open(self.configfile, "w")
        # Writes the preferences
        FileHandle.write(self.m_oPreferencesXML.xml())
        # Close the FIle
        FileHandle.close()

        # -------------------------------------------
        # Destroy the preferences window
        self.widgets['preferences'].destroy()

    # ----------------------------------------------------------------------
    # Cancel Button handler function
    def on_preferences_cancel_clicked(self, *args):
        """
        This function is called whenever the cancel button on the preferences window is clicked.
        It just exits the window without saving any changes.
        """
        # Just destroy the window, without savind the changes
        self.widgets['preferences'].destroy()

        # ----------------------------------------------------------------------

# Preferences = Preferences()
# Preferences.show( center=0 )
