from permission import Permission
from .rules import AdminRule, UserRule, VisitorRule


class VisitorPermission(Permission):
    def rule(self):
        return VisitorRule()


class UserPermission(Permission):
    def rule(self):
        return UserRule()


class AdminPermission(Permission):
    def rule(self):
        return AdminRule()
