import sys
sys.path.append("/home/cloud/projects/bin/nemo-gitannex/")
import hashlib
import urllib
import gitannex_utils as utils

from gi.repository import Nemo, Gtk, GObject

class GitAnnexPropertyPage(GObject.GObject, Nemo.PropertyPageProvider):
    def __init__(self):
        pass
    
    def get_property_pages(self, files):
        if len(files) != 1:
            return
        
        file = files[0]
        if file.get_uri_scheme() != 'file':
            return

        if file.is_directory():
            return

        filename = urllib.unquote(file.get_uri()[7:])
        self.property_label = Gtk.Label('git-annex')
        self.property_label.show()

        locations = utils.getLocations(filename)

        self.vbox = Gtk.VBox()
        self.vbox.show()
        copies = Gtk.Label("copies: "+str(len(locations)))
        copies.show()

        self.vbox.pack_start(copies, False, False, 0)
        self.hbox = Gtk.HBox(homogeneous=False, spacing=5)
        self.hbox.show()
        label = Gtk.Label('Locations: ')
        label.show()
        self.hbox.pack_start(label, False, False, 0)
        text = ""
        for loc in locations:
          text += loc+"\n"
        value_label = Gtk.Label()
        value_label.set_text(text);
        value_label.show()
        self.hbox.pack_start(value_label, False, False, 0)

        self.vbox.pack_start(self.hbox, False, False, 0)

        return Nemo.PropertyPage(name="NemoPython::gitannex",
                                     label=self.property_label, 
                                     page=self.vbox),
