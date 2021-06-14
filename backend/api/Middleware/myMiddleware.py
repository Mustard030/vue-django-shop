from django.utils.deprecation import MiddlewareMixin
from .. import models
from django.http import JsonResponse


class MDW(MiddlewareMixin):
    def process_requests(self, request):
        if request.method in ['POST', 'PUT', 'DELETE']:
            token = request.headers.get('Authorization', None)
            user = models.Token.objects.filter(token=token).first().user
            if not user:
                return JsonResponse({'meta': 500, 'message': '非法访问'}, save=False)
            path = request.path_info
            if user.roles.permissions.filter(url=path).exists():
                return None

            return JsonResponse({'meta': 500}, safe=False)
