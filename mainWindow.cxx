#include <gtk/gtk.h>
#include <iostream>

static void activate(GtkApplication* app, gpointer user_data)
{
	GtkWidget* mainWindow;
	GtkWidget* header;
	GtkWidget* fileButton;
	GIcon* fileIcon;
	GtkWidget* fileImage;

	mainWindow = gtk_application_window_new(app);
	//gtk_window_set_title(GTK_WINDOW(mainWindow), "Stop Bitchin' - Start Watchin'");
	gtk_window_set_default_size(GTK_WINDOW(mainWindow), 1200, 720);

	header = gtk_header_bar_new();
	gtk_header_bar_set_show_close_button(GTK_HEADER_BAR(header), TRUE);
	gtk_header_bar_set_title(GTK_HEADER_BAR(header), "Stop Bitchin' - Start Watchin'");
	gtk_header_bar_set_has_subtitle(GTK_HEADER_BAR(header), FALSE);
	gtk_window_set_titlebar(GTK_WINDOW(mainWindow), header);

	fileButton = gtk_button_new_with_label("Open a File");
	//g_signal_connect()
	//fileIcon = g_themed_icon_new("mail-send-receive-symbolic");
	//fileImage = gtk_image_new_from_gicon(fileIcon, GTK_ICON_SIZE_BUTTON);
	//gtk_container_add(GTK_CONTAINER(fileButton), fileImage);
	gtk_header_bar_pack_start(GTK_HEADER_BAR(header), fileButton);

	gtk_widget_show_all(mainWindow);
}

int main (int argc, char** argv)
{
  GtkApplication* app;
  int status;

  app = gtk_application_new ("com.github.tristan957.stop_bitchin-start_watchin", G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
  status = g_application_run(G_APPLICATION(app), argc, argv);
  g_object_unref(app);

  return status;
}
