import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GObject


class InitWindow2(Gtk.ApplicationWindow):
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
        cancel.connect('clicked', self.cancel_cb)
        cancel.get_style_context().add_class('destructive-action')

        button_box.pack_end(cancel, False, False, 0)
        button_box.pack_end(enter, False, False, 0)

    def enter_cb(self, button):
        self.cred_dict['location'] = self.location_entry.get_text()
        self.cred_dict['username'] = self.user_entry.get_text()
        self.cred_dict['password'] = self.pass_entry.get_text()
        self.emit('credentials-set', self.cred_dict)

    def cancel_cb(self, button):
        self.emit('cancel')


class LogIn(Gtk.Box):
    """Widget to grab initial log in information for the database"""

    __gsignals__ = {
        'credentials-set': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, margin=40,
                         spacing=30, halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)

        self.cred_dict = {}

        header = Gtk.Label(label='<big><b>Enter the following information to begin</b></big>',
                           use_markup=True)
        self.check = Gtk.CheckButton(label='Click to enter a username and password if needed')
        self.check.connect('toggled', self.check_cb)

        locBox = Gtk.Box()
        locBox.get_style_context().add_class('linked')
        self.locBut = Gtk.Button(label='Enter')
        self.locBut.connect('clicked', self.grabLoc_cb)
        self.location = Gtk.Entry()
        self.location.connect('activate', self.grabLoc_cb)
        locBox.pack_start(self.location, True, True, 0)
        locBox.pack_end(self.locBut, False, True, 0)

        self.rev = Gtk.Revealer(transition_duration=300, transition_type=Gtk.RevealerTransitionType.CROSSFADE)
        revBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)

        userBox = Gtk.Box()
        userBox.get_style_context().add_class('linked')
        self.userBut = Gtk.Button(label='Enter')
        self.userBut.connect('clicked', self.grabUser_cb)
        self.userName = Gtk.Entry()
        self.userName.connect('activate', self.grabUser_cb)
        userBox.pack_start(self.userName, True, True, 0)
        userBox.pack_end(self.userBut, False, True, 0)

        passBox = Gtk.Box()
        passBox.get_style_context().add_class('linked')
        self.passBut = Gtk.Button(label='Enter')
        self.passBut.connect('clicked', self.grabPass_cb)
        self.password = Gtk.Entry(invisible_char_set=True)
        self.password.connect('activate', self.grabPass_cb)
        passBox.pack_start(self.password, True, True, 0)
        passBox.pack_end(self.passBut, False, True, 0)

        revBox.add(Gtk.Label(label='Enter a username', halign=Gtk.Align.START))
        revBox.add(userBox)
        revBox.add(Gtk.Label(label='Enter a password', halign=Gtk.Align.START))
        revBox.add(passBox)

        self.rev.add(revBox)

        self.pack_start(header, False, True, 0)
        self.pack_start(self.check, False, True, 0)
        self.pack_start(Gtk.Label(label='Enter a location for the database',
                                  halign=Gtk.Align.START), False, True, 0)
        self.pack_start(locBox, False, True, 0)
        self.pack_start(self.rev, False, True, 0)

    def check_cb(self, button):
        self.rev.set_reveal_child(button.get_active())

    def checkLength(self):
        """Check if all the credentials have been set"""

        if len(self.cred_dict) == 3 or (self.check.get_active() is False and len(self.cred_dict) == 1):
            self.emit('credentials-set', self.cred_dict)

    def grabLoc_cb(self, widget):
        """Grab the location of the server"""

        self.locBut.set_sensitive(False)
        self.location.set_sensitive(False)

        self.cred_dict['location'] = self.location.get_text()
        self.checkLength()

    def grabUser_cb(self, widget):
        """Grab the location of the server"""

        self.userBut.set_sensitive(False)
        self.userName.set_sensitive(False)

        self.cred_dict['username'] = self.userName.get_text()
        self.checkLength()

    def grabPass_cb(self, widget):
        """Grab the location of the server"""

        self.passBut.set_sensitive(False)
        self.password.set_sensitive(False)

        self.cred_dict['password'] = self.password.get_text()
        self.checkLength()


class InitWindow(Gtk.ApplicationWindow):
    """Gets the initial location information"""

    __gsignals__ = {
        "credentials-set": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self):
        Gtk.Window.__init__(self)

        header = Gtk.HeaderBar(title="Flix with Friends", show_close_button=True)
        self.set_titlebar(header)

        cred = LogIn()
        cred.connect("credentials-set", self.cred_cb)

        self.add(cred)

    def cred_cb(self, stack, cred_dict):
        self.emit("credentials-set", cred_dict)
