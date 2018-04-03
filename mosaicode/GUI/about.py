# -*- coding: utf-8 -*-
"""
This module contains the class About.
"""

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.system import System as System
import gettext
_ = gettext.gettext


class About(Gtk.Window):
    """
    This class contains methods related the About class
    This class contains the information about the project.
    """

    def __init__(self, main_window):
        """
        This method is the constuctor.

          Parameters:
            * **Types** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
        """
        self.data_dir = System.DATA_DIR
        Gtk.Window.__init__(self, title=_("About Mosaicode"))
        self.set_default_size(650, 480)

        grid = Gtk.Grid()
        self.add(grid)

        # -----------------------logo mosaicode----------------------------------#

        image = Gtk.Image()
        image.set_from_file(self.data_dir + "images/mosaicode2.png")

        frame = Gtk.Frame()
        frame.set_border_width(2)
        frame.add(image)

        frameBorder = Gtk.Frame()
        frameBorder.set_border_width(10)
        frameBorder.add(frame)

        grid.add(frameBorder)

        # --------------------------------------------------------------------#
        # -------------------------------About Text---------------------------#

        labelAbout = Gtk.Label(_('Mosaicode Project intends to build a ' +
                                 'graphical environment for learning,\n' +
                                 'implementing and management of machine ' +
                                 'vision systems.\n\nThe system is ' +
                                 '(would-be) made of several software ' +
                                 'modules for hardware\ncomunication, ' +
                                 'image (signal) processing and remote ' +
                                 'management of\nvision systems.\n\n' +
                                 'The system could be used in industries ' +
                                 'or acadamics, making easier to\n' +
                                 'develop quality control systems, and ' +
                                 'vision system based process,\n' +
                                 'helping the learning and spreading of ' +
                                 'vision systems.'))
        aboutBox = Gtk.Box()
        aboutBox.add(labelAbout)
        aboutBox.set_border_width(35)

        # --------------------------------------------------------------------#
        # ----------------------------License Text----------------------------#

        labelLicense = Gtk.Label(_('Mosaicode\n' +
                                   'Copyright (C) 2018\n\n' +
                                   'This program is free software: you can ' +
                                   ' redistribute it and/or modify\n' +
                                   'it under the terms of the GNU General  ' +
                                   'Public License as published by\n' +
                                   'the Free Software Foundation, either  ' +
                                   'version 3 of the License, or\n' +
                                   '(at your option) any later version.\n' +
                                   'This program is distributed in the hope' +
                                   'that it will be useful,\n' +
                                   'but WITHOUT ANY WARRANTY; without even  ' +
                                   'the implied warranty of\n' +
                                   'MERCHANTABILITY or FITNESS FOR A  ' +
                                   'PARTICULAR PURPOSE.  See the\n' +
                                   'GNU General Public License for more  ' +
                                   'details.\n\n' +
                                   'You should have received a copy of the  ' +
                                   'GNU General Public License\n' +
                                   'along with this program.  If not, ' +
                                   'see www.gnu.org/licenses.'))

        labelLicense.set_justify(Gtk.Justification.CENTER)

        frameLicense = Gtk.Frame()
        frameLicense.set_border_width(10)
        frameLicense.add(labelLicense)

        # --------------------------------------------------------------------#
        # -----------------------------Development part-----------------------#
        labelDevelopment = Gtk.Label(_("Development"))
        labelDevelopment.set_markup(_("<b>Development</b>"))

        imageDevelopment = Gtk.Image()
        imageDevelopment.set_from_file(self.data_dir + "images/mosaicode64x64.ico")

        labelDevelopmentText = Gtk.Label(_('Departamento ' +
                                           'de Ciência da Computação\n' +
                                           'Universidade Federal ' +
                                           'de São João del Rei\n\n' +
                                           'Bits & Beads Research Lab\n'))

        labelDevelopmentText.set_justify(Gtk.Justification.CENTER)

        textBox = Gtk.Box()
        textBox.add(labelDevelopmentText)

        imgbox = Gtk.Box()
        imgbox.add(imageDevelopment)

        developmentBox = Gtk.Box()
        developmentBox.set_spacing(315)
        developmentBox.add(imgbox)
        developmentBox.add(textBox)

        frame2 = Gtk.Frame()
        frame2.set_label_widget(labelDevelopment)
        frame2.set_size_request(635, 262)
        frame2.set_border_width(10)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)

        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left.set_homogeneous(False)
        vbox_left.set_border_width(5)
        vbox_center = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_center.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)
        vbox_right.set_border_width(5)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_center, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        gridFrame = Gtk.Grid()
        gridFrame.add(developmentBox)

        x = Gtk.Separator()

        gridFrame.attach_next_to(x, developmentBox,
                                 Gtk.PositionType.BOTTOM, 1, 2)
        gridFrame.attach_next_to(hbox, x, Gtk.PositionType.BOTTOM, 1, 2)

        labelFinal = Gtk.Label(_('Any bugs or sugestions ' +
                                 'should be directed to\n' +
                                 'http://mosaicode.github.io/\n'))

        labelFinal.set_justify(Gtk.Justification.CENTER)

        finalbox = Gtk.Box()
        finalbox.pack_start(labelFinal, True, True, 0)

        gridFrame.attach_next_to(finalbox, hbox, Gtk.PositionType.BOTTOM, 2, 2)

        frame2.add(gridFrame)

        gridTeste = Gtk.Grid()
        gridTeste.add(frame2)

        # --------------------------------------------------------------------#
        # ------------------------------Placing everything--------------------#

        notebook = Gtk.Notebook()
        notebook.set_border_width(10)

        notebook.page1 = Gtk.Frame()
        notebook.page1.set_border_width(10)
        notebook.page1.add(aboutBox)
        notebook.append_page(notebook.page1, Gtk.Label(_('About')))

        notebook.page2 = Gtk.ScrolledWindow()
        notebook.page2.set_min_content_width(635)
        notebook.page2.add(gridTeste)
        notebook.append_page(notebook.page2, Gtk.Label(_('Developers')))

        notebook.page3 = Gtk.ScrolledWindow()
        notebook.page3.set_min_content_width(635)
        notebook.page3.add(frameLicense)
        notebook.append_page(notebook.page3, Gtk.Label(_('License')))

        grid.attach_next_to(
            notebook, frameBorder, Gtk.PositionType.BOTTOM, 1, 2)
