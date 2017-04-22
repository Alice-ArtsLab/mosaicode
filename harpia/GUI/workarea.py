# -*- coding: utf-8 -*-
"""
This module contains the WorkArea class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.dialog import Dialog
import gettext
_ = gettext.gettext


class WorkArea(Gtk.Notebook):
    """
    This class contains methods related the WorkArea class.
    """

    def __init__(self, main_window):
        Gtk.Notebook.__init__(self)
        self.main_window = main_window
        self.set_scrollable(True)
        self.diagrams = []
        self.connect("switch-page", self.__on_switch_page)
        self.connect("page-removed", self.__on_page_removed)

    # ----------------------------------------------------------------------
    def __on_page_removed(self, notebook, child, page_num):
        if self.get_n_pages() == 0:
            self.main_window.set_title("")

    # ----------------------------------------------------------------------
    def __on_switch_page(self, notebook, child, page_num):
        self.main_window.set_title(child.get_children()[0].file_name)

    # ----------------------------------------------------------------------
    def add_diagram(self, diagram):
        """
        This method add a  new diagram page.

            Parameters:
                * **diagram** (:class:`Diagram<harpia.GUI.diagram`)
        """
        frame = Gtk.ScrolledWindow()
        frame.set_shadow_type(Gtk.ShadowType.IN)
        frame.add(diagram)
        name = diagram.patch_name
        diagram.set_scrolled_window(frame)
        index = self.append_page(frame, self.__create_tab_label(name, frame))
        self.show_all()
        self.diagrams.append(diagram)
        self.set_current_page(self.get_n_pages() - 1)

    # ----------------------------------------------------------------------
    def close_tab(self, position=None):
        """
        This method close a tab.

            Parameters:
                * **position**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if position is None:
            position = self.get_current_page()
        tab = self.get_nth_page(position)
        diagram = tab.get_children()[0]

        if diagram.modified:
            dialog = Dialog().confirm_dialog(_("Diagram ") +
                                             diagram.file_name +
                                             _("is not saved.\nIf you close it"
                                               ", changes will be lost.\n"
                                               "Confirm?"), self.main_window)
            result = dialog.run()
            dialog.destroy()
            if result == Gtk.ResponseType.CANCEL:
                return False

        self.remove_page(position)
        self.diagrams.pop(position)
        return True

    # ----------------------------------------------------------------------
    def __create_tab_label(self, text, frame):
        """
        This method create a tab label.
            Parameters:
                * **text** (:class:`str<str>`)
            Returns:
                * **box**
        """
        box = Gtk.HBox()
        button = Gtk.Button()
        image = Gtk.Image().new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        button.set_image(image)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect('clicked', self.__on_close_button_clicked, frame)
        label = Gtk.Label(text)
        box.add(label)
        box.add(button)
        box.show_all()
        return box

    # ----------------------------------------------------------------------
    def __on_close_button_clicked(self, widget, frame):
        index = -1
        for tab in self.get_children():
            index += 1
            if tab == frame:
                break
        self.close_tab(index)

    # ----------------------------------------------------------------------
    def get_current_diagram(self):
        """
        This method get current diagram page.
            Return
                * **Types** (:class:`int<int>`)
        """

        if self.get_current_page() > -1:
            return self.diagrams[self.get_current_page()]
        else:
            return None

    # ----------------------------------------------------------------------
    def get_diagrams(self):
        return self.diagrams

    # ----------------------------------------------------------------------
    def rename_diagram(self, diagram):
        """
        This method rename a diagram page.

            Parameters:
                * **diagram** (:class:`diagram<harpia.GUI.diagram>`)
        """
        index = -1
        for scrolled_window in self.get_children():
            index += 1
            tab = scrolled_window.get_children()[0]
            if tab == diagram:
                break
        tab = self.get_nth_page(index)
        if tab is None:
            return
        hbox = self.get_tab_label(tab)
        label = hbox.get_children()[0]
        name = diagram.patch_name
        if diagram.modified:
            name = "* " + name
        label.set_text(name)
        self.main_window.set_title(diagram.file_name)

    # ----------------------------------------------------------------------
    def resize(self, data):
        """
        This method resize a diagram page.

            Parameters:
                * **data**

        """
        for diagram in self.diagrams:
            diagram.resize(data)

    # ----------------------------------------------------------------------
    def close_tabs(self):
        """
        This method close tabs.

            Returns:
               * **boolean** (:class:`boolean<boolean>`)
        """
        n_pages = self.get_n_pages()
        for i in range(n_pages):
            if not self.close_tab(0):
                return False
        return True
# ----------------------------------------------------------------------
