"""Test Pack Model"""

from app import create_app, g
from unittest import TestCase
from models import db,connect_db, Pack,Item, PackItem, User

# Connect to a test database prior to importing app

app = create_app('packlist_test', testing=True)
connect_db(app)


db.create_all()

CURR_USER_KEY = 'curr_user'

class ItemModelTestCase(TestCase):
    
    
    
    def setUp(self):
        """Create test client, add sample data."""
        
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
        
        
        test_item = Item(name='test', category='test', essential=True, rain_precautionary=False, cold_precautionary=False, heat_precautionary=False, emergency_precautionary=True, created_by = self.test_user.id ,removable=True)
        
        test_item_id = 111
        test_item.id = test_item_id
        
        db.session.add(test_item)
        db.session.commit()
        
        self.test_item = test_item
        self.test_item_id = test_item_id
        
        self.client = app.test_client()
        
    
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
        
        
    def test_all_items(self):
        """Test render content of all items showing"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.get('/items')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Items", str(resp.data))
    
    
    def test_unauthorized_all_items(self):
        """Test render content of all items showing when not logged in"""
        with self.client as c:
            
            resp = c.get('/items', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))


    def test_create_items_form(self):
        """Test render content of get request to create item form"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.get('/items/new')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create Item Form", str(resp.data))
    
    
    def test_unauthorized_create_items_form(self):
        """Test render content of get request to create item form when not logged in"""
        with self.client as c:
            
            resp = c.get('/items/new', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))
            
    def test_create_item_form_submission(self):
        """Test render content of create item form submission"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.post('/items/new', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Items", str(resp.data))


    def test_edit_items_form(self):
        """Test render content of get request to edit item form"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.get(f'/items/{self.test_item.id}/edit')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Item Form", str(resp.data))
    
    
    
    def test_default_edit_items_form(self):
        """Test render content when a user tries to edit an item that is a system default"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            test_item2 = Item(name='test2', category='test2', essential=True, rain_precautionary=False, cold_precautionary=False, heat_precautionary=False, emergency_precautionary=True, created_by = self.test_user.id ,removable=False)
        
            test_item2_id = 222
            test_item2.id = test_item2_id
            
            db.session.add(test_item2)
            db.session.commit()
            
            resp = c.get(f'/items/{test_item2_id}/edit', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Items", str(resp.data))


    def test_unauthorized_edit_items_form(self):
        """Test render content of get request to edit item form when not logged in"""
        with self.client as c:
            
            resp = c.get(f'/items/{self.test_item.id}/edit', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))
            
    
    def test_edit_item_form_submission(self):
        """Test render content of edit item form submission"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            
            resp = c.post(f'/items/{self.test_item.id}/edit', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Items", str(resp.data))
    

    def test_delete_item(self):
        """Test render content of deleting a user created item"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.post(f'/items/{self.test_item.id}/delete', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Items", str(resp.data))
            
    def test_show_unauthorized_item_delete(self):
        """Test render content of deleting an item when not logged in"""
        with self.client as c:
            resp = c.post(f'/items/{self.test_item.id}/delete', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))


    