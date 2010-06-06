import hestia.core.plugins.pattern_threaded as threaded
import os
import sys
import time
import pygtk
pygtk.require('2.0')
import gtk
#import gobject
import glib

#gobject.threads_init()

#glib.threads_init()
#


class GTK_GUI(threaded.threading_pattern):
    def destroy(self, widget, data=None):
        self.parent_queue.put('quit')
        #gtk.main_quit()
        
    def update(self, fd, condition):
        pass
        
    def __init__(self, child=None, parent=None):
        print child, parent
        threaded.threading_pattern.__init__(self, child=child, parent=parent)
        self.parent_queue = parent
        gtk.gdk.threads_init()

        
    def main(self):        
        #gtk.threads_init()
        #gobject.threads_init()
        #threaded.threading_pattern.__init__(self, child=child, parent=parent)
        glib.io_add_watch(self.parent_queue._reader.fileno(), glib.IO_IN, self.update)
        
        self.window = gtk.Window()
        self.window.set_default_size(200, 200)

        self.label = gtk.Label("Hello World!")
        self.window.add(self.label)
        
        self.label.show()
        self.window.show_all()
        self.window.connect("destroy", lambda _: gtk.main_quit())
        
        #gtk.main()
    #def run(self, lock, child_connection, parent_queue):
    #    self.child_connection = child_connection
    #    self.lock = lock
    #    self.parent_queue = parent_queue
    #    
    #    keep_running = True
    #    while keep_running:
    #        print "Hi"
            #gtk.gdk.threads_enter()
            #while gtk.events_pending():
    #        gtk.main_iteration(block=True)
            #gtk.gdk.threads_leave()
            #if self.child_connection.poll():
            #    msg = self.child_connection.recv()
        #gtk.main()
        ## gtk.main_iteration()
    
