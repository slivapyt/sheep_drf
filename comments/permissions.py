from typing import Any
from rest_framework import permissions, views
from rest_framework.request import Request


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(
        self,  # noqa: IND101
        request: Request,  # noqa: IND101
        view: views.View,  # noqa: IND101
        obj: Any,  # noqa: IND101
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
