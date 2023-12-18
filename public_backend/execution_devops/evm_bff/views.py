import json
import re
from re import match
from datetime import datetime, timedelta

from django import http
from django.contrib.auth import authenticate, login
from django.views import View
# from rest_framework.generics import   APIView
from rest_framework.pagination import PageNumberPagination

from evm_bff.models.db_serializers import TaskGroupSerializerupload, FlowSerializer, TaskDscSerializer, TaskSerializer
from evm_bff.models.ewm_models import TestCaseSerializer, TestCycleSerializer, TestResultSerializer, TestCycleStaticsSerializer,TestStepSerializer
from evm_bff.models.ewm_models import TestCycle, TestCase, TestStep
from evm_bff.models.ewm_models import UserManagement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from evm_bff.models import Usersrigra
from evm_bff.models import Flow, Attachement

# Create your views here.
resp_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

# username='txwswe'
# password='123456'
# role='worker'
# userinfo = {"username":username,"password":password,'role':role}
# Usersrigra.objects.create_user(userinfo)


class StandardResultPagination(PageNumberPagination):
    # 指定分页的默认页容量
    page_size = 3
    # 指定获取分页数据时，指定页容量参数的名称
    page_size_query_param = 'page_size'
    # 指定分页时的最大页容量
    max_page_size = 5
class ActiveTestCycle(APIView):
    """ Get combination information from Camunda and HSDES for the test cycle"""
 
    def post(self,request):
        page_num = request.data.get('index')
        page_size = request.data.get('page_size')
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        tc = TestCycle()
        tcs = tc.get_assignee_group(assignee, password, page_num if page_num else 0,page_size if page_size else 3)
        active_testcycles = tcs['result']
        print(active_testcycles)
        serializer = TestCycleSerializer(instance=active_testcycles,many=True)
        active_testcycle={
            'list':serializer.data,
            'total':tcs['total']
        }
        return Response(active_testcycle, headers=resp_headers)

class ActiveTestCycleDetails(  APIView):
    """ 
        This api can be called by mobile app.
        when this api is called, the Plan, Assignment tasks should be done.
    """
    serializer_class = TestCaseSerializer
 

    def post(self,request,cycle_id):
        """
        1, Get active tasks from Camunda
        2, Get test cases info from hsdes
        3, combine the 2 parts information
        """
        page_num = request.data.get('index')
        # 每页数量:
        page_size = request.data.get('page_size')
        assignee = request.data.get('assignee')
        password = request.data.get('token')
        table=request.data.get('table')

        tc = TestCase()
        tasks = tc.get_all(assignee, password, cycle_id,page_num,page_size)
        result = {}
        for key in tasks:
            cat_tasks = tasks[key]['result']
            serializer = TestCaseSerializer(instance= cat_tasks,many=True)
            mdict={
                'list':serializer.data,
                'total':tasks[key]['total']
            }
            result[key] = mdict
        return Response(result[str(table)], headers=resp_headers)

class ActiveTestCycleStart(  APIView):
    """ Start a Test Cycle instance from Camunda"""
 

    def post(self,request,cycle_id):
        cycle = TestCycle()
        assignee = request.data.get('assignee')
        password = request.data.get('token')
        process_id = cycle.start_cycle(assignee, password, cycle_id)
        if process_id:
            resp = {"status":0,"data":process_id}
        else:
            resp = {"status":-1,"data":None}
        return Response(resp, headers=resp_headers)

class ActiveTestCycleStop(  APIView):
    """ Kill a Test Cycle instance from Camunda"""
 

    def post(self,request,cycle_id):
        cycle = TestCycle()
        status_code, data = cycle.kill_cycle(cycle_id,"Test")
        return Response(data, headers=resp_headers)

class ActiveTestCycleStatics(  APIView):
      
 
    def post(self,request):
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        index = request.data.get("index")
        pagesize = request.data.get("page_size")
        tc = TestCycle()
        active_testcycles_statics = tc.get_all_statics(assignee, password,index,pagesize)
        print(active_testcycles_statics)
        serializer = TestCycleStaticsSerializer(instance=active_testcycles_statics,many=True)

        return Response(serializer.data, headers=resp_headers)

class StaticTestCycle(  APIView):
    """ For validation lead usage for view all the current test cycle from HSDES"""
  

    def get(self,request):
        tc = TestCycle()
        active_testcycles = tc.get_all()
        print(active_testcycles)
        serializer = TestCycleSerializer(instance=active_testcycles,many=True)

        return Response(serializer.data, headers=resp_headers)

    def post(self,request):
        "create a testcycle"
        pass

class ActiveTestCaseDetails(  APIView):
    """ list the test steps for a test case"""
  

    def post(self,request,testcase_id):
        page_size=request.data['page_size']
        page_num=request.data.get('index')
        ts = TestStep()
        cycle_title = request.data.get("cycle_title")
        test_steps = ts.get_all(cycle_title,testcase_id,page_size,page_num)['test_steps']
        serializer = TestStepSerializer(instance = test_steps, many = True)
        test={
            'list':serializer.data,
            'total':ts.get_all(cycle_title,testcase_id,page_size,page_num)['total']
        }
        return Response(test, headers = resp_headers)

class ActiveTestCaseStart(  APIView):


    def post(self,request,cycle_id, testcase_id):
        """ Complete ReadTestStep task from camunda"""
        tc = TestCase()
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        print(cycle_id)
        print(testcase_id)
        print(assignee)
        print(password)
        tc.CompleteReadExecutionStep(assignee, password,cycle_id, testcase_id)

        return Response({"name":"start testcase"}, headers=resp_headers)

