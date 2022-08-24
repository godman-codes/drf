from .permissions import IsStaffEditorPermission, IsDeleteRolesPermission
from rest_framework import permissions

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser ,IsStaffEditorPermission]

class DeleteRolesPermissionMixin():
    permission_classes = [IsDeleteRolesPermission]