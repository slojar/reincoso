# from rest_framework.permissions import BasePermission
#
# class ReadOnlyPermission(BasePermission):
#     def has_permission(self, request, view):
#         print(view)
#         if request.user.profile.role == 'user':
#             return False
#         if request.user.profile.role == 'admin' and request.method == 'GET':
#             return True
#         if request.user.profile.role == 'super 1':
#             return True
#
#
# class AllowAllPermission(BasePermission):
#     def has_permission(self, request, view):
#         print(view)
#         if request.user.profile.role == 'user':
#             return False
#


def can_view(user, model):
    users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
    if f"view_{str(model).lower()}" not in users_perms:
        return False
    return True


def can_change(user, model):
    users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
    if f"change_{str(model).lower()}" not in users_perms:
        return False
    return True


def can_delete(user, model):
    users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
    if f"delete_{str(model).lower()}" not in users_perms:
        return False
    return True


def can_add(user, model):
    users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
    if f"add_{str(model).lower()}" not in users_perms:
        return False
    return True


# class IsPermitted(BasePermission):
#     def __init__(self, user, model):
#         self.user = user
#         self.model = model
#         print(user)
#         print(model)
#
#     def can_view(user, model):
#         users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
#         print(users_perms)
#         if f"view_{str(model).lower()}" not in users_perms:
#             return False
#         return True
#
#     def can_change(user, model):
#         users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
#         if f"change_{str(model).lower()}" not in users_perms:
#             return False
#         return True
#
#     def can_delete(user, model):
#         users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
#         if f"delete_{str(model).lower()}" not in users_perms:
#             return False
#         return True
#
#     def can_add(user, model):
#         users_perms = [perm.split('.')[1] for perm in user.get_all_permissions()]
#         if f"add_{str(model).lower()}" not in users_perms:
#             return False
#         return True
#
#

