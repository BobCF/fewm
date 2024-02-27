import json
import re
from re import match
from datetime import datetime, timedelta
import traceback

from django import http
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict

from evm_bff.utils import exception
from evm_bff.utils import token
from evm_bff.models.db_models import User, Task, UserProfile

# Create your views here.
resp_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

class LoginView(APIView):

    @exception.exception_catcher
    def post(self,request):
        # create test user
        User.objects.update_or_create(username='test', password='test')
        username=request.data.get('username')
        password=request.data.get('password')
        if not all([username,password]):
                return Response({'code':100,'errmsg':'username or password missing !'}, headers=resp_headers)
        try:
            # search in db user table
            user=User.objects.get(username=username, password=password)
        except Exception as exc:
            return Response({'code':100,'errmsg':'username or password wrong !'}, headers=resp_headers)
        # generate token
        response= Response({'code': 0, 'errmsg': '',
            'data': {"token": token.jwt_encode_token(username)}}, headers=resp_headers)
        return response

# CRUD for single task
class TaskView(APIView):

    @exception.exception_catcher
    @token.token_required
    def get(self,request):
        # query
        print(request.GET.dict())
        task = model_to_dict(Task.objects.get(**request.GET.dict()))
        return Response({'code':0,'errmsg':'', 'data': task}, headers=resp_headers)

    @exception.exception_catcher
    @token.token_required
    def post(self,request):
        # create or update, id as primary key
        print(request.POST.dict())        
        if 'id' in request.POST:
            task, is_created = Task.objects.update_or_create(
                id=request.POST['id'], defaults=request.POST.dict())
        else:
            task, is_created = Task.objects.update_or_create(**request.POST.dict())
        task = model_to_dict(task)
        return Response({'code':0,'errmsg':'','data': task}, headers=resp_headers)

# query for multi tasks
class TasksView(APIView):
    
    @exception.exception_catcher
    @token.token_required
    def get(self,request):
        # query
        username = request.username
        print(request.GET.dict())
        tasks = Task.objects.filter(**request.GET.dict())
        tasks = [model_to_dict(task) for task in tasks]
        return Response({'code':0,'errmsg':'','data': tasks}, headers=resp_headers)
