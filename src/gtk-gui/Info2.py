import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, GdkPixbuf

from Database import Database


class ActionBar(Gtk.ActionBar):
    """Toolbar for displaying mocie actions"""

    def __init__(self, movie):
        Gtk.ActionBar.__init__(self)

        self.get_style_context().add_class("inline-toolbar")

        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                             spacing=10)
        self.title = Gtk.Label(label="<big><b>{}</b></big>".format(movie.title.replace('&', '&amp;')),
                               justify=Gtk.Justification.CENTER,
                               use_markup=True)
        self.rating = Gtk.LevelBar.new_for_interval(0, 10)
        self.rating.set_value(float(movie.vote))
        self.rating.set_size_request(-1, 15)

        center_box.add(self.title)
        center_box.add(self.rating)
        self.set_center_widget(center_box)

        popout = Gtk.Button.new_from_icon_name("view-paged-symbolic", Gtk.IconSize.BUTTON)
        popout.connect("clicked", self._popout_cb)

        menu_image = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        menu = Gtk.MenuButton(image=menu_image)

        # trailer button

        self.pack_start(popout)
        self.pack_end(menu)

    def _popout_cb(self, button):
        pass

    def update(self, movie):
        """Updates the data within"""

        self.title.set_label("<big><b>{}</b></big>".format(movie.title.replace('&', '&amp;')))
        self.rating.set_value(float(movie.vote))


class ImageBox(Gtk.Grid):
    """Box for displaying the poster and the cast"""

    def __init__(self, movie):
        Gtk.Grid.__init__(self, column_spacing=25, row_spacing=25, halign=Gtk.Align.CENTER)

        # don't do this at home folks
        self.poster = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file(movie.get_large_image()))
        self.peep_imgs = [Gtk.Image.new_from_file(peep.img) for peep in movie.cast]

        self.attach(self.peep_imgs[0], 0, 0, 1, 1)
        self.attach(self.peep_imgs[1], 0, 1, 1, 1)
        self.attach(self.poster, 1, 0, 1, 2)
        self.attach(self.peep_imgs[2], 2, 0, 1, 1)
        self.attach(self.peep_imgs[3], 2, 1, 1, 1)

        self.show_all()

    def update(self, movie):
        """Update all the images"""
        self.poster.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file(movie.get_large_image()))
        for index, img in enumerate(self.peep_imgs):
            img.set_from_file(movie.cast[index].img)

        self.show_all()


class InfoPage(Gtk.Box):
    """A single page to display movie information"""

    def __init__(self, movie):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL,
                         spacing=40)

        self.action = ActionBar(movie)
        self.images = ImageBox(movie)

        self.pack_start(self.action, False, True, 0)
        self.pack_start(self.images, True, True, 0)
        # self.add(Gtk.Image.new_from_file(movie.get_large_image()))

    def update(self, movie):
        """Update all UI components"""
        self.action.update(movie)
        self.images.update(movie)

        self.show_all()
