import secrets

from django.conf import settings
from rest_framework.permissions import BasePermission

class HasMobileThemeAPIKey(BasePermission):
    message = "Invalid or missing API key."

    def has_permission(self, request, view):
        provided_key = request.headers.get("api-key", "")
        expected_key = settings.MOBILE_THEME_API_KEY

        allowed = bool(provided_key) and secrets.compare_digest(
            provided_key,
            expected_key
        )

        # print(f'Path: {request.path}')
        # print(f'Header Provided: {bool(provided_key)}')
        # print(f'Allowed: {allowed}')

        return allowed


    