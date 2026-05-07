# """Test User Model"""
from flask import Flask

from unittest import TestCase
from flask_bcrypt import Bcrypt

from models import connect_db, db, Item, Pack, PackItem, User
from app import create_app

app = create_app('packlist_test', testing=True)
connect_db(app)

db.create_all()

class ItemModelTestCase(TestCase):
    """  """
   
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
    
    def test_item_model(self):
        """Test that the Item model works"""
        
        test_item = Item(name='test', category='test', essential=True, rain_precautionary=False, cold_precautionary=False, heat_precautionary=False, emergency_precautionary=True, created_by = self.u1.id ,removable=False)
        
        test_item_id = 111
        test_item.id = test_item_id
        
        db.session.add(test_item)
        db.session.commit()
        
        self.assertEqual(len(Item.query.all()), 1)
        self.assertEqual(test_item.name, 'test')
        