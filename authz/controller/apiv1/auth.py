from datetime import datetime
from flask import request
from jwt import encode
from time import time

from authz.authz import db
from authz.config import Config
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.util import jsonify, now

class AuthTokenController:

    def verify_jwt_token():
        return jsonify(status=501, code=107)

    def create_jwt_token():
        if request.is_json is False:
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
        if user is None:
            return jsonify(status=403, code=103)
        if user.password == data["password"]:
            if user.expires_at < now():
                return jsonify(status=403, code=108)
            if user.status != 3:
                return jsonify(status=403, code=109)
            current_datetime = now()
            current_time = time()
            try:
                user_jwt_token = encode(
                    {
                        "user" :{
                            "id" : user.id,
                            "username" : user.username,
                            "role" : user.role,
                            "expire" : datetime.isoformat(user.expires_at)
                        },
                        "sub" : user.id,
                        "nbf" : current_time,
                        "exp" : current_time + Config.JWT_TOKEN_DEFAULT_EXPIRY_TIME
                    },
                    Config.SECRET_KEY,
                    Config.JWT_TOKEN_DEFAULT_ALGO
                ).encode("utf8")
            except:
                return jsonify(status=500, code=110)
            user.last_login_at = current_datetime
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(status=500, code=102)
            user_schema = UserSchema()
            return jsonify(
                {"user": user_schema.dump(user)},
                status=201,
                headers = {"X-Subject-Token" : user_jwt_token}
            )

        else:
            user.failed_auth_at = now()
            user.failed_auth_count += 1
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(status=500, code=102)
            return jsonify(status=403, code=111)
