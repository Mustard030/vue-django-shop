from .. import models
from django.http import JsonResponse


def need_admin(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        # print(request.path_info)
        token = request.headers.get('Authorization', None)
        user = models.Token.objects.filter(token=token).first()

        permission = user.user.is_superuser if user else False
        # print(permission)
        if permission:
            return func(*args, **kwargs)
        else:
            res = {
                'meta': {
                    'message': '非法访问，权限不足',
                    'code': 403
                }}
            return JsonResponse(res, safe=False)

    return wrapper
