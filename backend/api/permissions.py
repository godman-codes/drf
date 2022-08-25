from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions): # the class name is made up of Is<the group names you created>Permissions
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    # def has_permission(self, request, view):
    #     print(request.user.get_all_permissions())
    #     print('cold')
    #     if request.user.is_staff: # this checks if the user is a staff
    #         return True
    #     return super().has_permission(request, view)


