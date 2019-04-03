from flask import Flask
from config import Config
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Config) # Getting from config.py
mongo = PyMongo(app) # MongoDB client

from app import routes
