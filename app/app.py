from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['bank_db']

app.config['JWT_SECRET_KEY'] = 'epsi'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=5)
jwt = JWTManager(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
