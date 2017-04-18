# Copyright 2009 Simon Schampijer
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""HelloWorld Activity: A case study for developing an activity."""
from gi.repository import GObject
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from shutil import copyfile
import os
import pygame
from pygame.locals import *


class GMapCatcher(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""
    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        # Uso un widget principal para los problemas de resolucion x2..
        self.widget_principal = Gtk.EventBox()
        self.crear_menu()
        self.scroll.add(self.widget_principal)
        self.maximize()
       # self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        self.widget_principal.modify_bg(
            Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        self.set_canvas(self.scroll)
        self.scroll.show_all()

    def crear_menu(self):
        self.menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        Logos = Gtk.Image()

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            'images/map.png', 500, 600)
        Logos.set_from_pixbuf(pixbuf)
        Run = Gtk.Button('Run GMapCatcher')
        Run.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        About = Gtk.Button('About GMapCatcher')
        About.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        Credits = Gtk.Button('Credits')
        Credits.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        self.menu.add(Logos)
        self.menu.add(Run)
        self.menu.add(About)
        self.menu.add(Credits)


        # Diseno
        self.menu.pack_start(Run, True, True, 10)
        self.menu.pack_start(About, False, False, 5)
        self.menu.pack_start(Credits, False, False, 5)
        About.connect('clicked', self.introduction)
        Run.connect('clicked',self.run_map)
        Credits.connect('clicked', self.credit)
        self.menu.show_all()
        self.widget_principal.add(self.menu)
        self.widget_principal.show_all()

    def limpiar_ventana(self):
        for widget in self.widget_principal.get_children():
            self.widget_principal.remove(widget)

    def entrar_a_menu(self, widget=None):
        if not self.menu:
            self.crear_menu()

        self.limpiar_ventana()
        self.widget_principal.add(self.menu)
        self.widget_principal.show_all()

    def introduction(self, entrar_a_menu):
        self.limpiar_ventana()

        introduction = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        titulo = Gtk.Label('How to use GMapCatcher')
        titulo.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        info = Gtk.TextView()
        info.set_wrap_mode(Gtk.WrapMode.WORD)
        info.set_editable(False)

        textbuffer = info.get_buffer()
        textbuffer.set_text("\nOverview\n"

"\nGMapCatcher is an offline maps viewer. It can display maps from many providers such as:\n"

"\nCloudMade, OpenStreetMap, Yahoo Maps, Bing Maps, Nokia Maps.\n"

"\nIt displays them using a custom GUI. User can view the maps while offline. GMapCatcher doesn't depend on the map's JavaScript.\n"

"\nGMapCatcher is written in Python 2.7 & PyGTK, can run on Linux, Windows and Mac OSX.\n"

"\nUsage\n"


"\nmaps.py is a gui program used to browse google map. With the offline toggle button unchecked, it can download google map tiles automatically.\n"
"\nOnce the file downloaded, it will reside on user's hard disk and needn't to be downloaded again any more.\n"
"\nAt release 0.02, it use multi-threaded downloader and can be faster.\n"

"\nAfter version 0.04, user can force GMapCatcher to re-download old map tiles by checking 'Force update'.\n"
"\nIf a tile is older than 24 hours, it will be re-downloaded.\n"

"\n download.py is a downloader tools that can be used to download map tiles without gui. maps can use files it downloaded without configuration.\n"

"\nBelow is an example using download.py:\n"

"\n$ download.py --location='Paris, France' --max-zoom=16 --min-zoom=0 --latrange=2.0 --lngrange=2.0\n"
 )

        quit = Gtk.Button('Exit')
        quit.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))


        quit.connect('clicked', self.entrar_a_menu)

        introduction.pack_start(titulo, False, False, 0)
        introduction.pack_start(info, True, True, 10)
        introduction.pack_start(quit, False, False, 10)

        self.widget_principal.add(introduction)
        self.show_all()

    def credit(self, Help):
        self.limpiar_ventana()

        helping = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        infor = Gtk.TextView()
        infor.set_wrap_mode(Gtk.WrapMode.WORD)
        infor.set_editable(False)

        textbuffer = infor.get_buffer()
        textbuffer.set_text("\nAbout GMapCather\n"
        	"\nAuthors:\n"

"\npi3orama@gmail.com, HelderSepu@gmail.com\n"
"\nSugar version for Pablo Ortega salomonpabloortega@gmail.com\n"
"\nFor more information https://github.com/heldersepu/GMapCatcher\n")

        quiti = Gtk.Button('Exit')
        quiti.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        Help.connect('clicked', self.credit)

        quiti.connect('clicked', self.entrar_a_menu)


        helping.pack_start(infor, True, True, 10)
        helping.pack_start(quiti, False, False, 10)

        self.widget_principal.add(helping)
        self.widget_principal.show_all()

    def run_map(self,os):
    	import os

        os.system("python maps.py")