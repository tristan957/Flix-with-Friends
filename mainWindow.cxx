#include <gtk/gtk.h>
#include <iostream>

static void create_file_chooser_dialog(GtkWidget* fileButton, gpointer mainWindow)
{
	GtkWidget* fileDialog;
	fileDialog = gtk_file_chooser_dialog_new("Open File", GTK_WINDOW(mainWindow), GTK_FILE_CHOOSER_ACTION_OPEN, ("Cancel"), GTK_RESPONSE_CANCEL, ("Open"), GTK_FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME, NULL);
	gtk_widget_show_all(fileDialog);
	char* filename = gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(fileDialog));
	std::cout << filename << std::endl;
}

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
	g_signal_connect(fileButton, "clicked", G_CALLBACK(create_file_chooser_dialog), mainWindow);
	gtk_header_bar_pack_start(GTK_HEADER_BAR(header), fileButton);
	gtk_widget_show_all(mainWindow);
}

int main (int argc, char** argv)
{
  GtkApplication* app;
  int status;

  app = gtk_application_new("com.github.tristan957.stop_bitchin-start_watchin", G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
  status = g_application_run(G_APPLICATION(app), argc, argv);
  g_object_unref(app);

  return status;
}
