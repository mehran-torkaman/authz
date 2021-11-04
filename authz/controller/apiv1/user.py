from flask import request

from authz.authz import db
from authz.decorator.apiv1 import auth_required
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.util import jsonify, now

class UserController:

    @auth_required
    def get_users_list():
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)
        try:
            users = User.query.all()
        except:
            return jsonify(status=500, code=102)
        user_schema = UserSchema(many=True)
        return jsonify({
            "users" : user_schema.dump(users)
        })

    @auth_required
    def get_user(user_id):
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)
        try:
            user = User.query.get(user_id)
        except:
            return jsonify(status=500, code=102)
        if user is None:
            return jsonify(status=403, code=103)
        user_schema = UserSchema()
        return jsonify({
            "user" : user_schema.dump(user)
        })

    def create_user():
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)
        user_schema = UserSchema(only=["username","password"])
        try:
            data = user_schema.load(request.get_json())
        except:
            return jsonify(status=400, code=104)
        if not data["username"] or not data["password"]:
            return jsonify(status=400, code=105)
        try:
            user = User.query.filter_by(username=data["username"]).first()
        except:
            return jsonify(status=500, code=102)
        if user is not None:
            return jsonify(status=409, code=106)
        user = User(username=data["username"], password=data["password"])
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=102)
        user_schema = UserSchema()
        return jsonify(
            {"user" : user_schema.dump(user)}, status=201
        )

    @auth_required
    def update_user(user_id):
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)
        user_schema = UserSchema(only=["password"])
        try:
            data = user_schema.load(request.get_json())
        except:
            return jsonify(status=400, code=104)
        if not data["password"]:
            return jsonify(status=400, code=105)
        try:
            user = User.query.get(user_id)
        except:
            return jsonify(status=500, code=102)
        if user is None:
            return jsonify(status=403, code=103)
        user.password = data["password"]
        user.last_change_at = now()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=102)
        user_schema = UserSchema()
        return jsonify({
            "user" : user_schema.dump(user)
        })

    @auth_required
    def delete_user(user_id):
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)
        try:
            user = User.query.get(user_id)
        except:
            return jsonify(status=500, code=102)
        if user is None:
            return jsonify(status=403, code=103)
        db.session.delete(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=102)
        return jsonify()
