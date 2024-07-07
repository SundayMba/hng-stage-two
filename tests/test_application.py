import sqlalchemy.exc
from app import create_app
from app.extensions import db
from flask import current_app
import unittest
from app.models.user import User
from app.models.organisation import Organisation
import sqlalchemy
import time
import uuid
import json
import datetime
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

class testCurrentApp(unittest.TestCase):
    """A test for the current App
        this class test for both End to End testcase and unittest
    """
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user1 = User()
        self.user1.email = "mba@gmail.com"
        self.user1.firstName = "mba"
        self.user1.lastName = "kama"
        self.user1.password = '12345'
        self.user1.phone = "09873684762"
        self.user1.hash_password = self.user1.password

        self.user2 = User()
        self.user2.email = "sunday@gmail.com"
        self.user2.firstName = "sunday"
        self.user2.lastName = "kama"
        self.user2.password = '12345'
        self.user2.phone = "09873684762"
        self.user2.hash_password = self.user1.password
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        # end to End test client (e.g acts like the broswer.)
        self.client = self.app.test_client()
    
    
    def tearDown(self) -> None:
        db.drop_all()
        db.session.remove()
        self.app_context.pop()

    def test_current_app_exist(self):
        """ Test that current app exist """
        self.assertIsNotNone(current_app)
    
    def test_current_app_env(self):
        """Test that current app is configured for TESTING env."""
        self.assertTrue(current_app.config['TESTING'])

    def test_User_creation(self):
        """Test user creation"""
        self.assertTrue(self.user1)
        self.assertTrue(self.user2)

    def test_userId_is_unique(self):
        """Test that user id is unique - user creation respect schema constraint"""
        self.assertNotEqual(self.user1.password, self.user2.password)
    
    def test_valid_schema_type(self):
        """Test that user schema type is valid"""
        self.assertIsInstance(self.user1.email, str)
        self.assertIsInstance(self.user1.password, str)
        self.assertIsInstance(self.user1.firstName, str)
        self.assertIsInstance(self.user1.lastName, str)
        self.assertIsInstance(self.user1.phone, str)
        self.assertIsInstance(self.user1.userId, str)
    
    def test_unique_email(self):
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.user1.email = 'abc@gmail.com'
            self.user2.email = 'abc@gmail.com'
            db.session.add_all([self.user1, self.user2])
            db.session.commit()