# quips

Silly web app for silly quips. :tada:

![quips-screenshot](https://github.com/infinitewarp/quips/assets/1472326/05e6652d-4f61-4d49-9440-99f2ad7369f8)

Yes, the names of speakers are jumbled. :slightly_smiling_face:

[Live Demo](https://quips.infinitewarp.com/quips/)

## Setup

### Running Locally in Podman or Docker

Using either Podman or Docker, run the app with compose:

    podman compose -f dev.yml up --build

The quips app should start serving on http://127.0.0.1:8000/, but you may need to load some data.

> [!NOTE]
>
> The `dev.yml` compose file is intended only for local use, not production environments.

Loading fixture data:

    podman compose -f dev.yml run django /app/manage.py loaddata trek

Creating admin user:

    podman compose -f dev.yml run django /app/manage.py createsuperuser

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

Local `importquips` usage:

    /app/manage.py importquips [--purge] filename.csv

If you are running in composed containers, you will need to copy the file into the container before running the `importquips` command. For example:

    podman compose -f dev.yml cp ./quips.csv django:/tmp/quips.csv
    podman compose -f dev.yml run django /app/manage.py importquips /tmp/quips.csv


### API Usage

You can query the API for a limited set of read-only data. Supported paths include:

- `/quips/api/speaker/` list speakers
- `/quips/api/speaker/{id}/` get specific speaker
- `/quips/api/cliques/` list cliques
- `/quips/api/cliques/{id}/` get specific clique
