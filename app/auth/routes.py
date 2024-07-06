from . import auth
from flask import request
from ..models.user import User
from ..models.organisation import Organisation, users_organisation
from flask import jsonify
from ..extensions import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


@auth.route("/register", methods=["POST"])
def register():
    req = request.json
    user = User()
    user.email = req.get("email")
    user.firstName = req.get("firstName")
    user.lastName = req.get("lastName")
    user.password = req.get("password")
    user.phone = req.get("phone")
    errors = user.validate_user()
    if errors:
        response = {
            "errors": errors
        }
        return jsonify(response), 422
    user.hash_password = user.password
    try:
        """Creating an organisation"""
        org = Organisation()
        org.name = f"{user.firstName}'s Organisation"
        db.session.add(org)
        access_token = user.generate_token()
        #Add the created organisation to the list of org. that belongs to this user
        user.organisations.append(org)

        db.session.add(user)
        db.session.commit() # save to database

        response = {
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone
                }
            }
        }

        return response, 201
    except Exception as e:
        response = {
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
        }
        print(e)
        return response, 400
    


@auth.route("/login", methods=["POST"])
def login():
    req = request.json
    password = req.get("password")
    email = req.get("email")
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = user.generate_token()
        response = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
        }
        return jsonify(response), 200
    else:
        response = {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }
        return jsonify(response), 401

    
@auth.route("/protected")
@jwt_required()
def protected():
    userid = get_jwt_identity()
    return jsonify(user_id=userid)