from unittest import TestCase

from app import app
from models import db, User, Post


app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


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
        user = User(first_name="Test", last_name="Subject")
        post = Post(title="Test Post", content="test post content", user_id=1)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_list_users(self):
        """tests list user page"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Subject", html)

    def test_new_user(self):
        """tests creating a new user"""
        with app.test_client() as client:
            d = {
                "first_name": "Test",
                "last_name": "Subject2",
                "image_url": "https://play-lh.googleusercontent.com/0SAFn-mRhhDjQNYU46ZwA7tz0xmRiQG4ZuZmuwU8lYmqj6zEpnqsee_6QDuhQ4ZofwXj=w240-h480-rw",
            }
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="user_details_h1">Test Subject2</h1>', html)
            self.assertEqual(len(User.query.all()), 2)

    def test_edit_user(self):
        """tests editing a user"""
        with app.test_client() as client:
            d = {
                "first_name": "Subject",
                "last_name": "Test",
                "image_url": "https://play-lh.googleusercontent.com/0SAFn-mRhhDjQNYU46ZwA7tz0xmRiQG4ZuZmuwU8lYmqj6zEpnqsee_6QDuhQ4ZofwXj=w240-h480-rw",
            }
            resp = client.post("/users/1/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="user_details_h1">Subject Test</h1>', html)

    def test_delete_user(self):
        """tests deleting a user and all of their posts"""
        with app.test_client() as client:
            resp = client.post("/users/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(len(Post.query.filter(Post.user_id == 1).all()), 0)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(User.query.all()), 0)
            self.assertIn("<h1>Users</h1>\n<ul>\n  \n</ul>", html)

    def test_new_post(self):
        """tests creating a new post"""
        with app.test_client() as client:
            d = {"title": "New Post", "content": "new post content"}
            resp = client.post("/users/1/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/posts/2">New Post</a></li>', html)

    def test_edit_post(self):
        """tests editing a post"""
        with app.test_client() as client:
            d = {"title": "Edited Post", "content": "edited post content"}
            resp = client.post("/posts/1/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edited Post</h1>\n<p>edited post content</p>", html)

    def test_delete_post(self):
        """tests deleting a post"""
        with app.test_client() as client:
            resp = client.post("/posts/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<li><a href="/posts/1">Test Post</a></li>', html)
