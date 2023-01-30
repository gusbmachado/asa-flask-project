from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from .models import Flight, Booking, Ticket

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')


@main.route('/flights', methods=["GET", "POST"])
@login_required
def flights():
	Flight.create_tables()
	flights = Flight.query.all()
	trips = Flight.get_routes()
	airports = Flight.get_airports()
	flightsTime = Flight.get_flights()
	
	return render_template('flights.html', name=current_user.name, flights=flights, trips=trips, airports=airports, flightsTime=flightsTime)

@main.route('/dashboard/<name>/<flight>')
@login_required
def dashboard(name, flight):
	Booking.book_flight(name, flight)
	history = Booking.book_history()
	h = history.pop()
	return render_template('booking.html', name=name, flight=flight, history=h)

@main.route('/dashboard/history')
@login_required
def booking_history():
	history = Booking.book_history()
	return render_template('check_booking.html', history=history)

@main.route('/dashboard/cancel/<flightCode>/<bookingId>')
@login_required
def cancel(flightCode, bookingId):
	Booking.book_cancel(flightCode, bookingId)
	return render_template('cancel.html', flightCode=flightCode)

@main.route('/ticket/<bookingId>')
@login_required
def ticket(bookingId):
	Ticket.set_ticket(bookingId)
	tickets = Ticket.get_ticket()
	t = tickets.pop()
	return render_template('tickets.html', tickets=t)

@main.route('/ticket/history')
@login_required
def ticket_history():
	tickets = Ticket.get_ticket()
	return render_template('check_tickets.html', tickets=tickets)
