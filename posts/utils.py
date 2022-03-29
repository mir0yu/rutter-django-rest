from rest_framework import permissions
from .permissions import IsOwner


def override_view_attributes(ref):
    ref.permission_classes = (permissions.IsAuthenticated,
                              IsOwner)
