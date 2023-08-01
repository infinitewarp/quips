#!/bin/sh

set -e
cmd="$*"

[ -z "$POSTGRES_USER" ] && POSTGRES_USER="postgres"
[ -z "$POSTGRES_PASSWORD" ] && POSTGRES_PASSWORD="postgres"
[ -z "$POSTGRES_HOST" ] && POSTGRES_HOST="postgres"
[ -z "$POSTGRES_DBNAME" ] && POSTGRES_DBNAME="postgres"
[ -z "$POSTGRES_PORT" ] && POSTGRES_PORT="5432"

postgres_ready() {
python << END
import sys
try:
    import psycopg2cffi as psycopg2
except ModuleNotFoundError:
    import psycopg2
try:
    conn = psycopg2.connect(
        dbname="$POSTGRES_USER",
        user="$POSTGRES_USER",
        password="$POSTGRES_PASSWORD",
        host="$POSTGRES_HOST",
        port="$POSTGRES_PORT",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing..."

[ -z "$REDIS_URL" ] && REDIS_URL="redis://redis:6379"
export REDIS_URL
[ -z "$DATABASE_URL" ] && DATABASE_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DBNAME"
export DATABASE_URL

exec $cmd
