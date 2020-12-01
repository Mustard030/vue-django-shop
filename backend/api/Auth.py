from rest_framework.authentication import BaseAuthentication
from . import models
from rest_framework.exceptions import AuthenticationFailed


class UserAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.GET.get('token')
        token_obj = models.Token.objects.filter(token=token).first()

        if request.method in ['POST', 'PUT', 'DELETE']:

            if token_obj:
                return token_obj.user, token
            else:
                raise AuthenticationFailed("无效的token")

        else:
            return token_obj.user, token
