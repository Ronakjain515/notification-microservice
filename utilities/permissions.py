import os

from rest_framework.permissions import BasePermission

from utilities import messages


class IsAuthenticatedPermission(BasePermission):
    """
    Class for specifying the details can only be manipulated by the user himself.
    """

    message = messages.PERMISSION_DENIED

    def has_permission(self, request, view):
        """
        Function for checking if user is active.
        """
        try:
            auth_header = request.headers.get('Authorization', None)
            head, token = auth_header.split(" ")
            return head == "Bearer" and token == os.getenv("API_KEY")
        except AttributeError:
            return False
