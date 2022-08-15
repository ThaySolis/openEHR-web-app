#!/usr/bin/env bash

SCRIPT_FOLDER=$( dirname -- "$( readlink -f -- "$0"; )"; )

# create a self-signed certificate for the CA that is valid for 100 years.
openssl req -x509 -newkey rsa:4096 -days 36500 -nodes \
    -config "$SCRIPT_FOLDER/ca-certreq.conf" \
    -keyout "$SCRIPT_FOLDER/ca-key.pem" \
    -out "$SCRIPT_FOLDER/ca-cert.pem"

# create a certificate signing request for the API.
openssl req -new -newkey rsa:4096 -nodes \
    -config "$SCRIPT_FOLDER/api-certreq.conf" \
    -keyout "$SCRIPT_FOLDER/api-key.pem" \
    -out "$SCRIPT_FOLDER/api-cert.csr"

# create a certificate for the API.
openssl x509 -req  -days 825 -sha256 -CAcreateserial \
    -in "$SCRIPT_FOLDER/api-cert.csr" \
    -CA "$SCRIPT_FOLDER/ca-cert.pem" \
    -CAkey "$SCRIPT_FOLDER/ca-key.pem" \
    -out "$SCRIPT_FOLDER/api-cert.pem" \
    -extfile "$SCRIPT_FOLDER/api-certreq.conf"
