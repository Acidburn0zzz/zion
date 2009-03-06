"""
Common values that may be needed by the generic setup, windows setup and the
macosx setup.
"""
import os

BIN_DIRNAME = 'bin'

# These directories are relative to the installation or dist directory
# Ex: python setup.py install --prefix=/tmp/umit
# Will create the directory /tmp/umit with the following directories
PIXMAPS_DIR = os.path.join('share', 'pixmaps', 'umit')
ICONS_DIR = os.path.join('share', 'icons', 'umit')
LOCALE_DIR = os.path.join('share', 'locale')
CONFIG_DIR = os.path.join('share', 'umit', 'config')
DOCS_DIR = os.path.join('share', 'doc', 'umit')
MISC_DIR = os.path.join('share', 'umit', 'misc')
SQL_DIR = os.path.join('share', 'umit', 'sql')