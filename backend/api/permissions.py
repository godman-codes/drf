from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions): # the class name is made up of Is<the group names you created>Permissions
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'], # this removes get from one of the safe methods only attributes with empty list are safe
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    def has_permission(self, request, view):
        # print(request.user.get_all_permissions())
        if request.user.is_staff: # this checks if the user is a staff
            return True
        return super().has_permission(request, view)




class IsDeleteRolesPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'], # this removes get from one of the safe methods only attributes with empty list are safe
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    def has_permission(self, request, view):
        # print(request.user.get_all_permissions()) # this will print out all the users permissions
        if request.user.is_staff: # this will check if the user is a staff 
            return True
        return super().has_permission(request, view) # we will check all the permission and verify the method as one we have permission for 
