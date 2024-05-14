"""Test Route Views"""

from app import g, create_app, CURR_USER_KEY
from unittest import TestCase
from models import db, connect_db, Trip, UserTrip, User, Pack, TripPack, TripStatus

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError


app = create_app('packlist_test', testing=True)
connect_db(app)


db.create_all()

class TestTripViews(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        
        test_user = User.register(
                "Tester1",
                "Test1",
                "testuser1",
                "testpassword1"
            )
        
        
        
        
        
        
        test_user_id = 1111
        test_user.id = test_user_id
        
        
        db.session.add(test_user)
        db.session.commit()
        
        self.test_user = test_user
        self.test_user_id = test_user.id
        
        trip_status1 = TripStatus(status = 'Upcoming')
        trip_status2 = TripStatus(status = 'Completed')
        
        trip_status1_id = 1
        trip_status1.id = trip_status1_id
        trip_status2_id = 2
        trip_status2.id = trip_status2_id
        
        db.session.add(trip_status1)
        db.session.add(trip_status2)
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
            status = 1)
        
        trip_id = 1111
        trip.id = trip_id
        
        db.session.add(trip)
        db.session.commit()
        
        self.trip_id = trip_id
        self.trip = trip        
        
        test_user.trips.append(trip)
        
        pack = Pack(owner = self.test_user.id,
                    name = "pack",
                    notes = "A simple pack for testing")
    
        packid = 1111
        pack.id = packid
            
        db.session.add(pack)
        db.session.commit()
        
        self.pack = pack
        self.packid = packid
        
        self.client = app.test_client()
        
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
            
        return res
    
    def test_show_trips_successful_view(self):
        """Test render content of a user's trips"""
        with self.client as c:            
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            g.user = sess[CURR_USER_KEY]
                    
            resp = c.get("/trips")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.trip.name}", str(resp.data))
    
    def test_show_trips_unauthorized_view(self):
        """Test render content redirect when not logged in"""
        with self.client as c:
            resp = c.get("/trips", follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))

            
    def test_show_new_successful_trip_form(self):
        """Test render content of new trip form when logged in"""
        with self.client as c:            
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            g.user = sess[CURR_USER_KEY]
                    
            resp = c.get("/trips/new")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create Trip Form", str(resp.data))
                
    def test_show_new_unauthorized_trip_form(self):
        """Test render content of new trip form when not logged in"""

        with self.client as c:
            with c.session_transaction() as sess:
                           
                resp = c.get("/trips/new", follow_redirects=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("Log In Form", str(resp.data))

            

            
    def test_show_successful_trip_details(self):
        """Test render content of trip details when logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user_id
            resp = c.get(f"/trips/{self.test_user.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.trip.name}", str(resp.data))

    
    def test_show_unauthorized_trip_details(self):
        """Test render content of trip details when not logged in"""
        with self.client as c:
            
            resp = c.get(f"/trips/{self.test_user.id}", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))

            
    def test_show_trip_successful_edit_form(self):
        """Test render content of edit form when logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user_id
            resp = c.get(f"/trips/{self.trip.id}/edit")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Trip Form", str(resp.data))
  
    def test_show_unauthorized_trip_edit_form(self):
        """Test render content of edit form when not logged in"""
        with self.client as c:
            resp = c.get(f"/trips/{self.trip.id}/edit", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))
            
    def test_show_succcessful_trip_status_update(self):
        """Test render content of updating a trip status"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user_id
            resp = c.post(f"/trips/{self.trip.id}/status", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.trip.name}", str(resp.data))

            
    def test_show_trip_successful_deleted_view(self):
        """Test render content when a user is logged in and deletes a trip"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user_id
            resp = c.post(f"/trips/{self.trip.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Trips", str(resp.data))
    
    
    def test_show_trip_unauthorized_deleted_view(self):
        """Test render content when a user is not logged in and deletes a trip"""
        with self.client as c:
            resp = c.post(f"/trips/{self.trip.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))
            
            

    def test_add_pack_to_trip(self):
        """Test render content when a user adds a pack to their trip"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user_id
            resp = c.post(f"/trips/{self.trip.id}/{self.pack.id}", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.trip.name}", str(resp.data))


    def test_remove_pack_from_trip(self):
        """Test render content when a user removes a pack to their trip"""
        with self.client as c:
            resp = c.post(f"/trips/{self.trip.id}/{self.pack.id}/delete", follow_redirects=True)
        

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.trip.name}", str(resp.data))


    def test_pack_check_view(self):
        """Test render contents of the test pack view"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
                
            g.user = sess[CURR_USER_KEY]
            resp = c.get(f"/trips/{self.trip.id}/{self.pack.id}/check")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Pack Contents", str(resp.data))


    def test_pack_check_edit(self):
        """Test the render contents of after a user updates a pack via the check pack functaionality"""
        with self.client as c:
            with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.post(f"/trips/{self.trip.id}/{self.pack.id}/check/edit", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.trip.name}", str(resp.data))
