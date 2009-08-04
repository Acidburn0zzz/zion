# -*- coding: utf-8 -*-
# Copyright (C) 2008 Adriano Monteiro Marques
#
# Author: Francesco Piccinno <stack.box@gmail.com>
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import gtk
import os.path

from higwidgets.higwindows import HIGWindow
from higwidgets.higboxes import HIGVBox

from higwidgets.higanimates import HIGAnimatedBar
from higwidgets.higtoolbars import HIGToolBar, HIGToolItem

from PathPage import PathPage
from PluginPage import PluginPage

from umit.core.Paths import Path
from umit.plugin.Update import UpdateEngine
from umit.plugin.Engine import PluginEngine

from Network import *

from umit.core.I18N import _


class PluginWindow(HIGWindow):
    def __init__(self):
        HIGWindow.__init__(self)

        self.engine = PluginEngine()
        self.update_eng = UpdateEngine()

        self.set_title(_('Plugin Manager'))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_size_request(600, 400)
        self.set_icon_from_file(os.path.join(Path.icons_dir, "umit_16.ico"))

        self.__create_widgets()
        self.__pack_widgets()

    def __create_widgets(self):
        self.vbox = HIGVBox()

        self.animated_bar = HIGAnimatedBar('')
        self.toolbar = HIGToolBar()

        self.notebook = gtk.Notebook()
        self.notebook.set_show_tabs(False)
        self.notebook.set_show_border(False)

        self.plug_page = PluginPage(self)
        self.path_page = PathPage(self)

    def __pack_widgets(self):
        self.add(self.vbox)

        self.vbox.pack_start(self.animated_bar, False, False, 0)
        self.vbox.pack_start(self.toolbar, False, False, 0)
        self.vbox.pack_start(self.notebook)

        self.notebook.append_page(self.plug_page)
        self.notebook.append_page(self.path_page)

        self.toolbar.connect('changed', self.__on_switch_page)

        self.connect('realize', self.__on_realize)

        # Create the pages

        lbls = (_('Extensions'), _('Paths'))
        imgs = ('extension_small', 'paths_small')

        for lbl, stock in zip(lbls, imgs):
            image = gtk.image_new_from_stock(stock, gtk.ICON_SIZE_MENU)

            self.toolbar.append(
                HIGToolItem('<b>%s</b>' % lbl, image)
            )

        self.toolbar.set_active(0)
        self.get_child().show_all() # No show the root

        # We have to hide unused buttons in plugin page
        self.plug_page.install_updates_btn.hide()
        self.plug_page.skip_install_btn.hide()
        self.plug_page.restart_btn.hide()

        self.connect('delete-event', self.__on_delete_event)

    def __on_delete_event(self, widget, evt):
        self.hide()
        return True

    def __on_realize(self, widget):
        self.animated_bar.hide()

        self.plug_page.populate()
        self.path_page.populate()

    def __on_switch_page(self, widget, id):
        self.notebook.set_current_page(id)
