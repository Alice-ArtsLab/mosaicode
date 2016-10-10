# -*- coding: utf-8 -*-
import gi
import os
from gi.repository import Gtk
gi.require_version('Gtk', '3.0')


class About(Gtk.Window):

    def __init__(self, main_window):
        self.data_dir = os.environ['HARPIA_DATA_DIR']
        Gtk.Window.__init__(self, title="About Harpia")
        self.set_default_size(650, 480)

        grid = Gtk.Grid()
        self.add(grid)
# -----------------------logo harpia----------------------------------#
        image = Gtk.Image()
        image.set_from_file(self.data_dir + "images/harpia_ave.png")

        frame = Gtk.Frame()
        frame.set_border_width(2)
        frame.add(image)

        frameBorder = Gtk.Frame()
        frameBorder.set_border_width(10)
        frameBorder.add(frame)

        grid.add(frameBorder)
# --------------------------------------------------------------------#
# -------------------------------About Text---------------------------#
        labelAbout = Gtk.Label('Harpia Project was one of the aproved'
                               'projects under CT-INFO 2003 Edital.\n' +
                               'This project intends to build a ' +
                               'graphical environment for learning,\n' +
                               'implementing and management of machine' +
                               ' vision systems.\n\n The system is ' +
                               '(would-be) made of several software ' +
                               'modules for hardware\n comunication,' +
                               ' image (signal) processing and remote management of vision\n' +
                               'systems.\n\n' +
                               'The system could be used in industries or acadamics, making easier to \n' +
                               'develop quality control systems, and vision system based process,\n' +
                               'helping the learning and spreading of vision systems.')
        aboutBox = Gtk.Box()
        aboutBox.add(labelAbout)
        aboutBox.set_border_width(35)
# --------------------------------------------------------------------#
# ----------------------------License Text----------------------------#
        labelLicense = Gtk.Label('Harpia\n' +
                                 'Copyright (C) 2007 S2i-das-ufsc\n\n' +
                                 'This program is free software: you can redistribute it and/or modify\n' +
                                 'it under the terms of the GNU General Public License as published by\n' +
                                 'the Free Software Foundation, either version 3 of the License, or\n' +
                                 '(at your option) any later version.\n\n' +
                                 'This program is distributed in the hope that it will be useful,\n' +
                                 'but WITHOUT ANY WARRANTY; without even the implied warranty of\n' +
                                 'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n' +
                                 'GNU General Public License for more details.\n\n' +
                                 'You should have received a copy of the GNU General Public License\n' +
                                 'along with this program.  If not, see www.gnu.org/licenses.\n\n' +
                                 'This Program uses the Amara software,\n' +
                                 'Copyright 2006 Uche Ogbuji\n' +
                                 '(http://uche.ogbuji.net), more information\n' +
                                 'found in the copyright archive \n' +
                                 'provided with this software.')

        labelLicense.set_justify(Gtk.Justification.CENTER)

        frameLicense = Gtk.Frame()
        frameLicense.set_border_width(10)
        frameLicense.add(labelLicense)
