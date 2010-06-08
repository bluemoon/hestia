#!/usr/bin/python
import pygtk
import signal
import logging as log
from circuits.core import Component
from circuits.core.handlers import handler
from circuits.drivers._inotify import *
from hestia.core.common_events import *

pygtk.require('2.0')

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

 
class gtk_status_icon(Component):
    channel = "inotify"
    def __tick__(self):
        while gtk.events_pending():
            gtk.main_iteration_do(block=True)
 
    def __init__(self, settings=None):
        super(gtk_status_icon, self).__init__(channel=self.channel)
        self.directory = settings.config.project.monitor_directory
        #print self.settings.config
        
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
        self.statusIcon.set_tooltip("Monitoring (%s)" % self.directory)

        self.log = log.getLogger('')
        
    @handler("return_code")
    def on_returncode(self, *args):
        time = args[0]
        command_name = args[1]
        status = (args[2][0]._value == args[2][1]._value)
        self.log.debug(status)
        
        if PYNOTIFY and not status:
            self.push(Notification("Command status", "'%s' command run time: %fs" % (command_name[0], time), self.bad_icon_path))
                 
        self.statusIcon.set_tooltip("build time %fs" % time)
        
        if not status:  
            self.set_icon(self.bad_icon_path)  
        else:  
            self.set_icon(self.good_icon_path) 
               
        return True   
    
    def quit_cb(self, *args):
        #signal.signal(signal.SIGALRM, handler)

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
    
 
 
 
