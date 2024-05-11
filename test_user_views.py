"""Test Route Views"""

# import os
# import sys

# current = os.path.dirname(os.path.realpath(__file__))

# parent = os.path.dirname(current)

# sys.path.append(parent)

from app import app, CURR_USER_KEY
from unittest import TestCase
from models import db, Trip, UserTrip, User, Pack, TripPack

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError


# Connect to a test database prior to importing app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///packlist_test'
app.config['SQLALCHEMY_ECHO'] = False

# import application


db.create_all()


class TestUserViews(TestCase):
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


        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_homepage(self):
        """Test homepage render content"""
        with self.client as c:
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)


    def test_signup_view(self):
        """Test render content of signup view"""
        with self.client as c:
            resp = c.get('/signup')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign Up Form", str(resp.data))

    def test_login_view(self):
        """Test render content of login view"""
        with self.client as c:
            resp = c.get('/login')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))


    def test_logout_view(self):
        with self.client as c:

            resp = c.get('/logout', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome To Packlist", str(resp.data))

    def test_user_details_view(self):
        with self.client as c:
            resp = c.get(f"/users/{self.test_user.id}")

            print(self.test_user.username)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"'s Profile", str(resp.data))


    def test_user_edit_view(self):
        with self.client as c:
            resp = c.get(f"/users/{self.test_user.id}/edit")

            self.assertEqual(resp.status_code, 200)
