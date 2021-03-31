# Israblog Migration to Wordpress

This is the online-deployed version of the original [Israblog backup repo](https://github.com/eliramk/israblog). It's almost entirely based on the original repo and the work done by [Eliram](https://github.com/eliramk), with a few modifications made by [Shir](https://github.com/shirblc) to create the Wordpress-style XML.

## Requirements

- Python 3

## Installation and Usage (Source directory!)

1. Download or clone the repo.
3. cd into the project directory.
4. Run ```pip install -r requirements.txt``` to install dependencies (they're necessary for the Wordpress conversion).
5. Run flask with:
    - ```export FLASK_APP=app.py```
    - ```export FLASK_ENV=development``` (Recommended)
    - ```flask run```
7. Save your backup file in accordance with the instructions, upload it and download the newly converted file.

## Contents

1. **app.py** - The app file (runs on Flask).
2. **convert.py** - Converts the Israblog HTML backup into XML/JSON.
3. **convert_to_wp.py** - Converts the Israblog HTML backup into a Wordpress XML.
4. **templates** - Folder that contains the two HTML templates required for the deployed version.
5. **static** - Folder that contains the static client-side files, such as JavaScript and CSS files.
6. **uploads** - A placeholder folder to contain all file uploads.

## Dependencies

1. **pytz** - A timezone utility for Python. For more information, check their [PyPI page](https://pypi.org/project/pytz/).
2. **flask** - Flask is a Python microframework used to build and run the local server on which the app is running. For full Flask documentation, try the [Flask website](https://flask.palletsprojects.com/en/1.1.x/).
3. **gunicorn** - A Python WSGI HTTP Server for UNIX. For more information, check their [website](https://gunicorn.org).

## Known Issues

There are no current issues at the time.
