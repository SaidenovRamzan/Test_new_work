from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


class IsTokenProvided(BasePermission):
    """Разрешает доступ только если токен предоставлен в запросе"""

    def has_permission(self, request, view):
        """Проверяем, что токен предоставлен в запросе"""
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Token '):
            return False

        token = auth_header.split(' ')[1]

        try:
            token = Token.objects.get(key=token)
            return bool(token)
        except Token.DoesNotExist:
            return False