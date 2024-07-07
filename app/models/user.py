from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_jwt_extended import create_access_token
import datetime

class User(db.Model):
    "User model class"
    __tablename__ = "users"
    userId = db.Column(db.String, unique=True, nullable=False, index=True, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False, index=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super(User, self).__init__(*args, **kwargs)
        self.userId = str(uuid.uuid4())

    def __repr__(self) -> str:
        return "<User {} {}>".format(self.firstName, self.lastName)

    @property
    def hash_password(self):
        """Password getter"""
        return self.password
    
    @hash_password.setter
    def hash_password(self, plain_password):
        """Password setter"""
        self.password = generate_password_hash(plain_password)

    def verify_password(self, plain_password):
        """Validate user password"""
        if not plain_password:
            return False
        return check_password_hash(self.password, plain_password)

    def validate_user(self):
        """User Validation"""
        errors = []
        if not isinstance(self.firstName, str):
            errors.append({
                'field': "firstName",
                'message': "First Name must be a string"
            })
        if not isinstance(self.lastName, str):
            errors.append({
                'field': "lastName",
                'message': "Last Name must be a string"
            })
        if not isinstance(self.email, str):
            errors.append({
                'field': "email",
                'message': "Email Must be a string"
            })
        if not isinstance(self.password, str):
            errors.append({
                'field': "password",
                'message': "password must be a string"
            })
        if self.phone and not isinstance(self.phone, str):
            errors.append({
                'field': "phone",
                'message': "phone must be a string"
            })
        if not self.firstName:
            message = "First Name must not be null"
            response = {
                "field": "firstName",
                "message": message
            }
            errors.append(response)
        if not self.lastName:
            message = "Last Name must not be null."
            response = {
                "field": "lastName",
                "message": message
            }
            errors.append(response)
        if not self.email:
            message = 'Email field must not be null'
            response = {
                "field": "email",
                "message": message
            }
            errors.append(response)
        if self.email and not self.email.__contains__('@'):
            message = "invalid email"
            response = {
                "message": message,
                "field": "email"
            }
            errors.append(response)
        if not self.password:
            message = "password field can not be null"
            response = {
                "field": "password",
                "message": message
            }
            errors.append(response)
        if self.email:
            user = User.query.filter_by(email=self.email).first()
            if user:
                errors.append({
                    "field": "email",
                    "message": "User already exist with this email address"
                })

        return errors
    
    def generate_token(self, seconds=2):
        """Generate Users token"""
        token = create_access_token(identity={"name": self.firstName, 'userId': self.userId})
        return token