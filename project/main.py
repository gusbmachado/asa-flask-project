from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from .models import Flight, Booking

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')


@main.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
	flights = Flight.query.all()
	trips = Flight.get_routes()
	airports = Flight.get_airports()
	flightsTime = Flight.get_flights()
	
	return render_template('profile.html', name=current_user.name, flights=flights, trips=trips, airports=airports, flightsTime=flightsTime)

@main.route('/dashboard/<name>/<flight>')
@login_required
def dashboard(name, flight):
	Booking.book_flight(name, flight)
	return 'Hi, %s. Get a ticket for %s' % (name, flight)