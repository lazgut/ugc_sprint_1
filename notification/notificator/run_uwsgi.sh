#!/usr/bin/env bash

set -e

uwsgi --strict --ini /app/uwsgi.ini
