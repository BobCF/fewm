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

from evm_bff.models.db_models import *
from evm_bff.utils import token


# Create your views here.
resp_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

class Login(APIView):
    def post(self,request):
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
        response= Response({
            'code': 0,
            'errmsg': '',
            'data': {
                "token": token.jwt_encode_token(username)
            }
        }, headers=resp_headers)
        return response

# CRUD for single task
class Task(APIView):
    @token.token_required
    def get(self,request):
        return Response({'code':0,'errmsg':''}, headers=resp_headers)

    @token.token_required
    def post(self,request):
        return Response({'code':0,'errmsg':''}, headers=resp_headers)

# query for multi tasks
class Tasks(APIView):
    @token.token_required
    def get(self,request):
        return Response({'code':0,'errmsg':''}, headers=resp_headers)

    @token.token_required
    def post(self,request):
        return Response({'code':0,'errmsg':''}, headers=resp_headers)
