# Address Book
This application allows you to save your favorites locations on a map.

## How to use
- Click on the map to save an address
- If there's no address nearby, the point will not be saved
- Locations from [this Fusiontable](https://fusiontables.google.com/data?docid=1z4oT18gGaoHWbnk08SV6hhOA99xC3OdheXulCjSW) are loaded also

## How to install
Application wrote in Python with Django, follow the instructions bellow to have your environment set and your server running.
- Install Python 3
- Clone this repository
- Update the `# Fusion Table Permissions` session on `settings.py` (or ask me the key file to access this table)
- run `./startup.sh`

This script will
- Create a virtualenv
- Load the new virtualenv
- Pip Install the required packages present on `requirements.txt`
- Create a SQLite database with the necessary tables
- Start a local server

## Todo
- Handle user sessions: save a session identifier in both local database and Fusiontables in order to load only the actual session addresses
