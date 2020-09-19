import os

import firebase_admin
from flask import Flask
from flask_sqlalchemy import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

firebase_private_key = os.environ.get("firebase_private_key")
firebase_type = os.environ.get("firebase_type")
firebase_project_id = os.environ.get("firebase_project_id")
firebase_private_key_id = os.environ.get("firebase_private_key_id")
firebase_client_email = os.environ.get("firebase_client_email")
firebase_client_id = os.environ.get("firebase_client_id")
firebase_auth_uri = os.environ.get("firebase_auth_uri")
firebase_token_uri = os.environ.get("firebase_token_uri")
firebase_auth_provider_x509_cert_url = os.environ.get("firebase_auth_provider_x509_cert_url")
client_x509_cert_url = os.environ.get("client_x509_cert_url")
firebase_json = {
    "type": firebase_type,
    "project_id": firebase_project_id,
    "private_key_id": firebase_private_key_id,
    "private_key": firebase_private_key,
    "client_email": firebase_client_email,
    "client_id": firebase_client_id,
    "auth_uri": firebase_auth_uri,
    "token_uri": firebase_token_uri,
    "auth_provider_x509_cert_url": firebase_auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url
}
firebase_setup = firebase_admin.initialize_app()

# firebase_config = {
#     "apiKey" : os.environ.get("firebase_apiKey"),
#     "authDomain" : os.environ.get("firebase_authDomain"),
#     "databaseURL" : os.environ.get("firebase_databaseURL"),
#     "projectId" : os.environ.get("firebase_projectId"),
#     "storageBucket" : os.environ.get("firebase_storageBucket"),
#     "messagingSenderId" : os.environ.get("firebase_messagingSenderId"),
#     "appId" : os.environ.get("firebase_appId")
# }
# initiate = firebase
# auth = firebase.auth()


app = Flask("pyth")
engine = db.create_engine(os.environ.get("db_engine"))
Session = sessionmaker(bind=engine)
session = Session()
