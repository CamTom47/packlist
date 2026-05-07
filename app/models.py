from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    app.app_context().push()
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key= True,
        autoincrement = True)
    
    first_name = db.Column(
        db.Text,
        nullable = False,
    )
  
    last_name = db.Column(
        db.Text,
        nullable = False,
    )
        
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

    trips = db.relationship('Trip',
                                secondary='users_trips',
                                backref='users',
                                cascade='save-update')
    
    @classmethod
    def register (cls, first_name, last_name, username, password):
        """Register user w/ hashed password & returns user"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(first_name = first_name, last_name = last_name, username=username, password=hashed_utf8 )
    
    @classmethod
    def auth_update (cls, first_name, last_name, username, password):
        """Register user w/ hashed password & returns user"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(first_name = first_name, last_name = last_name, username=username, password=hashed_utf8 )
    
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
        db.ForeignKey('users.id'),
        nullable = False
    )

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey('trips.id'),
        nullable = False
    )


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    
    name = db.Column(
        db.Text,
        nullable = False
    )

    location = db.Column(
        db.Text,
        nullable = False
    )

    start_date = db.Column(
        db.Date,
        nullable = False
    )
    end_date = db.Column(
        db.Date,
        nullable = False
    )

    mileage = db.Column(
        db.Integer
    )

    notes = db.Column(
        db.Text
    )
    
    lat = db.Column(
        db.Float
    )
    
    lng = db.Column(
        db.Float
    )
    
    status = db.Column(
        db.Integer,
        db.ForeignKey('trip_status.id'),
        nullable=False
    )

    packs = db.relationship('Pack',
                            secondary='trips_packs',
                            backref='trips',
                            cascade='save-update')
    
    trip_status = db.relationship('TripStatus',
                                  backref='trips',
                                  cascade='save-update')
    
class TripStatus(db.Model):
    __tablename__ = 'trip_status'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    
    status = db.Column(
        db.Text,
        nullable = False
    )


class TripPack(db.Model):
    __tablename__ = 'trips_packs'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey('trips.id'),
        nullable = False
    )

    pack_id = db.Column(
        db.Integer,
        db.ForeignKey('packs.id'),
        nullable = False
    )

class Pack(db.Model):
    __tablename__ = 'packs'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    
    owner = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    name = db.Column(
        db.Text,
        nullable = False
    )

    notes = db.Column(
        db.Text
    )

    items = db.relationship('Item',
                            secondary='packs_items',
                            backref='packs',
                            cascade='save-update')


class PackItem(db.Model):
    __tablename__ = 'packs_items'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    pack_id = db.Column(
        db.Integer,
        db.ForeignKey('packs.id'),
        nullable = False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey('items.id'),
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
        db.Text,
        nullable = False,
        unique = True
    )

    category = db.Column(
        db.Text,
        nullable = False,
    )

    essential = db.Column(
        db.Boolean,
        nullable = False
    )

    rain_precautionary = db.Column(
        db.Boolean
    )
    cold_precautionary = db.Column(
        db.Boolean
    )
    heat_precautionary = db.Column(
        db.Boolean
    )
    emergency_precautionary = db.Column(
        db.Boolean
    )
    
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    
    removable = db.Column(
        db.Boolean
    )