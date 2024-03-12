import json
import re
from re import match
from datetime import datetime, timedelta
import traceback
import logging

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
from evm_bff.models.db_models import *

# Create your views here.
resp_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

# login and return token
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
        except:
            # only for test use
            if password == 'ewm!@#123':
                return Response({'code': 0, 'errmsg': '',
                    'data': {"token": token.jwt_encode_token(username)}}, headers=resp_headers)
            return Response({'code':100,'errmsg':'username or password wrong !'}, headers=resp_headers)
        # generate token
        response= Response({'code': 0, 'errmsg': '',
            'data': {"token": token.jwt_encode_token(username)}}, headers=resp_headers)
        return response

# query user info
class UserProfileView(APIView):
    
    @exception.exception_catcher
    @token.token_required
    def get(self,request):
        username = request.username
        user = model_to_dict(UserProfile.objects.get(assignee=username))
        return Response({'code':0,'errmsg':'','data': user}, headers=resp_headers)

# CRUD for single task
class TaskView(APIView):

    @exception.exception_catcher
    @token.token_required
    def get(self,request):
        # query by task fields
        logging.info(request.GET.dict())
        task = model_to_dict(Task.objects.get(**request.GET.dict()))
        return Response({'code':0,'errmsg':'', 'data': task}, headers=resp_headers)

    @exception.exception_catcher
    @token.token_required
    def post(self,request):
        # create or update task, id as primary key
        logging.info(request.POST.dict())
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
        # query by task fields
        username = request.username
        tasks = Task.objects.filter(assignee=username)
        # filter by status
        params = request.GET.dict()
        logging.info(params)
        if 'status' in params:
            if params['status'] == 'finished':
                tasks = tasks.filter(status='complete')
            else:
                tasks = tasks.exclude(status='complete')
        tasks = [model_to_dict(task) for task in tasks]
        return Response({'code':0,'errmsg':'','data': tasks}, headers=resp_headers)
