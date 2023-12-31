"""Test Related to user model."""

from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create(email, password)


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_successfull(self):
        """Test creating a user with email is successfull"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_create_new_user_email(self):
        """Test email is normalized for new users"""
        smaple_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected_email in smaple_emails:
            user = get_user_model().objects.create_user(email, 'testpass123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test creating a user without and email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass')

    def test_create_superuser_is_success(self):
        """Test creating superuser is successfull."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

