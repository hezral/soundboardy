# main.py
#
# Copyright 2021 adi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Granite, Gdk

from .window import SoundboardyWindow


class Application(Gtk.Application):

    granite_settings = Granite.Settings.get_default()
    gtk_settings = Gtk.Settings.get_default()
    gio_settings = Gio.Settings(schema_id="com.github.hezral.soundboardy")

    main_window = None

    def __init__(self):
        super().__init__(application_id='com.github.hezral.soundboardy',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)
        self.granite_settings.connect("notify::prefers-color-scheme", self.on_prefers_color_scheme)

        provider = Gtk.CssProvider()        
        provider.load_from_path(os.path.join(os.path.dirname(__file__), "data", "application.css"))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.icon_theme = Gtk.IconTheme.get_default()
        self.icon_theme.prepend_search_path(os.path.join(os.path.dirname(__file__), "data", "icons"))

        if "io.elementary.stylesheet" not in self.gtk_settings.props.gtk_theme_name:
            self.gtk_settings.set_property("gtk-theme-name", "io.elementary.stylesheet.blueberry")

    def do_activate(self):
        if not self.main_window:
            self.main_window = SoundboardyWindow(application=self)
        self.main_window.present()

    def on_prefers_color_scheme(self, *args):
        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)


def main(version):
    app = Application()
    return app.run(sys.argv)
