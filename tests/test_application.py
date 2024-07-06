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


    def test_token_expiration(self):
        # Login to get the token
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=2)
        response = self.client.post('/auth/register', data=json.dumps(
            {
                "firstName": "mba",
                'lastName': "kama",
                "email": "mab@gmail.com",
                'userId': str(uuid.uuid4),
                "password": '12345'
            }
        ),
        content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        token = data['data']['accessToken']
        print(f'token: {token}')
        # Wait for the token to expire
        time.sleep(3)  # Wait for more than the token expiration time (3 seconds)

        # Try to access the protected route with the expired token
        response = self.client.get('/auth/protected', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'The token has expired')

    def test_token_expiration(self):
        # Login to get the token
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=1)
        response = self.client.post('/auth/register', data=json.dumps(
            {
                "firstName": "mba",
                'lastName': "kama",
                "email": "mab@gmail.com",
                'userId': str(uuid.uuid4),
                "password": '12345'
            }
        ),
        content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        token = data['data']['accessToken']

        # Wait for the token to expire
        time.sleep(2)  # Wait for more than the token expiration time (2 seconds)

        # Try to access the protected route with the expired token
        response = self.client.get('/auth/protected', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'The token has expired')

    def test_user_claims_unchanged_in_token(self):
        with self.app.test_request_context():
            self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=1)
            response = self.client.post('/auth/register', data=json.dumps(
                {
                    "firstName": "mba",
                    'lastName': "kama",
                    "email": "kama@gmail.com",
                    "password": '12345'
                }
            ),
            content_type='application/json')
            
            self.assertEqual(response.status_code, 201)

            data = json.loads(response.data)
            token = data['data']['accessToken']

            self.assertIsNotNone(token)

            # Use get_jwt_identity to check the identity
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                verify_jwt_in_request()
                identity = get_jwt_identity().get('name')
                self.assertEqual(identity, 'mba')

    def test_organisation_creation(self):
        response = self.client.post('/auth/register', data=json.dumps(
            {
                "firstName": "mba",
                'lastName': "kama",
                "email": "mab@gmail.com",
                "password": '12345'
            }
        ),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # print(data)
        token = data['data']['accessToken']

        # Get all organisations
        response = self.client.get('/api/organisations', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        org_id = data['data']['organisations'][0].get('orgId')

        #test org is valid
        self.assertTrue(org_id)

        response = self.client.get(f'/api/organisations/{org_id}', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        org_name = data['data']['name']
        self.assertEqual(org_name, f"mba's Organisation")

    
    def test_user_firstName_validations(self):
        response = self.client.post('/auth/register', data=json.dumps(
            {
                "firstName": 1233,
                'lastName': 'kama',
                "email": "mabgmail.com",
                "password": '12345'
            }
        ),
        content_type='application/json')
        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)

        self.assertTrue(data['errors'])

    def test_user_lastName_validations(self):
        response = self.client.post('/auth/register', data=json.dumps(
            {
                "firstName": 'mba',
                "email": "mab@gmail.com",
                "password": '12345'
            }
        ),
        content_type='application/json')
        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)

        self.assertTrue(data['errors'])

    def test_user_email_validations(self):
        response = self.client.post('/auth/register', data=json.dumps(
            {
                "firstName": 'mba',
                'lastName': 'kama',
                "email": "mabgmail.com",
                "password": '12345'
            }
        ),
        content_type='application/json')
        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)
        self.assertTrue(data['errors'])

    def test_user_hashed_password(self):
        self.user1.hash_password = 'cat'
        self.assertNotEqual(self.user1.password, 'cat')