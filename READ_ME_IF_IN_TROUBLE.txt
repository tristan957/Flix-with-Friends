12/23/16 - JMM
If you are having problems here are the steps currently to search for name or Description

1. Load file testing.xlsx (error will occur if you search without doing this first, will need try-catch or something to fix)

2. type to search (none of the search options are selected by default so nothing be displayed, will need to select either title or description then press ENTER or type another letter)

Rating searching is nearly done, others need some work. The 'viewer' aspect has not been implemented at all yet.

Let me know how the regex works for you. It is currently set to a standard string searching algorithm that comes with the 're' package. Seems to work decently, I can improve if need be.

Current Capabilities that are not currently in use:
	DATABASE_NAME.update() - this will go through  the entire excel spreadsheet and update everything regardless if there was something in the field already. This is includes the title of the movie which on occasion can be incorrect. This could possibly be hooked up to a button in the GUI or something

	Within the getImageFiles folder there is code I have written that can be used to get high quality poster images. Sizes vary greatly, if we need specific dimensions I can probably pull it.
