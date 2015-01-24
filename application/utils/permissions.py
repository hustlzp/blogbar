from permission import Permission
from .roles import AdminRole, UserRole, VisitorRole


class VisitorPermission(Permission):
    def role(self):
        return VisitorRole()


class UserPermission(Permission):
    def role(self):
        return UserRole()


class AdminPermission(Permission):
    def role(self):
        return AdminRole()
