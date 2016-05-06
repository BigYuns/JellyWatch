# Jelly Watch

How to Jelly Watch
The Jelly Watch web app lives at [https://ri-jellywatch.appspot.com](https://ri-jellywatch.appspot.com).

Users can create a bookmark for it on their phones. On an iPhone, they can add it to their homescreen by pressing the share button, scrolling the bottom row and tapping “Add to Home Screen.”

Admins
The default administrator account is admin@admin.com, and the password is “jellywatch383703.” If you log in using this account, you’ll be able to access the “admin” page, where you can create or modify existing user accounts.

You can create accounts for individuals, or check “organizational account” to create a single email+password combination for an entire organization to share. Every time someone logs in using an organizational account, we’ll ask them for their name (there’s no master list of names; names are just recorded.)

Downloading data
The admin page has a link to view the most recent jellyfish sighting as a table, as well as a link to download the data as a CSV.

You need to be logged in as an admin to view the CSV—if you want to write a script to automatically download the CSV, you can use the URL https://ri-jellywatch.appspot.com/jellyfish/csv/3f32e6beaa2042dd995bce8069233ec4 .

Modifying the code
The code is on GitHub here: [https://github.com/BigYuns/JellyWatch](https://github.com/BigYuns/JellyWatch). The site is a Google AppEngine app written in Python, with the frontend written in Javascript.

To modify the form, take a look in the public/templates/form_page.html file. Adding new options is usually as simple as copying the HTML for an existing element and changing it. Adding entirely new fields to collect means requires:
Adding HTML for an entirely new question in form_page.html
Adding Javascript to read the data out of the form and place it into the sighting object that’s sent to the server (bottom of form_page.html)
Adding a new property to the Sighting object in jellyfish.py
Adding code to save the data that’s sent to the server into a Sighting database object, in jellyfish.py’s import_json function
Adding code to export the new field as a CSV in jellyfish.py’s get_sightings function

When changes are made, they need to be deployed to the web using the AppEngine launcher.

## Running & Deploying

_Running the code_ requires downloading the [Google AppEngine SDK](https://cloud.google.com/appengine/downloads) and adding the `JellyWatch` folder. This allows you to run the code locally. To deploy, you'll need to have have a Google account (_not_ a Brown account) with permissions to modify the AppEngine project (email nathaniel_parrott@brown.edu). Alternatively, you can create a new AppEngine project and upload the data using that account.
