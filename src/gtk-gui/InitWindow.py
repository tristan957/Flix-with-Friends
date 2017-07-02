import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GObject


class InitWindow(Gtk.ApplicationWindow):
    """Log-in window for accessing the database"""

    __gsignals__ = {
        'cancel': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'credentials-set': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    cred_dict = None

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self, resizable=False, window_position=Gtk.WindowPosition.CENTER)

        self.cred_dict = {}

        self.set_titlebar(Gtk.HeaderBar(title='Enter Credentials', show_close_button=True))

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=10)
        self.add(main_box)

        grid = Gtk.Grid(row_spacing=10, column_spacing=10, margin=10)
        main_box.pack_start(grid, True, True, 0)

        self.location_entry = Gtk.Entry()
        self.user_entry = Gtk.Entry()
        self.pass_entry = Gtk.Entry()

        grid.attach(Gtk.Label(label='Location', halign=Gtk.Align.START), 0, 0, 1, 1)
        grid.attach(self.location_entry, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label='Username', halign=Gtk.Align.START), 0, 1, 1, 1)
        grid.attach(self.user_entry, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label='Password', halign=Gtk.Align.START), 0, 2, 1, 1)
        grid.attach(self.pass_entry, 1, 2, 1, 1)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin_end=10)
        main_box.pack_end(button_box, True, True, 0)

        enter = Gtk.Button(label='Enter')
        enter.connect('clicked', self.enter_cb)
        enter.get_style_context().add_class('suggested-action')

        cancel = Gtk.Button(label='Cancel')
        cancel.connect('clicked', lambda button: self.emit('cancel'))
        cancel.get_style_context().add_class('destructive-action')

        button_box.pack_end(cancel, False, False, 0)
        button_box.pack_end(enter, False, False, 0)

    def enter_cb(self, button):
        self.cred_dict['location'] = self.location_entry.get_text()
        self.cred_dict['username'] = self.user_entry.get_text()
        self.cred_dict['password'] = self.pass_entry.get_text()
        self.emit('credentials-set', self.cred_dict)
