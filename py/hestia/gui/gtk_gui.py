#import hestia.core.plugins.pattern_threaded as threaded
import logging as log
import os
import sys
import time
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import glib
import threading

class GTK_GUI:
    def __init__(self, child, parent, lock):
        self.work = True
        self.child = child
        self.parent_queue = parent
        self.lock = lock
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        #self.window.set_default_size(200, 200)
        
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)
        
        self.button = gtk.Button("Press me!")
        self.button.connect("clicked", self.send_msg, "Button pressed")
        self.box1.pack_start(self.button, True, True, 0)
        self.button.show()
        self.box1.show()
        self.window.show()
        
        #glib.io_add_watch(self.parent_queue._reader.fileno(), glib.IO_IN, self.update)
        
    def MsgBox (self, text, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK_CANCEL) :
        d = gtk.MessageDialog(message_format=text, type=type, buttons=buttons, flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT)
        d.set_property("deletable", False)
        w,h = d.get_size()
        d.move( gtk.gdk.screen_width() // 2 - w // 2, gtk.gdk.screen_height() // 2 - h)
        d.show()
        r = d.run()
        d.destroy()
        return r
    
    def run(self):
        #log.debug(threading.current_thread())
        #log.debug("calling GTK_GUI main")
        while self.work:
            while gtk.events_pending():
                gtk.main_iteration()
        #gtk.main()
        #log.debug("leaving GTK_GUI main")
        #keep_running = True
        #while keep_running:
        #    #gtk.gdk.threads_enter()
        #    while gtk.events_pending():
        #        gtk.main_iteration(block=False)
            #gtk.gdk.threads_leave()
            #if self.child_connection.poll():
            #    msg = self.child_connection.recv()
        #gtk.main()
        ## gtk.main_iteration()
    
    def destroy(self, widget, data=None):
        self.parent_queue.put('quit')
        #gtk.main_quit()
        self.work = False
        
    def update(self, fd, condition):
        msg = self.parent_queue.get()
        log.debug("msg recvd: %s" % msg)
        return True
        
    def hook(self):
        gtk.main_iteration(block=False)

    def send_msg(self, widget, msg=None):
        #self.MsgBox("Button pressed!")
        if msg:
            self.parent_queue.put(msg)
            


        
