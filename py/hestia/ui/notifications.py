from circuits.core import Component
import pynotify
import gtk

class notifications(Component):
    def Notification(self, title, text, image):
        n = pynotify.Notification(title, text)
        if image:
            n.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file(image))
        
        n.show()
         
        
 
