#!/usr/bin/env bash

# Define container and PostgreSQL properties
CONTAINER_NAME="postgresql-local"
export DB_NAME="local"
export DB_USER="postgres"
export DB_PASS="postgres"
export DB_HOST="localhost"

# Check if the container is already running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  echo "PostgreSQL container '$CONTAINER_NAME' is already running."
else
  # Check if the container exists (but not running)
  if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Removing existing PostgreSQL container '$CONTAINER_NAME'..."
    docker rm $CONTAINER_NAME
  fi

  # Start the PostgreSQL container
  echo "Starting PostgreSQL container '$CONTAINER_NAME'..."
  docker run -d \
    --name $CONTAINER_NAME \
    -e POSTGRES_DB=$DB_NAME \
    -e PGUSER=$DB_USER \
    -e POSTGRES_USER=$DB_USER \
    -e POSTGRES_PASSWORD=$DB_PASS \
    -p 5432:5432 \
    postgres:latest

  # Wait for the container to fully start
  sleep 5

  # Check if the container started successfully
  if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "PostgreSQL container '$CONTAINER_NAME' is now running."
  else
    echo "Failed to start PostgreSQL container '$CONTAINER_NAME'. Check logs for details."
  fi
fi