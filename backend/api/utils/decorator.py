import json
import re
from django.db import models
from django.http import JsonResponse


def need_login(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        print(request.path_info)
        token = request.headers.get('Authorization', None)
        # usergroup = models.UserGroup
        if token:
            return func(*args, **kwargs)
        else:
            res = {
                'meta': {
                    'message': '非法访问，用户未登录',
                    'code': 403
                }}
            return JsonResponse(res, safe=False)

    return wrapper
