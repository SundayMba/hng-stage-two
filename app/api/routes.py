from . import api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from ..models.user import User
from ..models.organisation import Organisation
from ..extensions import db

@api.route("/users/<string:id>", methods=["GET"])
@jwt_required()
def get_user_record(id):
    user = get_user(id)
    if not user:
        return jsonify({
            "message": f"no user with this id of {id}"
        }), 404
    
    response = {
		"status": "success",
        "message": "User record retrieved successfully",
        "data": {
            "userId": user.userId,
            "firstName": user.firstName,
			"lastName": user.lastName,
			"email": user.email,
			"phone": user.phone
        }
    }
    return jsonify(response), 200

@api.route("/organisations", methods=["GET"])
@jwt_required()
def get_all_organisations():
    userId = get_jwt_identity().get('userId')
    user = get_user(userId)
    if not user:
        return jsonify({
            "message": f"no user with this id of {userId}"
        }), 404
    
    orgs = []
    for org in user.organisations.all():
        orgs.append({
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description
        })
    response = {
        "status": "success",
		"message": "Successfully retrieved user's organisation",
        "data": {
            "organisations": orgs
        }
    }
    return jsonify(response), 200 

@api.route("/organisations/<string:orgId>", methods=["GET"])
@jwt_required()
def get_one_organisation(orgId):
    userId = get_jwt_identity().get('userId') # retrieve the userId
    try:
        user = User.query.filter_by(userId=userId).first()
        org = user.organisations.filter_by(orgId=orgId).first()
        response = {
            "status": "success",
            "message": "successfully retrieved users organisation",
            "data": {
                "orgId": org.orgId,
                "name": org.name, 
                "description": org.description,
            }
        }
        return jsonify(response), 200
    except Exception as e:
        resp = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        return jsonify(resp), 400



@api.route("/organisations", methods=["POST"])
@jwt_required()
def create_organisation():
    name = request.json.get("name")
    description = request.json.get("description")
    org = Organisation()
    org.name = name
    org.description = description
    errors = org.validate_org()
    if errors:
        response = {
            "errors": errors
        }
        return jsonify(response)

    try:
        """Add this organisation to the current logged in user's organisation"""
        userId = get_jwt_identity().get('userId')
        user = get_user(userId)
        user.organisations.append(org)
        db.session.add_all([user, org])
        db.session.commit()
        resp = {
            "status": "success",
            "message": "Organisation created successfully",
            "data": {
	            "orgId": org.orgId, 
				"name": org.name, 
				"description": org.description
            }
        }
        return jsonify(resp), 201
    except Exception as e:
        print(e)
        resp = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        return jsonify(resp), 400
    
@api.route("/organisations/<string:orgId>/users", methods=["POST"])
def add_user_to_organisation(orgId):
    userId = request.json.get("userId")
    org = Organisation.query.filter_by(orgId=orgId).first()
    user = User.query.filter_by(userId=userId).first()
    if not org:
        org = Organisation()
        org.name = f"{user.name}'s Organisation"
    org.users.append(user)
    db.session.add_all([org, user])
    db.session.commit()
    resp = {
        "status": "success",
        "message": "User added to organisation successfully",
    }
    return jsonify(resp), 200

def get_user(userId):
    """Retrieve a user from the database"""
    user = User.query.filter_by(userId=userId).first()
    return user