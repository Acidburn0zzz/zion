#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Adriano Monteiro Marques
#
# Author: Joao Paulo de Souza Medeiros <ignotus@umitproject.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import gtk
import gobject

from higwidgets.higboxes import HIGVBox, HIGHBox
from higwidgets.higdialogs import HIGAlertDialog
from higwidgets.higscrollers import HIGScrolledWindow

from umit.core.UmitConf import ProfileNotFound, Profile
from umit.core.Paths import Path
from umit.core.UmitLogging import log
from umit.core.I18N import _

class ZionProfile(HIGVBox):
    """
    """
    def __init__(self, target=None):
        """
        """
        HIGVBox.__init__(self)

        self.target = target
        self.result = ZionResultsPage()

        self.pack_end(self.result)
        self.show_all()

    def update_target(self, target):
        """
        """
        self.target = target

class ZionHostsList(gtk.ScrolledWindow):
    """
    """
    def __init__(self):
        """
        """
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__cell_text = gtk.CellRendererText()
        self.__cell_pixbuf = gtk.CellRendererPixbuf()

        self.__hosts_store = gtk.ListStore(gtk.gdk.Pixbuf,
                                           gobject.TYPE_STRING)

        self.__hosts_treeview = gtk.TreeView(self.__hosts_store)
        self.__hosts_treeview.connect('cursor-changed', self.__cursor_callback)

        self.__hosts_column = list()

        self.__column_type = gtk.TreeViewColumn(_('Type'),
                                                self.__cell_pixbuf,
                                                pixbuf=0)
        self.__column_host = gtk.TreeViewColumn(_('Host'),
                                                self.__cell_text,
                                                text=1)

        fw = gtk.gdk.pixbuf_new_from_file('share/pixmaps/zion/firewall.png')
        sp = gtk.gdk.pixbuf_new_from_file('share/pixmaps/zion/shield.png')
        hp = gtk.gdk.pixbuf_new_from_file('share/pixmaps/zion/honey.png')

        self.__hosts_store.append([fw, 'firewall.example.com'])
        self.__hosts_store.append([sp, 'synproxy.example.com'])
        self.__hosts_store.append([hp, 'honeyd.example.com'])

        self.__column_type.set_reorderable(True)
        self.__column_type.set_resizable(False)
        self.__column_host.set_reorderable(True)
        self.__column_host.set_resizable(False)

        self.__hosts_treeview.append_column(self.__column_type)
        self.__hosts_treeview.append_column(self.__column_host)

        self.__hosts_store.set_sort_func(0, self.__sort_type)
        self.__hosts_store.set_sort_func(1, self.__sort_host)

        self.add(self.__hosts_treeview)

        self.__hosts_treeview.set_cursor((0,))
        self.__cursor_callback(self.__hosts_treeview)

    def __cursor_callback(self, widget):
        """
        """
        path = widget.get_cursor()[0]
        iter = self.__hosts_store.get_iter(path)
        self.__hosts_store.get_value(iter, 0)

    def __sort_type(self, treemodel, iter1, iter2):
        """
        """
        return 0

    def __sort_host(self, treemodel, iter1, iter2):
        """
        """
        return 0

class ZionResultsPage(gtk.HPaned):
    """
    """
    def __init__(self):
        """
        """
        gtk.HPaned.__init__(self)
        self.set_border_width(6)

        self.__create_widgets()
        self.set_position(200)

    def __create_widgets(self):
        """
        """
        self.__list = ZionHostsList()
        self.add1(self.__list)
        self.add2(gtk.Label('Right'))

class ZionProfileHoneyd(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

class ZionProfileOS(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

class ZionProfilePrompt(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

        self.__command_hbox = HIGHBox()
        self.__command_label = gtk.Label(_('Command:'))
        self.__command_entry = gtk.Entry()

        self.__command_hbox._pack_noexpand_nofill(self.__command_label)
        self.__command_hbox._pack_expand_fill(self.__command_entry)

        self._pack_noexpand_nofill(self.__command_hbox)

class ZionProfileSYNProxy(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

PROFILE_CLASS = {'1': ZionProfileHoneyd,
                 '2': ZionProfileOS,
                 '3': ZionProfilePrompt,
                 '4': ZionProfileSYNProxy}

class ZionScanNotebookPage(gtk.Alignment):
    """
    """
    def __init__(self, page):
        """
        """
        gtk.Alignment.__init__(self, 0, 0, 1, 1)

        self.page = page
        self.profile = None

    def profile_changed(self, widget, event=None):
        """
        """
        profile = self.page.toolbar.selected_profile

        if self.profile != profile:
            id = Profile()._get_it(profile, 'zion_id')
            if self.get_child():
                self.remove(self.get_child())

            self.add(PROFILE_CLASS[id]())

            if type(self.get_child()) == ZionProfilePrompt:
                self.page.toolbar.target_entry.set_sensitive(False)
            else:
                self.page.toolbar.target_entry.set_sensitive(True)

            self.show_all()
            self.profile = profile

    def target_changed(self, widget, event=None):
        """
        """
        target = self.page.toolbar.selected_target.strip()
        self.get_child().update_target(target)

    def check_scan(self):
        """
        """
        self.page.toolbar.scan_button.set_sensitive(True)
        self.page.toolbar.scan_button.set_sensitive(False)

    def start_scan_cb(self, widget):
        """
        """
        pass

    def kill_scan(self):
        """
        """
        pass

    def close_tab(self):
        """
        """
        pass

    def erase_references(self):
        """
        """
        pass
