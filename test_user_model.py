"""Test User Model"""

from app import create_app
from unittest import TestCase
from models import db, connect_db, User, UserTrip, Trip, TripStatus

from flask_bcrypt import Bcrypt

app = create_app('packlist_test', testing=True)
connect_db(app)


db.create_all()

class UserModelTestCase(TestCase):
    
    def setUp(self):
        """Create test client, add sample data."""
        
        db.drop_all()
        db.create_all()
        
        u1 = User.register(
            "Tester1",
            "Test1",
            "testuser1",
            "testpassword1"
        )
        
        trip_status = TripStatus(id= 1,status = 'upcoming')
        db.session.add(trip_status)
        db.session.commit()
        
        uid1 = 111
        u1.id = uid1
        
        u2 = User.register(
            "Tester2",
            "Test2",
            "testuser2",
            "testpassword2"
        )
        
        uid2 = 222
        u2.id = uid2
        
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        
        self.u1 = u1
        self.uid1 = uid1
        
        self.u2 = u2
        self.uid2 = uid2
        
        self.client = app.test_client()
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does the basic model work?"""
        self.assertEqual((self.u1.username), "testuser1")
        self.assertEqual((self.u1.first_name), "Tester1")
        self.assertEqual((self.u2.username), "testuser2")
        
    def test_valid_register(self):
        """Does the signup method work?"""
        test_user = User.register(
            "Tester3",
            "Test3",
            "testuser3",
            "testpassword3"
        )
        
        uid = 1234
        test_user.id = uid
        
        db.session.add(test_user)
        db.session.commit()
        
        test_user = User.query.get(uid)
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.first_name, 'Tester3')
        self.assertEqual(test_user.last_name, 'Test3')
        self.assertEqual(test_user.username, 'testuser3')
        self.assertNotEqual(test_user.password, 'testpassword3')
        self.assertTrue(test_user.password.startswith("$2b$"))
                
    def test_authentication(self):
        """Does the authenticate method work?"""
        u = User.authenticate(self.u1.username, 'testpassword1')
        self.assertIsNotNone(u)
        self.assertEqual(self.u1.id, self.uid1)
        
    def test_adding_user_trip(self):
        """Test adding a trip to a user's planned trips"""
        trip1 = Trip(
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
        
        self.u1.trips.append(trip1)
        
        user_trip = UserTrip.query.filter(UserTrip.user_id == self.u1.id).first()
        
        self.assertEqual(len(UserTrip.query.all()), 1)
        self.assertEqual(user_trip.user_id, self.uid1)
        self.assertEqual(user_trip.trip_id, 1)
        
    def test_invalid_username_register(self):
        """Test that a username is valid when signing up"""
        with self.assertRaises(AssertionError) as context:
            invalid_user = User.register('test-first', 'test-last', None, 'testpw')
            uid = 12345
            invalid_user.id = uid
            db.session.commit()
            
    def test_invalid_password_register(self):
        """Test that a password is valid when signing up"""
        with self.assertRaises(ValueError) as context:
            invalid_user = User.register('test-first', 'test-last', 'testuser', None)
            uid = 12345
            invalid_user.id = uid
            db.session.commit()
        
        
