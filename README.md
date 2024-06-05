# quips

Silly web app for silly quips. :tada:

[Live Demo](https://quips.infinitewarp.com/quips/)

## Setup

### Running Locally (macOS)

Install and start Docker:

    brew install --cask docker
    open -a Docker

Alternatively, using Docker Toolbox for older CPUs that don't have VT-x and
VT-d:

    brew install --cask docker-toolbox
    docker-machine create -d "virtualbox" mydockermachine
    eval $(docker-machine env mydockermachine)

Run the app with compose:

    docker-compose -f dev.yml up --build

Loading fixture data:

    docker-compose -f dev.yml run django /app/manage.py loaddata trek

Creating admin user:

    docker-compose -f dev.yml run django /app/manage.py createsuperuser

### Importing Quips

You can import quips in bulk via CSV file upload. One row contains a Quip
with one to many Quotes, each Quote having one Speaker's name.

Example row from CSV file:

    1990-06-18,"The Best of Both Worlds, Part 1","I am Locutus of Borg. Resistance is futile. Your life as it has been is over. From this time forward, you will service us.",Jean-Luc Picard,Mister Worf: Fire.,William Riker

This row will create a Quip dated 1990-06-18 with the context "The Best of Both
Worlds, Part 1". The Quip will have two Quotes, the first by "Jean-Luc Picard"
and the second by "William Riker".

The Quips app provides a new Django management command `importquips` to import
this particular CSV format. It has an optional argument `--purge` that removes
all existing Quips, Quotes, and Speakers before importing the file.

`importquips` usage:

    /app/manage.py importquips [--purge] filename.csv

### API Usage

You can query the API for a limited set of read-only data. Supported paths include:

- `/quips/api/speaker/` list speakers
- `/quips/api/speaker/{id}/` get specific speaker
- `/quips/api/cliques/` list cliques
- `/quips/api/cliques/{id}/` get specific clique
