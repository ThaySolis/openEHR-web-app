# Certificate

This folder holds the certificate and key that should be used when running the server in HTTPS mode (`api-cert.pem` and `api-key.pem`).

The certificate and key must be encoded in PEM (Privacy Enhanced Mail) format, as defined in IETF RFC 7468.

## Sample certificate and key

This folder comes with a sample certificate-key pair for the CA and a sample certificate-key pair for the API, which may be used for development and testing.

In order to create a new self-signed certificate, run the `generate.sh` script. It requires `openssl` to be installed.
