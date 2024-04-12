from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key= True,
        autoincrement = True)
    
    username = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )

    password = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )
    
    @classmethod
    def register (cls, username, password):
        """Register user w/ hashed password & returns user"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decord('utf8')

        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        """validate that a user exists & that their password is correct"""
        u = User.query.filter_by(username = username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
        
    class UserTrip(db.Model):
        __tablename__ = 'users_trips'

        id = db.Column(
            db.Integer,
            primary_key = True,
            autoincrement = True,
        )

        user_id = db.Column(
            db.Integer,
            db.foreignKey('users.id'),
            nullable = False
        )

        trip_id = db.Column(
            db.Integer,
            db.foreignKey('trips.id'),
            nullable = False
        )


    class Trip(db.Model):
        __tablename__ = 'trips'

        id = db.Column(
            db.Integer,
            primary_key = True,
            autoincrement = True
        )

        location = db.Column(
            db.String,
            nullable = False
        )

        trip_duration = db.Column(
            db.Integer
        )

        mileage = db.Column(
            db.Integer
        )

        notes = db.Column(
            db.String
        )

    class TripChecklist(db.Model):
        __table__name = 'trips_checklists'

        id = db.Column(
            db.Integer,
            primary_key = True,
            autoincrement = True
        )

        trip_id = db.Column(
            db.Integer,
            db.foreignKey('trips.id'),
            nullable = False
        )

        checklist_id = db.Column(
            db.Integer,
            db.foreignKey('checklist.id'),
            nullable = False
        )

    class Checklist(db.Model):
        __tablename__ = 'checklists'

        id = db.Column(
            db.Integer,
            primary_key = True,
            autoincrement = True
        )

        name = db.Column(
            db.String,
            nullable = False
        )

        notes = db.Column(
            db.String
        )

    class ChecklistItems(db.Model):
        __tablename__ = 'checklists_items'

        id = db.Column(
            db.Integer,
            primary_key = True,
            autoincrement = True
        )

        checklist_id = db.Column(
            db.Integer,
            db.foreignKey('checklists.id'),
            nullable = False
        )

        items_id = db.Column(
            db.Integer,
            db.foreignKey('items.id'),
            nullable = False
        )

    class Item(db.Model):
        __tablename__ = 'items'

        id = db.Column(
            db.Integer,
            primary_key = True,
            autoincrement = True
        )

        name = db.Column(
            db.String,
            nullable = False,
            unique = True
        )

        category = db.Column(
            db.String,
            nullable = False,
        )

        essential = db.Column(
            db.Boolean,
            nullable = False
        )

        rain_precautionary = db.Column(
            db.Boolean
        )