#! /bin/bash
set -o errexit
set -o nounset
poetry run celery -A stocktrader worker -B --loglevel=INFO
