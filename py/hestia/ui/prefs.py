import pygtk
pygtk.require('2.0')
import gtk

class PreferencesMgr(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self, 'Preferences', None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_OK,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.current_frame = None
        self.create_gui()

    def create_gui(self):
        model = gtk.ListStore(str, gtk.gdk.Pixbuf)
        pixbuf = gtk.gdk.pixbuf_new_from_file('images/prefs_general.png')        
        model.append(['General', pixbuf])
        pixbuf = gtk.gdk.pixbuf_new_from_file('images/prefs_security.png')
        model.append(['Security', pixbuf])

        self.icon_view = gtk.IconView(model)
        self.icon_view.set_text_column(0)
        self.icon_view.set_pixbuf_column(1)
        self.icon_view.set_orientation(gtk.ORIENTATION_VERTICAL)
        self.icon_view.set_selection_mode(gtk.SELECTION_SINGLE)
        self.icon_view.connect('selection-changed', self.on_select, model)
        self.icon_view.set_columns(1)
        self.icon_view.set_item_width(-1)
        self.icon_view.set_size_request(72, -1)
        
        self.content_box = gtk.HBox(False)
        self.content_box.pack_start(self.icon_view, fill=True, expand=False)
        self.icon_view.select_path((0,)) # select a category, will create frame
        self.show_all()
        self.vbox.pack_start(self.content_box)        
        self.resize(640, 480)
        self.show_all()

    def on_select(self, icon_view, model=None):
        selected = icon_view.get_selected_items()
        if len(selected) == 0: return
        i = selected[0][0]
        category = model[i][0]
        if self.current_frame is not None:
            self.content_box.remove(self.current_frame)
            self.current_frame.destroy()
            self.current_frame = None
        if category == 'General':
            self.current_frame = self.create_general_frame()
        elif category == 'Security':
            self.current_frame = self.create_security_frame()    
        self.content_box.pack_end(self.current_frame, fill=True, expand=True)
        self.show_all()

    def create_general_frame(self):
        frame = gtk.Frame('General')        
        return frame        

    def create_security_frame(self):
        frame = gtk.Frame('Security')        
        return frame        

if __name__ == '__main__':
    p = PreferencesMgr()
    p.run()
    p.destroy()