class ActiveTestCaseReStart(  APIView):
    """ Go back to the first test step """
  

    def post(self,request,cycle_id, testcase_id):
        tc = TestCase()
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        tc.Complete(assignee, password,cycle_id, testcase_id,True)
        return Response({"name":"test case restart"}, headers=resp_headers)
class ActiveTestCaseComplete(APIView):
    """ Complete ConfirmResult task from Camunda"""
  

    def post(self,request,cycle_id, testcase_id):
        tc = TestCase()
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        tc.Complete(assignee, password,cycle_id, testcase_id)
        return Response({"name":"testcase complete"}, headers=resp_headers)

class ActiveTestCaseAssign(  APIView):
    """ Complete the Assign task from Camunda"""
  

    def post(self,request,cycle_id):
        tc = TestCycle()
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        team = request.data.get("team")
        tc.CompleteAssign(assignee, password, cycle_id, team)
        return Response({"name":"test case assigned"}, headers=resp_headers)

class ActiveTestCaseStage(  APIView):
    """ Complete the Assign task from Camunda"""
  

    def post(self,request,testcase_id):
        tc = TestCase()
        cycle_title = request.data.get("cycle_title")
        stage = tc.stage(cycle_title,testcase_id)
        return Response({"stage":stage}, headers=resp_headers)
class ActiveTestExecution(APIView):
    """ Complete the Execution task from Camunda"""
  
    def post(self,request, cycle_id, testcase_id):
        tc = TestCase()
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        result = request.data.get("result")
        tc.CompleteExecution(assignee, password,cycle_id,testcase_id,result)
        return Response({"name":"test step complete"}, headers=resp_headers)

class Loginview(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        if not all([username,password]):
                return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9_-]{1,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名')
        if not re.match(r'^[0-9A-Za-z]{2,20}$', password):
            return http.HttpResponseForbidden('请输入正确的密码')
        try:
            user=Usersrigra.objects.get(username=username)
        except Exception as exc:
            return Response({'code':100,'errmsg':'用户名错误'})


        # user=authenticate(username=username,password=password)
        # s=Usersrigra.objects.get(username=username).exists()
        # print(s)
        # print(user.password)
        # print(user.role)
        if user.password != password:
            print(user.password)
            return Response({'code':100,'errmsg':'密码错误'})
        login(request,user)
        request.session.set_expiry(None)
        role=user.role
        return Response({'code':0,'errmsg':'ok','role':role},headers=resp_headers)

# class Usercenter(APIView):
#     def get(self,request):
class UploaddbView(APIView):
    # def __init__(self):

    def post(self,request):
        taskdata=request.data.pop('tasklist')
        print(taskdata)
        groupdata=request.data
        print(groupdata)
        groupdata['group_id']=groupdata.pop('id')
        groupdata['assignee']=groupdata.pop('owner')
        groupdata['configuration']=str(groupdata['configuration'])
        print(groupdata)
        Groupserializer=TaskGroupSerializerupload(data=groupdata)
        Groupserializer.is_valid(raise_exception=True)
        print(Groupserializer.validated_data)
        # 如果校验失败，获取校验失败的错误原因
        print(Groupserializer.errors)
        # if Groupserializer.errors is None:
        # return Response({'code':400,'errmsg':Groupserializer.errors},status=400)
        Groupserializer.save()
        # 如果校验成功，获取校验之后的数据
        for task in taskdata:
            task['group_id']=groupdata['group_id']
            task['task_id']=task.pop('id')
            task['task_title']=task.pop('title')
            steps=task.pop('steps')
            print(task)
            taskserializer = TaskSerializer(data=task)
            taskserializer.is_valid(raise_exception=True)
            print(taskserializer.errors)
            # if taskserializer.errors :
            #     return Response({'code':100,'errors':taskserializer.errors}, status=100)
            taskserializer.save()
            step_id=1
            for item in steps:
                item['step_id']=step_id
                item['task_id']=task['task_id']
                item['dsc_id']=task['dsc_id']
                item['title']=task['task_title']
                item['expection']=item.pop('expected_results')
                print(item)
                taskdscserializer = TaskDscSerializer(data=item)
                taskdscserializer.is_valid()
                print(taskdscserializer.errors)
                taskdscserializer.save()
                # item['group_id']=groupdata['group_id']
                # item['assignee']=groupdata['assignee']
                # del item['action']
                # del item['expection']
                # del item['notes']
                # flowserializer = FlowSerializer(data=item)
                # flowserializer.is_valid()
                # print(flowserializer.errors)
                # flowserializer.save()
                step_id+=1

        return Response({'code':200,'errmsg':'数据已保存'})

class Users(APIView):
    def post(self,request):
        assignee = request.data.get("assignee")
        password = request.data.get("token")
        user_set = request.data.get("userset")

        userM = UserManagement()
        userM.importUser(assignee, password,user_set)

        return Response({'code':200,'errmsg':"User info saved"})


class TestCaseResult(APIView):
    """ Get Test Case Result, inside sync dag pull data from here"""
    def get(self, request):
        interval = datetime.now() - timedelta(hours=24*7)
        flows = Flow.objects.raw("""
            SELECT id,group_id,task_id,assignee, 
                GROUP_CONCAT(result) as step_results, 
                MAX(step_id) as max_step_id 
            from evm_bff_flow 
            where task_id in 
                (SELECT distinct task_id from evm_bff_flow where create_at > '{}' ) 
            GROUP BY task_id;""".format(interval))
        for flow in flows:
            flow.test_case_result = 'running'
            if 'fail' in flow.step_results:
                flow.test_case_result = 'fail'
            elif '99' in str(flow.max_step_id):
                flow.test_case_result = 'complete'
        return Response({'code':0,'errmsg':'','data': [i.to_json() for i in flows]}, headers=resp_headers)
