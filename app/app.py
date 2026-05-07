import os 
from flask import Flask, render_template, request, redirect, session, g, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Item, Pack, User, UserTrip, Trip, TripPack, PackItem, TripStatus
from forms import AddUserForm, EditUserForm, LoginForm, AddTripForm, AddPackForm, EditPackForm, EditTripForm, AddItemForm, EditItemForm
from weather import get_weather_information, get_weather_highs_lows
from dashboard import count_trips_completed, count_upcoming_trips, average_trip_mileage, total_mileage_completed, total_days_backpacking
from sqlalchemy import exc, and_, or_


CURR_USER_KEY = 'curr_user'

def add_user_to_g():
        """See if user is logged in, add current user to Flask global"""

        if CURR_USER_KEY in session:
            g.user = User.query.get(session[CURR_USER_KEY])

        else:
            g.user = None
def create_app(database_name, testing=False):            
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "secret secrets"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    debug = DebugToolbarExtension(app)

   

    def serialize_item(item):
        """Serialize an SQLAlchemy obj to dictionary"""

        return {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "essential": item.essential,
            "rain_precautionary": item.rain_precautionary,
            "cold_precautionary": item.cold_precautionary,
            "heat_precautionary": item.heat_precautionary,
            "emergency_precautionary": item.emergency_precautionary,
            "removable": item.removable
        }

    @app.before_request
    def add_user():
        add_user_to_g()
            
            
    def do_login(user):
        """Log in a user"""
        session[CURR_USER_KEY] = user.id

    def do_logout():
        """Log out a user"""
        if CURR_USER_KEY in session:
            del session[CURR_USER_KEY]
                    
    return app


app = create_app('packlist')
connect_db(app)