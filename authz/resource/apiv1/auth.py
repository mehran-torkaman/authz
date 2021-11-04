from flask_restful import Resource

from authz.controller.apiv1 import AuthTokenController

class AuthTokenResource(Resource):

    def get(self):
        return AuthTokenController.verify_jwt_token()

    def post(self):
        return AuthTokenController.create_jwt_token()
