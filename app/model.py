from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float
import config  
 
# DB class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
db = SQLAlchemy(app)
 
# DB classess
class Location(db.Model):
    __tablename__ = 'player'
 
    id = db.Column('playerid', Integer, primary_key=True)
    lat = db.Column('username', String(30), unique=True)
    lng = db.Column('email', String(50), unique=True)
    address= db.Column('address', String(100), unique=False)
    name = db.Column('name', String(100),unique=1)
   
 
    def __init__(self, username=None, email=None,password=None):
        self.id = username
        self.lat = email
        self.lng = password 
        self.address = address 
        self.name = name
 
    def __repr__(self):
        return '<location %s %s>' % (self.address, self.name)
