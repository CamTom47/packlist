"""Test Pack Model"""

from app import create_app
from unittest import TestCase
from models import db, connect_db, Pack, TripPack, Trip, Item, PackItem, User

app = create_app('packlist_test', testing=True)
connect_db(app)

db.create_all()

class PackModelTestCase(TestCase):
    
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
        
        pack = Pack(owner = self.u1.id,
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
        
        
        
    def test_pack_model(self):
        """Test that that pack model works"""
        test_pack = Pack(owner = self.u1.id,
                         name = "testpack",
                         notes = "test notes")
        
        testpackid = 1234
        test_pack.id = testpackid
        
        db.session.add(test_pack)
        db.session.commit()
        
        self.assertEqual(len(Pack.query.all()), 2)
        self.assertEqual(test_pack.id, 1234)
        self.assertEqual(test_pack.name, 'testpack')
        
    def test_adding_pack_item(self):
        """Test adding an item to a pack"""
        
        test_pack = Pack(owner = self.u1.id,
                         name = "testpack",
                         notes = "test notes")
        
        testpackid = 1234
        test_pack.id = testpackid
        
        db.session.add(test_pack)
        db.session.commit()
        
        item1 = Item(name='Maps', category='Navigation', essential=True, rain_precautionary=False, cold_precautionary=False, heat_precautionary=False, emergency_precautionary=True, removable=False)
        item2 = Item(name='Permits', category='Navigation', essential=True, rain_precautionary=False, cold_precautionary=False, heat_precautionary=False, emergency_precautionary=True, removable=False)
        
        item1id = 11
        item1.id = item1id
        
        item2id = 22
        item2.id = item2id
        
        
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()

        pack_item1 = PackItem(pack_id = test_pack.id,
                              item_id = item1.id)
        pack_item2 = PackItem(pack_id = test_pack.id,
                              item_id = item2.id)
        
        pack_item1id = 123
        pack_item1.id = pack_item1id
        pack_item2id = 456
        pack_item2.id = pack_item2id
        
        db.session.add(pack_item1)
        db.session.add(pack_item2)
        db.session.commit()
               
        self.assertEqual(len(PackItem.query.all()), 2)
        self.assertIsNotNone(PackItem.query.get(123))
        self.assertIsNotNone(PackItem.query.get(456))
        self.assertEqual(Item.query.get(11).name, 'Maps')
        self.assertEqual(Item.query.get(22).name, 'Permits')