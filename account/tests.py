from django.test import TestCase

from .models import User, UserFollowing
from .forms import UserRegistrationForm

class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('test_user', 'test_user@email.com', 'test_p4ssw0rd')
        User.objects.create_user('some_user', 'some_user@email.com', 'some_p4ssw0rd')

    def test_get_users(self):
        tu = User.objects.get(username='test_user')
        su = User.objects.get(username='some_user')
        self.assertEqual(tu.username, 'test_user', msg='test_user is not correct!')
        self.assertEqual(su.username, 'some_user', msg='some_user is not correct!')


class UserFollowingTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('test_user', 'test_user@email.com', 'test_p4ssw0rd')
        User.objects.create_user('some_user', 'some_user@email.com', 'some_p4ssw0rd')

    def test_following(self):
        tu = User.objects.get(username='test_user')
        su = User.objects.get(username='some_user')
        following = UserFollowing.objects.create(user=tu, following_user=su)
        self.assertEqual(following.user, tu)
        self.assertEqual(following.following_user, su)


class UserRegistrationFormTest(TestCase):
    def test_user_registration(self):
        form = UserRegistrationForm(data={
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john_doe@email.com',
            'password': 'j0hnd03w',
            'password_conf': 'j0hnd03w',
        })
        self.assertTrue(form.is_valid())

    def test_user_registration_without_username(self):
        form = UserRegistrationForm(data={
            'username': '',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john_doe@email.com',
            'password': 'j0hnd03w',
            'password_conf': 'j0hnd03w',
        })
        self.assertFalse(form.is_valid())

    def test_user_registration_without_password_confirm(self):
        form = UserRegistrationForm(data={
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john_doe@email.com',
            'password': 'j0hnd03w',
        })
        self.assertFalse(form.is_valid())
