import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models
from .utils.token import get_token_code
from api.models import UserInfo


# Create your views here.


class Login_view(APIView):
    def post(self, request):
        data = json.loads(str(request.body, encoding='utf8'))

        res = {
            'meta': {
                'message': '登陆失败',
                'code': 400
            }}

        exist_user = UserInfo.objects.filter(username=data.get('username'),
                                             password=data.get('password')).exists()
        if exist_user:
            user_obj = UserInfo.objects.get(username=data.get('username'),
                                            password=data.get('password'))
            token = get_token_code(user_obj.username)
            token_obj = models.Token.objects.filter(user_id=user_obj.id).first()
            if token_obj:
                token_obj.token = token
                token_obj.save()
            else:
                models.Token.objects.create(user_id=user_obj.id, token=token)

            res.update({'data': {
                'id': user_obj.id,
                'username': user_obj.username,
                'token': token
            }
            })
            res['meta']['message'] = '登陆成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)


