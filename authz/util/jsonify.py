from flask import current_app

DBG_MESSAGE = {
    "100" : "OK",
    "101" : "Unsupported Media Type",
    "102" : "Database Error",
    "103" : "Resource Not Found",
    "104" : "Bad Request, Validation Failed",
    "105" : "Empty Field",
    "106" : "Resource Conflict",
    "107" : "Not Implemented",
    "108" : "Resource Has Expired",
    "109" : "Desired Status Failed",
    "110" : "Token Encryption Error",
    "111" : "Resource Not Matched",
    "112" : "Token Required",
    "113" : "Token Decryption Failed",
    "114" : "Token Validation Failed",
    "115" : "Controller Access Role Error",
    "116" : "Access Denied",
    "117" : "Resource Role Not Found"
}

def jsonify(state={}, metadata={}, status=200, code=100, headers={}):
    data = state
    data.update(metadata)
    if current_app.debug:
        data["message"] = DBG_MESSAGE[str(code)]
    data["code"] = code
    return data, status, headers
