#Andrew
from sqlalchemy.sql import func
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///devices.db'
db = SQLAlchemy(app)

class device(db.Model): 
    mac = db.Column(db.String(17), primary_key = True)
    ip = db.Column(db.String(12), unique = True)
    verified = db.Column(db.Boolean)
