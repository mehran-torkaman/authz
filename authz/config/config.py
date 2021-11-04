from os import environ

class Config:

    ######################### Global Configuration #########################

    ENV = environ.get("TOYBOX_AUTHZ_ENV","production")

    DEBUG = int(environ.get("TOYBOX_AUTHZ_DEBUG","0"))

    TESTING = int(environ.get("TOYBOX_AUTHZ_TESTING","0"))

    SECRET_KEY = environ.get("TOYBOX_AUTHZ_SECRET_KEY","HARD_STRONG_SECRET_KEY")

    JSONIFY_PRETTYPRINT_REGULAR = DEBUG

    TIMEZONE = environ.get("TOYBOX_AUTHZ_TIMEZONE","Asia/Tehran")

    ######################## Database Configuration ########################

    SQLALCHEMY_DATABASE_URI = environ.get("TOYBOX_AUTHZ_SQLALCHEMY_DATABASE_URI",None)

    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG

    ########################## User Configuration ##########################

    USER_DEFAULT_ROLE = environ.get("TOYBOX_AUTHZ_USER_DEFAULT_ROLE","member")

    USER_DEFAULT_STATUS = int(environ.get("TOYBOX_AUTHZ_USER_DEFAULT_STATUS","0"))

    USER_DEFAULT_EXPIRY_TIME = int(environ.get("TOYBOX_AUTHZ_USER_DEFAULT_EXPIRY_TIME","365"))

    ##################### Authentication Configuration #####################

    JWT_TOKEN_DEFAULT_ALGO = environ.get("TOYBOX_AUTHZ_JWT_TOKEN_DEFAULT_ALGO","HS512")

    JWT_TOKEN_DEFAULT_EXPIRY_TIME = int(environ.get("TOYBOX_AUTHZ_JWT_TOKEN_DEFAULT_EXPIRY_TIME","86400"))
