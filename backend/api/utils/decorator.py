import json
from django.http import JsonResponse


def need_login(func):
    def wrapper(*args, **kwargs):
        _, request = args
        logined = request.headers.get('Authorization', None)
        if logined:
            return func(*args, **kwargs)
        else:
            res = {
                'meta': {
                    'message': '非法访问，用户未登录',
                    'code': 403
                }}
            return JsonResponse(res, safe=False)

    return wrapper
