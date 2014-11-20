from permission import Permission
from .roles import AdminRole


class AdminPermission(Permission):
    def role(self):
        return AdminRole()