# --------------------------------------------------------------------#
# -----------------------------Development part-----------------------#
        imageSponsors1 = Gtk.Image()
        imageSponsors1.set_from_file(self.data_dir + "images/finep_logo.gif")

        imgbox = Gtk.Box()
        imgbox.set_spacing(10)
        imgbox.set_border_width(2)

        textbox = Gtk.Box()
        textbox.set_spacing(10)
        textbox.set_border_width(2)

        imgbox2 = Gtk.Box()
        imgbox2.set_spacing(65)
        imgbox2.set_border_width(2)

        labelFinep = Gtk.Label('FINEP\n Financiadora de estudos e' +
                               'Pesquisas\n http://www.finep.gov.br/')

        labelFinep.set_justify(Gtk.Justification.CENTER)

        imgbox.add(imageSponsors1)

        textbox.add(labelFinep)

        spaceBox = Gtk.Box()
        spaceBox2 = Gtk.Box()

        sponsorsBox = Gtk.Box()
        sponsorsBox.set_spacing(65)
        sponsorsBox.add(spaceBox)
        sponsorsBox.add(imgbox)
        sponsorsBox.add(textbox)

        labelSponsors = Gtk.Label("Sponsors")
        labelSponsors.set_markup("<b>Sponsors</b>")

        frame2 = Gtk.Frame()
        frame2.set_label_widget(labelSponsors)
        frame2.set_border_width(10)
        frame2.add(sponsorsBox)

        labelDevelopment = Gtk.Label("Development")
        labelDevelopment.set_markup("<b>Development</b>")

        imageDevelopment = Gtk.Image()
        imageDevelopment.set_from_file(self.data_dir + "images/s2ilogo.png")

        labelDevelopmentText = Gtk.Label('Sistemas Industriais Inteligentes\n' +
                                         'Departamento de Automação e Sistemas\n' +
                                         'Universidade Federal de Santa Catarina\n' +
                                         'http://s2i.das.ufsc.br/')
        labelDevelopmentText.set_justify(Gtk.Justification.CENTER)

        textBox2 = Gtk.Box()
        textBox2.set_border_width(2)

        imgbox2.add(imageDevelopment)
        textBox2.add(labelDevelopmentText)

        developmentBox = Gtk.Box()
        developmentBox.set_spacing(65)
        developmentBox.add(spaceBox2)
        developmentBox.add(imgbox2)
        developmentBox.add(textBox2)

        frame3 = Gtk.Frame()
        frame3.set_label_widget(labelDevelopment)
        frame3.set_border_width(10)

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

        labelNames = Gtk.Label('Alberto Xavier Pavim\n\nChristian Emanuel Silvano\n\n' +
                               'Clovis Peruchi Scotti\n\nFábio Pedrotti Terra\n\n' +
                               'Fabrício Luchesi Forgerini\n\nFernando Deschamps\n\n' +
                               'Guilherme Augusto Rutzen\n\nLuís Carlos Dill Junges\n\n' +
                               'Marcelo Ricardo Stemmer\n\nMário Lúcio Roloff\n\n' +
                               'Mathias José Kreutz Erdtmann\n\n' +
                               'José Luiz Bittencourt\n\nRicardo Grützmacher')

        vbox_left.pack_start(labelNames, True, True, 0)

        labelJobs = Gtk.Label('Tutor\n\nDeveloper\n\nPresent Developer\n\n' +
                              'Developer\n\nTutor\n\nTutor\n\nDeveloper\n\n' +
                              'Developer\n\nCoordinator\n\nTutor\n\nDeveloper\n\n' +
                              'Developer\n\nDeveloper')

        vbox_center.pack_start(labelJobs, True, True, 0)

        labelEMAILS = Gtk.Label('axpavim@gmail.com\n\nsilvano@das.ufsc.br\n\n' +
                                'scotti@ieee.org\n\nfpterra@yahoo.com.br\n\n' +
                                'fabricio_forgerini@hotmail.com\n\nfernando' +
                                '.deschamps@terra.com.br\n\nrutzen@das.ufsc.br\n\n' +
                                'lcdjunges@yahoo.com.br\n\nmarcelo@das.ufsc.br\n\n' +
                                'roloff@cefetsc.edu.br\n\nerdtmann@das.ufsc.br\n\n' +
                                'jlbitt@yahoo.com\n\ngrutz@terra.com.br')

        vbox_right.pack_start(labelEMAILS, True, True, 0)

        gridFrame3 = Gtk.Grid()
        gridFrame3.add(developmentBox)

        x = Gtk.Separator()
        y = Gtk.Separator()

        gridFrame3.attach_next_to(
            x, developmentBox, Gtk.PositionType.BOTTOM, 1, 2)
        gridFrame3.attach_next_to(hbox, x, Gtk.PositionType.BOTTOM, 1, 2)
        gridFrame3.attach_next_to(y, hbox, Gtk.PositionType.BOTTOM, 1, 2)

        labelFinal = Gtk.Label('Any bugs or sugestions\n' +
                               'should be directed to\n' +
                               'scotti@ieee.org')

        labelFinal.set_justify(Gtk.Justification.CENTER)

        finalbox = Gtk.Box()
        finalbox.pack_start(labelFinal, True, True, 0)

        gridFrame3.attach_next_to(finalbox, y, Gtk.PositionType.BOTTOM, 1, 2)

        frame3.add(gridFrame3)

        gridTeste = Gtk.Grid()
        gridTeste.add(frame2)
        gridTeste.attach_next_to(frame3, frame2, Gtk.PositionType.BOTTOM, 1, 2)
# --------------------------------------------------------------------#
# ------------------------------Placing everything--------------------#
        notebook = Gtk.Notebook()
        notebook.set_border_width(10)

        notebook.page1 = Gtk.Frame()
        notebook.page1.set_border_width(10)
        notebook.page1.add(aboutBox)
        notebook.append_page(notebook.page1, Gtk.Label('About'))

        notebook.page2 = Gtk.ScrolledWindow()
        notebook.page2.set_min_content_width(635)
        notebook.page2.add(gridTeste)
        notebook.append_page(notebook.page2, Gtk.Label('Developers'))

        notebook.page3 = Gtk.ScrolledWindow()
        notebook.page3.set_min_content_width(635)
        notebook.page3.add(frameLicense)
        notebook.append_page(notebook.page3, Gtk.Label('License'))

        grid.attach_next_to(
            notebook, frameBorder, Gtk.PositionType.BOTTOM, 1, 2)
