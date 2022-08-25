from .permissions import IsStaffEditorPermission
from rest_framework import permissions

class StaffEditorPermissionMixin():
    # print('cold mixins')
    permission_classes = [IsStaffEditorPermission]

# class DeleteRolesPermissionMixin():
#     permission_classes = [IsDeleteRolesPermission]


class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        # print(lookup_data)
        qs = super().get_queryset(*args, **kwargs)
        # print(qs)
        if self.allow_staff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)