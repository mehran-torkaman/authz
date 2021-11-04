

class ControllerAccessRules:

    __controller_access_roles = {
        "get_users_list" : ["admin","service"],
        "get_user" : ["admin","service","member:user_id"],
        "create_user" : ["all"],
        "update_user" : ["admin","member:user_id"],
        "delete_user" : ["admin"]
    }

    def get_controller_access_roles(f):
        return ControllerAccessRules.__controller_access_roles[f]
