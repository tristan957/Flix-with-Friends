#include <gtk/gtk.h>
#include <iostream>

static gboolean
key_press_event_cb (GtkWidget *window,
    GdkEvent *event,
    GtkSearchBar *search_bar)
{
  return gtk_search_bar_handle_event (search_bar, event);
}

static void get_filename(GtkWidget* fileButton, gpointer user_data)
{

	char* filename = gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(fileButton));
	std::cout << filename << std::endl;
}

/*static void create_file_chooser_dialog_cb(GtkWidget* fileButton, gpointer mainWindow)
{
	GtkWidget* fileDialog;
	fileDialog = gtk_file_chooser_dialog_new("Open File", GTK_WINDOW(mainWindow), GTK_FILE_CHOOSER_ACTION_OPEN, ("Cancel"), GTK_RESPONSE_CANCEL, ("Open"), GTK_FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME, NULL);
	gtk_widget_show_all(fileDialog);
	gint resp = gtk_dialog_run(GTK_DIALOG(fileDialog));
	if(resp == GTK_FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME)
	{
		char* filename = gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(fileDialog));
		std::cout << filename << std::endl;
	}
	gtk_widget_destroy(fileDialog);
}*/

static void activate(GtkApplication* app, gpointer user_data)
{
	GtkWidget* mainWindow;
	GtkWidget* header;
	GtkWidget* fileButton;
	GtkWidget* searchBar;
	GtkWidget* entry;
	GtkWidget* box;
	GtkWidget* searchButton;
	//GIcon* searchIcon;
	//GtkWidget* searchImage;

	mainWindow = gtk_application_window_new(app);
	gtk_window_set_default_size(GTK_WINDOW(mainWindow), 1200, 720);

	header = gtk_header_bar_new();
	gtk_header_bar_set_show_close_button(GTK_HEADER_BAR(header), TRUE);
	gtk_header_bar_set_title(GTK_HEADER_BAR(header), "Stop Bitchin', Start Watchin'");
	gtk_header_bar_set_has_subtitle(GTK_HEADER_BAR(header), FALSE);
	gtk_window_set_titlebar(GTK_WINDOW(mainWindow), header);

	fileButton = gtk_file_chooser_button_new("Choose a file", GTK_FILE_CHOOSER_ACTION_OPEN);
	g_signal_connect(fileButton, "file-set", G_CALLBACK(get_filename), NULL);
	gtk_header_bar_pack_start(GTK_HEADER_BAR(header), fileButton);

	/*fileButton = gtk_button_new_with_label("Open a File");
	g_signal_connect(fileButton, "clicked", G_CALLBACK(create_file_chooser_dialog_cb), mainWindow);
	gtk_header_bar_pack_start(GTK_HEADER_BAR(header), fileButton);*/

	searchBar = gtk_search_bar_new();
	gtk_container_add(GTK_CONTAINER(mainWindow), searchBar);

	box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	gtk_container_add(GTK_CONTAINER(searchBar), box);

	entry = gtk_search_entry_new();
	gtk_box_pack_start(GTK_BOX(box), entry, TRUE, TRUE, 0);
	gtk_search_bar_connect_entry(GTK_SEARCH_BAR(searchBar), GTK_ENTRY(entry));
	//gtk_search_bar_set_show_close_button(GTK_SEARCH_BAR(searchBar), TRUE);
	g_signal_connect(mainWindow, "key-press-event", G_CALLBACK(key_press_event_cb), searchBar);

	searchButton = gtk_button_new();
	//"edit-find-symbolic"

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
