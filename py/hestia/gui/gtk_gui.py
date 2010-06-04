import hestia.core.plugins.pattern_threaded as threaded
import os
import sys
import time
#import pygtk
#pygtk.require('2.0')
import gtk
#import gobject
#import glib

#gobject.threads_init()

#glib.threads_init()
#

class GTK_GUI(threaded.threading_pattern):
    def destroy(self, widget, data=None):
        self.parent_queue.put('quit')
        gtk.main_quit()
        
    def __init__(self, child=None, parent=None):
        gtk.gdk.threads_init()

        self.parent_queue = parent
        
        threaded.threading_pattern.__init__(self, child=child, parent=parent)
        
        self.window = gtk.Window()
        self.window.set_default_size(200, 200)
        self.window.connect("destroy", self.destroy)

        self.label = gtk.Label("Hello World!")
        self.window.add(self.label)
        
        self.label.show()
        self.window.show()
        gtk.main()
        
        
