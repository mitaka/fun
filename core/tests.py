from django.test import TestCase
from core.models import Author, Post


class AuthorTestCase(TestCase):
    def setUp(self):
        self.user = Author.objects.create_user('testuser', 'testuser@test.com', 'testpassword')
        self.superuser = Author.objects.create_superuser('supertestuser', 'supertestuser@test.com', 'testpassword')

    def tearDown(self):
        del self.user
        del self.superuser

    def test_user_manager(self):
        "Test custom user manager"
        assert self.user.has_usable_password()
        assert self.user.check_password('testpassword')

        assert self.superuser.has_usable_password()
        assert self.superuser.check_password('testpassword')
        assert self.superuser.is_superuser

    def test_user(self):
        "Test proper creation of user"
        assert str(self.user) == 'testuser'
        assert self.user.is_staff is False

    def test_duplicate_users(self):
        "Test creation of duplicate users"
        pass

    def test_blacklisted_domain(self):
        "Test creation of user with blacklisted domain"
        with self.assertRaises(ValueError):
            Author.objects.create_user('bluser', 'bluser@mailinator.com', 'testpassword')


class PostTestCase(TestCase):
    pass
