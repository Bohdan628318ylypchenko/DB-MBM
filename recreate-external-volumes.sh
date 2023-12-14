#!/bin/bash

# Removing old
docker volume rm app-input db-data

# Creating new
docker volume create app-input
docker volume create db-data

# Copy data into input
docker run -d -e sleep -e 10 --mount source=app-input,target=/app-input --name cp-helper alpine
docker cp ./data/d19.csv cp-helper:/app-input
docker cp ./data/d20.csv cp-helper:/app-input
docker cp ./data/d21.csv cp-helper:/app-input
docker stop cp-helper
docker rm cp-helper
