import os

PLAIN_HTTP = (os.environ.get("PLAIN_HTTP", "no").lower() == "yes")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "12000"))

OPENEHR_API_BASE_URI = os.environ.get("OPENEHR_API_BASE_URI", "http://127.0.0.1:12000")
OPENEHR_API_AUTH_USERNAME = os.environ.get("OPENEHR_API_AUTH_USERNAME", "ehrbase-admin")
OPENEHR_API_AUTH_PASSWORD = os.environ.get("OPENEHR_API_AUTH_PASSWORD", "EvenMoreSecretPassword")
VALIDATE_OPENEHR_API_CERTIFICATE = (os.environ.get("VALIDATE_OPENEHR_API_CERTIFICATE", "no").lower() == "yes")
USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE = (os.environ.get("USE_CUSTOM_OPENEHR_API_CA_CERTIFICATE", "no").lower() == "yes")

DEMOGRAPHIC_API_BASE_URI = os.environ.get("DEMOGRAPHIC_API_BASE_URI", "http://127.0.0.1:12000")
DEMOGRAPHIC_API_AUTH_USERNAME = os.environ.get("DEMOGRAPHIC_API_AUTH_USERNAME", "demographic_user")
DEMOGRAPHIC_API_AUTH_PASSWORD = os.environ.get("DEMOGRAPHIC_API_AUTH_PASSWORD", "demographic_password")
VALIDATE_DEMOGRAPHIC_API_CERTIFICATE = (os.environ.get("VALIDATE_DEMOGRAPHIC_API_CERTIFICATE", "no").lower() == "yes")
USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE = (os.environ.get("USE_CUSTOM_DEMOGRAPHIC_API_CA_CERTIFICATE", "no").lower() == "yes")

PROV_API_BASE_URI = os.environ.get("PROV_API_BASE_URI", "http://127.0.0.1:12000")
PROV_API_AUTH_USERNAME = os.environ.get("PROV_API_AUTH_USERNAME", "prov_user")
PROV_API_AUTH_PASSWORD = os.environ.get("PROV_API_AUTH_PASSWORD", "prov_password")
VALIDATE_PROV_API_CERTIFICATE = (os.environ.get("VALIDATE_PROV_API_CERTIFICATE", "no").lower() == "yes")
USE_CUSTOM_PROV_API_CA_CERTIFICATE = (os.environ.get("USE_CUSTOM_PROV_API_CA_CERTIFICATE", "no").lower() == "yes")
