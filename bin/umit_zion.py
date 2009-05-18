#!/usr/bin/env python
# vim: set encoding=utf-8 :

# Copyright (C) 2009 Adriano Monteiro Marques.
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import sys
import getopt

if not hasattr(sys, 'frozen'):
    _source_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir))
    if os.path.exists(os.path.join(_source_path, 'bin/umit_zion.py')):
        # Assuming zion is being executed from a svn checkout
        sys.path.insert(0, _source_path)

import umit.zion.core.Address as Address
import umit.zion.core.Options as Options
from umit.zion.scan.Probe import get_addr_from_name
from umit.zion.core.Zion import Zion
from umit.zion.core.Host import Host

if __name__ == '__main__':

    zion = Zion(Options.Options(), [])

    options, address = getopt.gnu_getopt(sys.argv[1:], Options.FORMAT)

    for o in options:
        option, value = o
        zion.get_option_object().add_option(option, value)

    for a in address:
        if Address.recognize(a) == Address.Unknown:
            l = get_addr_from_name(a)
            for i in l:
                zion.append_target(Host(i))
        else:
            zion.append_target(Host(a))

    zion.run()