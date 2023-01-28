import sqlite3
from flask_login import UserMixin
from . import db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///project/db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))

class Flight(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	flightCode = db.Column(db.String(100), unique=True)
	departure = db.Column(db.String(1000))
	arrival = db.Column(db.String(1000))
	ticketPrice = db.Column(db.Float)
	passengers = db.Column(db.Integer)
	date = db.Column(db.DateTime(timezone=False))
	
	def create_tables():
		con = sqlite3.connect('project/db.sqlite')
		cursor = con.cursor()
		cursor.execute('''SELECT COUNT(*) from flight ''')
		result=cursor.fetchall()
		
		if result[0][0]==0:
			Base.metadata.create_all(engine)
			
			f1 = Flight(flightCode="747 AA", departure="LA Airport", arrival="NYC Airport", ticketPrice=668, passengers=416, date=datetime(2023, 2, 15, 8, 10, 10)) 
			f2 = Flight(flightCode="747 Delta", departure="NYC Airport", arrival="Miami Airport", ticketPrice=345, passengers=416, date=datetime(2023, 2, 15, 10, 10, 10)) 
			f3 = Flight(flightCode="747 JAL", departure="LA Airport", arrival="Dallas Airport", ticketPrice=445, passengers=416, date=datetime(2023, 2, 15, 8, 12, 10)) 
			f4 = Flight(flightCode="747 LAN", departure="Dallas Airport", arrival="Atlanta Airport", ticketPrice=337, passengers=416, date=datetime(2023, 2, 15, 14, 10, 10)) 
			f5 = Flight(flightCode="747 ANA", departure="Atlanta Airport", arrival="Miami Airport", ticketPrice=255, passengers=416, date=datetime(2023, 2, 15, 8, 16, 10))

			try:
				session.add_all([f1, f2, f3, f4, f5])
				session.commit()
			finally:
				session.close()

class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	flightCode = db.Column(db.String(100), unique=True)
	bookingId = db.Column(db.Integer, unique=True)

class Ticket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ticketNumber = db.Column(db.Integer, unique=True)
	seat = db.Column(db.String(10), unique=True)
