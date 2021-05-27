from unittest import TestCase

from app import app
from models import db, User

# be sure to connect Class Pet from models.py

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_db_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    # runs before you test the method so you start with something new
    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url=None)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    # runs after each method so you have a clean slate
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # tests if Test User exists at all
            self.assertIn("Test User", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # tests if Test User is included on the page
            self.assertIn("<h1>Test User</h1>", html)