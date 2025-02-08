from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['bank_db']

from routes import *

if __name__ == '__main__':
    app.run(debug=True)