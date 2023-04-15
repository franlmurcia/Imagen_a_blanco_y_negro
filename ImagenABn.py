import sys
import os
import shutil
from PIL import Image
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib




UI_FILE = "ImagenABn.glade"


class GUI:
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)

        self.builder.connect_signals(self)
        window = self.builder.get_object('window1')

        window.show_all()


    def on_window1_destroy(self, window):
        os.system('rm ~~*.*')
        Gtk.main_quit()

    def on_window1_show(self, window):
        self.Veces = 0
        self.Veces2 = 0
        boton2 = self.builder.get_object('button2')
        boton2.set_sensitive(False)

    def on_button1_clicked(self, button):
        dialogo = self.builder.get_object('filechooser1')

        if (self.Veces == 0):
            dialogo.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        response = dialogo.run()

        if response == Gtk.ResponseType.OK:
            
            self.directorio = dialogo.get_filename()
            contenido = os.listdir(self.directorio)
            imagenes = []
            for fichero in contenido:
                if os.path.isfile(os.path.join(self.directorio, fichero)) and fichero.endswith('.jpg'):
                    imagenes.append(fichero)
                if os.path.isfile(os.path.join(self.directorio, fichero)) and fichero.endswith('.jpeg'):
                    imagenes.append(fichero)
                if os.path.isfile(os.path.join(self.directorio, fichero)) and fichero.endswith('.png'):
                    imagenes.append(fichero)
                if os.path.isfile(os.path.join(self.directorio, fichero)) and fichero.endswith('.tiff'):
                    imagenes.append(fichero)
                if os.path.isfile(os.path.join(self.directorio, fichero)) and fichero.endswith('.tga'):
                    imagenes.append(fichero)
                if os.path.isfile(os.path.join(self.directorio, fichero)) and fichero.endswith('.gif'):
                    imagenes.append(fichero)

            iconview = self.builder.get_object('iconview1')
            liststore = self.builder.get_object('liststore1')

            iconview.set_model(liststore)
            iconview.set_text_column(1)
            iconview.set_pixbuf_column(0)

            liststore.clear()

            for icon in imagenes:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(self.directorio +'/'+ icon, 128, 128)
                liststore.append([pixbuf,icon])
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialogo.hide()
        self.Veces += 1

    def on_button2_clicked(self, button):
        dialogo2 = self.builder.get_object('filechooser2')

        if (self.Veces2 == 0):
            dialogo2.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        dialogo2.set_current_name("BN" + self.nombre_archivo)
        response = dialogo2.run()

        if response == Gtk.ResponseType.OK:
            shutil.copy2("~~" + self.nombre_archivo, dialogo2.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialogo2.hide()
        self.Veces2 += 1
            

    def on_iconview1_selection_changed(self, iconview):
        try:
            path = iconview.get_selected_items()
            liststore = self.builder.get_object('liststore1')
            treeiter = liststore.get_iter(path)
            self.nombre_archivo = liststore.get_value(treeiter, 1)
            image = Image.open(self.directorio + '/' + self.nombre_archivo)
            grayscale_image = image.convert('L')
            grayscale_image.save('~~' + self.nombre_archivo)
            imagenBN = self.builder.get_object('imageBN')
            pix = GdkPixbuf.Pixbuf.new_from_file_at_size('~~' + self.nombre_archivo, 256, 256)
            imagenBN.set_from_pixbuf(pix)

            boton2 = self.builder.get_object('button2')
            boton2.set_sensitive(True)
        except:
            pass
        

def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
