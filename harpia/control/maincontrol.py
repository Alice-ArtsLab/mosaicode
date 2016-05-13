#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MainControl():

    def __init__(self, main_window):
        self.main_window = main_window

    def new(self):
        self.main_window.work_area.add_tab("Untitled")

    def select_open(self):
        self.open("/home/flavio/helloworld.hrp")

    def open(self, file_name):
        self.main_window.work_area.open_diagram(file_name)

    def close(self):
        self.main_window.work_area.close_tab()

    def save(self):
        print "Save from control"

    def save_as(self):
        print "Save As from control"

    def export_diagram(self):
        print "Export from control"

    def exit(self):
        self.main_window.quit(None, None)

    def cut(self):
        print "Cut from control"

    def copy(self):
        print "Copy from control"

    def paste(self):
        print "Paste from control"

    def delete(self):
        print "Delete from control"

    def preferences(self):
        print "Preferences from control"

    def zoom_in(self):
        print "Zoom in from control"

    def zoom_out(self):
        print "Zoom out from control"

    def zoom_normal(self):
        print "Zoom Normal from control"

    def run(self):
        print "Run from control"

    def save_source(self):
        print "Save from control"

    def view_source(self):
        print "View Source from control"

    def tips(self):
        print "Tips from control"

    def about(self):
        print "About from control"

    def search(self, query):
        self.main_window.blocks_tree_view.search(query)

    def show_search_bar(self):
        self.main_window.search.show_search_bar()
        
    def set_help(self, block_name):
#        self.main_window.block_properties.set_help(block_name)
        pass

    def append_status_log(self, text):
        self.main_window.status.append_text(text)
