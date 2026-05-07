"""Test Pack Model"""

from app import g, create_app
from unittest import TestCase
from models import db, connect_db, Pack, TripPack, Trip, Item, PackItem, User

app = create_app('packlist_test', testing=True)
connect_db(app)


db.create_all()

CURR_USER_KEY = 'curr_user'


class PackModelTestCase(TestCase):
    
    
    
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
        
        
    
    
    def test_show_successful_packs(self):
        """Render HTML content of a user's packs"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
                
            g.user = sess[CURR_USER_KEY]
                    
            resp = c.get("/packs")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Packs", str(resp.data))
            
    



    def test_show_pack_details(self):
        """Show render contents of a packs details"""    
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.get(f"/packs/{self.pack.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add a Pack", str(resp.data))



    def test_show_successful_create_pack_view(self):
        """Show render contents of creating a new pack when logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.get("/packs/new")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create Pack Form", str(resp.data))
            


    def test_show_unauthorized_pack_edit_form(self):
        """Test render content of pack create form when not logged in"""
        with self.client as c:
            resp = c.get("/packs/new", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))



    def test_show_successful_edit_pack_view(self):
        """Show render contents of updating a pack when logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.get(f"/packs/{self.pack.id}/edit")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Pack", str(resp.data))
            


    def test_show_unauthorized_pack_edit_form(self):
        """Test render content of pack edit form when not logged in"""
        with self.client as c:
            resp = c.get(f"/packs/{self.pack.id}/edit", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))
                
                



    def test_show_succesful_delete_pack_view(self):
        """Show render contents after deleting a pack when logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
            
            g.user = sess[CURR_USER_KEY]
            
            resp = c.post(f"/packs/{self.pack.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Packs", str(resp.data))
            
            
    def test_show_unauthorized_pack_delete(self):
        """Test render content of trying to delete a pack when not logged in"""
        with self.client as c:
    
            resp = c.post(f"/packs/{self.pack.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Log In Form", str(resp.data))
            
    

