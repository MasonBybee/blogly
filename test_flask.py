from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config["DEBUG_TB_HOSTS"] = ['dont-show-debug-toolbar']




class PetViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()
        db.session.begin_nested()
        user = User(first_name='Test', last_name="Subject")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Subject', html)

    def test_new_user(self):
        with app.test_client() as client:
            d = {
            'first_name': 'Test',
            'last_name': 'Subject2',
            'image_url': 'https://play-lh.googleusercontent.com/0SAFn-mRhhDjQNYU46ZwA7tz0xmRiQG4ZuZmuwU8lYmqj6zEpnqsee_6QDuhQ4ZofwXj=w240-h480-rw'
        }
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="user_details_h1">Test Subject2</h1>', html)
            self.assertEqual(len(User.query.all()), 2)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {
            'first_name': 'Subject',
            'last_name': 'Test',
            'image_url': 'https://play-lh.googleusercontent.com/0SAFn-mRhhDjQNYU46ZwA7tz0xmRiQG4ZuZmuwU8lYmqj6zEpnqsee_6QDuhQ4ZofwXj=w240-h480-rw'
        }
            resp =  client.post('/users/1/edit', data = d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            print(User.query.get(1))

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="user_details_h1">Subject Test</h1>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post('/users/1/delete', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(User.query.all()), 0)
            self.assertIn("<h1>Users</h1>\n<ul>\n  \n</ul>", html)
