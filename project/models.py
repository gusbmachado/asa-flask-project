import uuid
import sqlite3
import random
from flask import flash
from datetime import datetime
from dateutil import parser
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
	seats = db.Column(db.Integer)
	date = db.Column(db.DateTime(timezone=False))
	
	def create_tables():
		con = sqlite3.connect('project/db.sqlite')
		cursor = con.cursor()
		cursor.execute('''SELECT COUNT(*) from flight ''')
		result=cursor.fetchall()
		
		if result[0][0]==0:
			Base.metadata.create_all(engine)
			
			f1 = Flight(flightCode="747 AA", departure="LA Airport", arrival="NYC Airport", ticketPrice=668, passengers=208, seats=416, date=datetime(2023, 2, 15, 8, 10, 10)) 
			f2 = Flight(flightCode="747 Delta", departure="NYC Airport", arrival="Miami Airport", ticketPrice=345, passengers=208, seats=416, date=datetime(2023, 2, 15, 10, 10, 10)) 
			f3 = Flight(flightCode="747 JAL", departure="LA Airport", arrival="Dallas Airport", ticketPrice=445, passengers=208, seats=416, date=datetime(2023, 2, 15, 8, 12, 10)) 
			f4 = Flight(flightCode="747 LAN", departure="Dallas Airport", arrival="Atlanta Airport", ticketPrice=337, passengers=208, seats=416, date=datetime(2023, 2, 15, 14, 10, 10)) 
			f5 = Flight(flightCode="747 ANA", departure="Atlanta Airport", arrival="Miami Airport", ticketPrice=255, passengers=208, seats=416, date=datetime(2023, 2, 15, 8, 16, 10))

			try:
				session.add_all([f1, f2, f3, f4, f5])
				session.commit()
			finally:
				session.close()

	def search_flights(search):
		conn = sqlite3.connect('project/db.sqlite')
		cursor = conn.cursor()
		cursor.execute(
			"SELECT * FROM `flight` WHERE `date` LIKE ?",
			("%"+search+"%",)
		)
		results = cursor.fetchall()
		conn.close()
		return results

	def get_flights():
		conn = sqlite3.connect('project/db.sqlite')
		flights = conn.execute('SELECT flightCode, date FROM flight').fetchall()
		conn.close()

		flights_list = list(flights)
		j = 0
		for i in flights_list:
			datetime_obj = parser.parse(i[1])
			flights_list[j] = (flights_list[j][0], datetime_obj.strftime("%B %d, %Y - %H:%M:%S"))
			j+=1

		return flights_list

	def get_airports():
		conn = sqlite3.connect('project/db.sqlite')
		d = conn.execute('SELECT departure FROM flight').fetchall()
		a = conn.execute('SELECT arrival FROM flight').fetchall()
		conn.close()

		airports = list(set(d + a))

		return airports

	def get_routes():
		conn = sqlite3.connect('project/db.sqlite')
		conn.row_factory = sqlite3.Row
		trips = conn.execute('SELECT departure, arrival FROM flight').fetchall()
		conn.close()

		return trips

class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	flightCode = db.Column(db.String(100))
	bookingId = db.Column(db.Integer, unique=True)

	def book_flight(name, flight):
		con = sqlite3.connect('project/db.sqlite')
		book = con.execute('SELECT * from flight WHERE flightCode="%s"' % flight).fetchall()
		if book[0][5] < book[0][6]:
			Base.metadata.create_all(engine)
			
			try:
				for c in session.query(Flight).all():
					if c.flightCode == flight:
						c.passengers += 1
				session.commit()

				session.add(Booking(name=name, flightCode=flight, bookingId=str(uuid.uuid4())))
				session.commit()
			finally:
				session.close()
		else:
			flash(f"There're no more seats!", "error")

	def book_history():
		conn = sqlite3.connect('project/db.sqlite')
		conn.row_factory = sqlite3.Row
		history = conn.execute('SELECT * FROM booking').fetchall()
		conn.close()

		return history

	def book_cancel(flightCode, bookingId):
		Base.metadata.create_all(engine)			
		try:
			x = Booking.query.filter_by(bookingId=bookingId).first()
			current_db_sessions = session.object_session(x)
			current_db_sessions.delete(x)
			current_db_sessions.commit()
			current_db_sessions.close()
			for c in session.query(Flight).all():
				if c.flightCode == flightCode:
					c.passengers -= 1
			session.commit()
		finally:
			session.close()

class Ticket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	flightCode = db.Column(db.String(100))
	seat = db.Column(db.String(10), unique=True)
	ticketNumber = db.Column(db.Integer, unique=True)

	def set_ticket(bookingId):
		con = sqlite3.connect('project/db.sqlite')
		name = con.execute('SELECT name from booking WHERE bookingId="%s"' % bookingId).fetchall()
		flight = con.execute('SELECT flightCode from booking WHERE bookingId="%s"' % bookingId).fetchall()

		row = random.randint(1, 68)
		place = chr(random.randint(ord('A'), ord('F')))
		seat = str(row) + " " + place

		Base.metadata.create_all(engine)

		try:
			session.add(Ticket(name=name[0][0], flightCode=flight[0][0], ticketNumber=str(uuid.uuid4()), seat=seat))
			session.commit()
		finally:
			session.close()

	def get_ticket():
		conn = sqlite3.connect('project/db.sqlite')
		conn.row_factory = sqlite3.Row
		tickets = conn.execute('SELECT * FROM ticket').fetchall()
		conn.close()

		return tickets
