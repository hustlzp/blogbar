from permission import Permission
from .roles import AdminRole, VisitorRole


class VisitorPermission(Permission):
    def role(self):
        return VisitorRole()


class AdminPermission(Permission):
    def role(self):
        return AdminRole()
