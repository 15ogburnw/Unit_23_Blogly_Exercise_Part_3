from unittest import TestCase
from app import app


"""

Tests for blogly Flask application

** YOU WILL NEED TO RUN 'seed.py' BEFORE RUNNING THESE TESTS**
"""


class AppTestCase(TestCase):

    def test_user_list(self):
        """Test that the app renders the user list page when a get request is sent"""

        with app.test_client() as client:

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<button class="btn btn-outline-primary my-3"> Create a New User </button>', html)

    def test_new_user_form(self):
        """Test that the app renders the new user form page when a get request is sent"""

        with app.test_client() as client:

            resp = client.get('users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<input class="form-control" type="text" name="last_name" id="last_name" placeholder="Enter Last Name">', html)

    def test_user_details(self):
        """Test that the app renders the user details page when a get request is sent"""

        with app.test_client() as client:

            resp = client.get(f'users/{1}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<button class="btn btn-lg btn-outline-success mx-2" formaction="/users/1/edit" formmethod="get" type="submit">Edit</button>', html)

    def test_edit_user_form(self):
        """Test that the app renders the edit user form page when a get request is sent"""

        with app.test_client() as client:

            resp = client.get(f'users/{1}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<button class="btn btn-lg btn-outline-success px-5 my-2" formmethod="post" formaction="/users/1/edit">Save</button>', html)
