#!/usr/bin/python
from subprocess  import PIPE, Popen, call
from hestia import *
from circuits.core import Event, Component, Manager
from circuits.core.handlers import handler
from circuits.drivers._inotify import *
import circuits.tools as tools

import pygtk
pygtk.require('2.0')

import gc
import gobject
import os
import sys
import time
import dbus

import logging

try:
    import gtk
    gtk.gdk.threads_init()
except:
    pass

try:
    import pynotify
    pynotify.init("Hestia")
    PYNOTIFY = True 
except:
    PYNOTIFY = False

 
class GtkStatusIcon(Component):
    channel = "inotify"
    def __tick__(self):
        while gtk.events_pending():
            gtk.main_iteration_do(block=True)

    def __init__(self, directory):
        super(GtkStatusIcon, self).__init__(channel=self.channel)

        self.good_icon_path = '/usr/local/share/icons/hestia/24-em-check.png'#"/usr/local/share/notifier/icons/24-em-check.png"
        self.bad_icon_path  = '/usr/local/share/icons/hestia/24-em-cross.png'#"/usr/local/share/notifier/icons/24-em-cross.png"
        
        #self.timeout_source = gobject.timeout_add(self.timeout, self.timeout_callback)
        self.statusIcon = gtk.StatusIcon()
        
        self.menu = gtk.Menu()
        #self.item = gtk.CheckMenuItem('  Compile?')
        #self.item.connect('activate', self.execute_cb, self.item)
        #self.item.set_active(True)
        #self.menu.append(self.item)
        
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_EXECUTE)
        self.menuItem.connect('activate', self.execute_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.last_build_time = "0"        
        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_from_file(self.good_icon_path)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Monitoring (%s)" % directory)

    @handler("returncode")
    def on_returncode(self, *args):
        status = args[0]
        time = args[1]
        
        #logging.debug(args)
        if PYNOTIFY and status != 0:
            if pynotify.init("Hestia"):
                n = pynotify.Notification("Build status", "build time: %fs" % (time))
                n.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self.bad_icon_path))
                                    
                n.set_timeout(1)
                #n.set_urgency(pynotify.URGENCY_NORMAL)
                #n.set_timeout(pynotify.EXPIRES_NEVER)
                n.show()
        self.statusIcon.set_tooltip("build time %fs" % time)
        if int(status) != 0:
            self.set_icon(self.bad_icon_path)
        else:
            self.set_icon(self.good_icon_path)
            
        return True
    
    def quit_cb(self, *args):
        print args
        self.stop()
        
    def execute_cb(self, widget, event, data = None):
        self.push(Modified('','', '', '', False ))
        
    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)
        
    def set_icon(self, path):
        self.statusIcon.set_from_file(path)
    

#global options

DEFAULT_CMD = "nosetests"
APP_NAME = "Notifier"





#parser = OptionParser()
#parser.add_option("--directory",    action="store",  dest="directory", default=os.getcwd())
#parser.add_option("--cmd",    action="store",  dest="cmd", default=DEFAULT_CMD)
#parser.add_option("--applet", action="store_true", dest="applet", default=False)
#parser.add_option("--applet_debug", action="store_true", dest="applet_debug", default=False)
#options, args = parser.parse_args()

"""
class Monitoring(ProcessEvent):
    def my_init(self, options=None):
        self.cmd    = options.cmd
        self.applet = options.applet            
            
    def process_IN_MODIFY(self, event):
        # We have explicitely registered for this kind of event.
        filename = event.name.split('.')
        file_ext = filename[-1]

        if file_ext == 'rst' or file_ext == 'py': 
            retVal = Popen(self.cmd, shell=True, stderr=PIPE, stdout=PIPE)
            retVal.wait()

            if retVal.returncode != 0:
                notice = retVal.communicate()
                if PYNOTIFY:
                    n = pynotify.Notification("Failure!", notice)
                    n.show()
                    
                f_handle = file('notify.log', 'a')
                f_handle.write(repr(notice) + '\n')
                f_handle.flush()
                f_handle.close()
                        
                
            
            f_handle = file('applet-notify.log', 'a')
            f_handle.write(repr(retVal.returncode) + '\n')
            f_handle.flush()
            f_handle.close()
            self.last_call = time.time()


    def process_default(self, event):
        print 'default: ', event.maskname


class MonitorTray:
    def __init__(self, directory):
        self.timeout = 5000
        self.good_icon_path = "/usr/local/share/notifier/icons/24-em-check.png"
        self.bad_icon_path  = "/usr/local/share/notifier/icons/24-em-cross.png"
        self.directory = directory

        self.timeout_source = gobject.timeout_add(self.timeout, self.timeout_callback)
        self.create_applet()
        
    def create_applet(self):
        self.statusIcon = gtk.StatusIcon()
        self.create_icon()
        
        self.menu = gtk.Menu()
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_EXECUTE)
        self.menuItem.connect('activate', self.execute_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)
        
        gtk.main()


    def timeout_callback(self):
        try:
            f_handle = open('applet-notify.log', 'r')
            return_values = f_handle.readlines()
            last = return_values[-1]
            
            if int(last) != 0:
                self.set_icon(self.bad_icon_path)
            else:
                self.set_icon(self.good_icon_path)
        except Exception, E:
            pass
            
        return 1

            
    def create_icon(self):
        self.statusIcon.set_from_file("/usr/local/share/notifier/icons/24-em-check.png")
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Monitoring (%s)" % self.directory)

    def set_icon(self, path):
        self.statusIcon.set_from_file(path)
        
    def execute_cb(self, widget, event, data = None):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        
        button = gtk.Button("Hello World")
        button.connect_object("clicked", gtk.Widget.destroy, window)
        
        window.add(button)
        button.show()
        window.show()

    def quit_cb(self, widget, data = None):
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
            if button == 3:
                if data:
                    data.show_all()
                    data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)


class main:
    def main(self):
        if options.applet:
            print "Running Gnome applet."
            MonitorTray(options.directory)

        print '==> monitoring %s (type ^c to exit)' % options.directory
        handler = Monitoring(options=options)
        wm = WatchManager()
        notifier = Notifier(wm, default_proc_fun=handler)
        wm.add_watch(options.directory, IN_MODIFY, rec=True)
        notifier.loop()


"""
