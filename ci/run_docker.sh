#!/usr/bin/env bash


docker-compose rm -fvs webserver
docker-compose build
exec docker-compose up