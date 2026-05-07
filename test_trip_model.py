"""Test Trip Model"""


from app import create_app

from unittest import TestCase
from models import db, connect_db, Trip, UserTrip, User, Pack, TripPack, TripStatus

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = create_app('packlist_test', testing=True)
connect_db(app)


db.create_all()

class UserModelTestCase(TestCase):
    """   """
    
    def setUp(self):
        """Create test client, add sample data."""
        
        db.drop_all()
        db.create_all()
        
        trip_status = TripStatus(id= 1,status = 'upcoming')
        db.session.add(trip_status)
        db.session.commit()
        
        trip = Trip(
            name = 'testTrip',
            location = 'test location',
            start_date = '04/04/1995',
            end_date = '04/05/1995',
            mileage = 25,
            notes = 'test notes',
            lat = -31,
            lng = -95,
            status = 1
            )
        
       
        
        trip_id = 1111
        trip.id = trip_id
        
        db.session.add(trip)
        db.session.commit()
        
        self.trip = trip
        self.trip_id = trip_id
        
        u1 = User.register(
            "Tester1",
            "Test1",
            "testuser1",
            "testpassword1"
        )
        
        uid1 = 111
        u1.id = uid1
                
        db.session.add(u1)
        db.session.commit()
        
        self.u1 = u1
        self.uid1 = uid1
        
        self.client = app.test_client()
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_trip_model(self):
        """Test to see if creating a trip works"""
        test_trip = Trip(
            name = 'testTrip2',
            location = 'test location2',
            start_date = '04/04/1995',
            end_date = '04/05/1995',
            mileage = 25,
            notes = 'test notes2',
            lat = -31,
            lng = -95,
            status = 1
                    )
        
        test_trip_id = 2222
        test_trip.id = test_trip_id
        
        db.session.add(test_trip)
        db.session.commit()
        
        
        self.assertIsNotNone(Trip.query.get(2222))
        self.assertEqual(len(Trip.query.all()), 2)
        self.assertEqual(self.trip.name, 'testTrip')
        
    def test_invalid_username_create_trip(self):
        with self.assertRaises(IntegrityError) as context:
            test_trip = Trip(
            name = None,
            location = 'test location2',
            start_date = '04/04/1995',
            end_date = '04/05/1995',
            mileage = 25,
            notes = 'test notes2',
            lat = -31,
            lng = -95,
            status = 1)
            
            db.session.add(test_trip)
            db.session.commit()
    
    def test_invalid_password_create_trip(self):
        with self.assertRaises(IntegrityError) as context:
            test_trip = Trip(
            name = 'test trip 2',
            location = None,
            start_date = '04/04/1995',
            end_date = '04/05/1995',
            mileage = 25,
            notes = 'test notes2',
            lat = -31,
            lng = -95,
            status = 1)
            
            db.session.add(test_trip)
            db.session.commit()
        
        
    def test_add_user_trip(self):
        """test adding a trip to an existing user"""
        
        user = User.query.get(self.uid1)
        user.trips.append(self.trip)
        
        user_trip = UserTrip.query.first()
        
        self.assertEqual(len(UserTrip.query.all()), 1)
        self.assertEqual(user_trip.user_id, self.uid1)
        self.assertEqual(user_trip.trip_id, self.trip_id)
    
    
    def test_add_trip_pack(self):
        """Test adding a pack to an existing trip"""
        pack = Pack(owner = self.u1.id,
                    name = "pack",
                    notes = "A simple pack for testing")
    
        packid = 1111
        pack.id = packid
            
        db.session.add(pack)
        db.session.commit()
        
        self.trip.packs.append(pack)
        
        trip_pack = TripPack.query.first()
        
        self.assertEqual(len(TripPack.query.all()), 1)
        self.assertEqual(trip_pack.pack_id, packid)
        self.assertEqual(trip_pack.trip_id, self.trip_id)
        

        