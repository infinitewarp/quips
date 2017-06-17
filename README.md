# quips

Silly web app for silly quips. :tada:

## Live Demo

[Quips on Heroku](https://infinitewarp.herokuapp.com/quips/)

## Setup

### Running Locally (macOS)

Install and start Docker:

    brew install docker
    open -a Docker

Run the app with compose:

    docker-compose -f dev.yml up --build

Loading fixture data:

    docker-compose exec django /entrypoint.sh python /app/manage.py loaddata next-gen

### Running on Heroku

Install and log in to Heroku:

    docker install heroku
    heroku login

Add the Heroku remote and push:

    git remote add heroku https://git.heroku.com/quips.git
    git push heroku master
