#!/usr/bin/env bash

# Paths to useful directories.
SCRIPT_FOLDER=$( dirname -- "$( readlink -f -- "$0"; )"; )
SOURCE_FOLDER=$SCRIPT_FOLDER/../..
RESOURCES_FOLDER=$SCRIPT_FOLDER/_resources
APP_FOLDER=$RESOURCES_FOLDER/app

# Generate the data folder if it does not exist.
mkdir -p "$RESOURCES_FOLDER"

# Delete app folder from previous execution.
rm -rf "$APP_FOLDER"

# Copy source files to the app folder.
mkdir -p "$APP_FOLDER"
cp "$SOURCE_FOLDER/requirements.txt" "$APP_FOLDER/"
cp "$SOURCE_FOLDER/app.py" "$APP_FOLDER/"
cp "$SOURCE_FOLDER/app_settings.py" "$APP_FOLDER/"
cp -r "$SOURCE_FOLDER/data_layer" "$APP_FOLDER/"
cp -r "$SOURCE_FOLDER/business_layer" "$APP_FOLDER/"
cp -r "$SOURCE_FOLDER/presentation_layer" "$APP_FOLDER/"
cp -r "$SOURCE_FOLDER/templates" "$APP_FOLDER/"
cp -r "$SOURCE_FOLDER/static" "$APP_FOLDER/"

# Copy the certificates to the data folder.
mkdir -p "$APP_FOLDER/certificate/"
cp "$SOURCE_FOLDER/certificate/api-cert.pem" "$APP_FOLDER/certificate/"
cp "$SOURCE_FOLDER/certificate/api-key.pem" "$APP_FOLDER/certificate/"
cp -r "$SOURCE_FOLDER/other_certificates" "$APP_FOLDER/"

# Build the Docker image.
docker build "$SCRIPT_FOLDER" \
    -t "openehr-web-app-plain"
