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
- run `./startup.sh`

This script will
- Create a virtualenv
- Load the new virtualenv
- Pip Install the required packages present on `requirements.txt`
- Create a SQLite database with the necessary tables
- Start a local server

## Todo
- Save selected addresses on the related Fusiontable
