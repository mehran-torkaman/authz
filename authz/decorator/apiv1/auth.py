from flask import request
from functools import wraps
from jwt import decode

from authz.model import User
from authz.rule.apiv1 import ControllerAccessRules
from authz.config import Config
from authz.util import jsonify, now

def auth_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.is_json is False:
            return jsonify(status=415, code=101)
        if "X-Auth-Token" not in request.headers:
            return jsonify(status=403, code=112)
        try:
            user_jwt_data = decode(
                request.headers.get("X-Auth-Token"),
                Config.SECRET_KEY,
                Config.JWT_TOKEN_DEFAULT_ALGO
            )
        except:
            return jsonify(status=403, code=113)
        try:
            user = User.query.get(user_jwt_data["user"]["id"])
        except:
            return jsonify(status=500, code=102)
        if user is None:
            return jsonify(status=403, code=103)
        if user.role != user_jwt_data["user"]["role"]:
            return jsonify(status=403, code=114)
        if user.expires_at < now():
            return jsonify(status=403, code=108)
        if user.status != 3:
            return jsonify(status=403, code=109)
        try:
            allowed_roles = ControllerAccessRules.get_controller_access_roles(f.__name__)
        except:
            return jsonify(status=500, code=115)
        if user.role in allowed_roles:
            return f(*args, **kwargs)
        elif user.role == "member" and "member:user_id" in allowed_roles:
            if user.id == args[f.__code__.co_varnames.index("user_id")]:
                return f(*args, **kwargs)
            else:
                return jsonify(status=403, code=116)
        else:
            return jsonify(status=403, code=117)
    return wrapper
