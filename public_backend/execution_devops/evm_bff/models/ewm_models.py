import datetime
import http
import os
import django
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Max, Sum
from rest_framework.response import Response

from evm_bff.api.camunda_v2 import CamundaApi
from evm_bff.api.mqtt import send_command_to_inside_service

# 设置 DJANGO_SETTINGS_MODULE 环境变量（引入settings文件）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'execution_devops.settings')
# 加载 Django 项目配置
django.setup()
from evm_bff.models.db_models import TaskGroup,Task,TaskDsc,Flow,Usersrigra
from evm_bff.api.ewm_workflow import EwmWorkFlow, uiapi
from rest_framework import serializers
from rest_framework import serializers
import pandas as pd
import json
import datetime as dt

# Create your models here.

class TestCycle():
    def __init__(self):
        self.workflow = EwmWorkFlow()

    def build_statics_data(self, group_statics_list):
        """
        return:
        {
            "id":group_id,
            "title":group_title,
            "startTime":group.'startTime',
            "total":task_total_num,
            "wip":task_wip_num,
            "notrun":task_notrun_num,
            "complete":task_finished_num,
            "pass": task_pass_num,
            "fail": task_fail_num,
            "block": task_block_num
        }

        """
        result = []
        for group_data in group_statics_list:
            try:
                tg = TaskGroup.objects.get(group_id=group_data['id'])
            except Exception as e:
                print(e)
                continue
            else:
                total = tg.size
            plan_num = group_data['plan']
            wip_num = group_data['wip']
            notrun_num = group_data['notrun']
            if plan_num:
                finished_num = 0
                wip_num=0
                notrun_num = total
            else:
                finished_num = total - wip_num - notrun_num
            result.append(
                {
                    "id":group_data['id'],
                    "title":tg.title,
                    "startTime":group_data['startTime'],
                    "total":total,
                    "wip":wip_num,
                    "notrun":notrun_num,
                    "complete":finished_num
                }
            )
        return result

    def get_all_statics(self, assignee, password, index = 0,pagesize=5):
        group_statics = self.workflow.getGroupStatusAll(assignee, password,index,pagesize)
        return self.build_statics_data(group_statics)

    def get_assignee_statics(self, assignee, password,index=0,pagesize=5):
        group_statics = self.workflow.getGroupStatusByAssignee(assignee, password,index,pagesize)
        return self.build_statics_data(group_statics)

    def build_group_data(self,active_group_list,status, index, pagesize):
        group_ids = [inst['businessKey'] for inst in active_group_list]
        try:
            tgs= TaskGroup.objects.filter(group_id__in=group_ids,status=status)
        except Exception as e:
            print(e)
        #     break
        # else:
        paginator=Paginator(tgs,pagesize)
        testcycle_idss = paginator.page(index+1)
        total_page = paginator.num_pages
        # page_group=group_ids[0:len(group_ids):int(pagesize)]
        # total_page = len(group_ids)//int(pagesize)+1
        result=[]
        tc = uiapi()
        executor = tc.getuserexcutor()
        for tg in testcycle_idss:
            td=tc.getexecutiondetails(tg)
            completesize=Task.objects.filter(group_id__in=group_ids,status='Completed').count()
            runningsize=Task.objects.filter(group_id__in=group_ids,status__in=['Execution','ConfirmResult']).count()
            opensize=Task.objects.filter(group_id__in=group_ids,status='ReadExecutionSteps').count()
            # try:
            #     assignee=Task.objects.filter(group_id=group_id,status='assignee')
            # except Exception as e:

            result.append({
                'id':tg.group_id,
                "title": tg.title,
                "eta": tg.eta,
                "team": tg.team,
                "size": tg.size,
                "status": tg.status,
                "start_time":tg.start_time,
                "configuration":tg.configuration ,
                "owner":tg.assignee,
                'executionsize': {
                    'complete': completesize,
                    'running': runningsize,
                    'open': opensize
                },
                'executiondata': {
                    'data': td[0],
                    'date': td[1]
                },
            })
        dict={
            'result':result,
            'total':total_page,
            'executor': executor
        }
        return dict

    def build_statistics(self, assignee, password, index=0, pagesize=3):

        processInsts = self.workflow.getActiveGroup(assignee, password, index=0, pagesize=9999)
        # print(processInsts)
        group_ids = [inst['businessKey'] for inst in processInsts]
        # print(group_ids)
        try:
            tgs = TaskGroup.objects.filter(group_id__in=group_ids)
            # print(tgs)
        except Exception as e:
            print(e)
        paginator = Paginator(tgs, pagesize)
        testcycle_idss = paginator.page(index+1)
        total_page = paginator.num_pages
        result = []
        tc = uiapi()
        td=tc.getCompleteAccumulationByUser(assignee)
        for tgs in testcycle_idss:
            tg = tc.getNewAssignment(tgs.group_id, assignee, start=False)
            print(tg)
            tug = tc.getUnAssigned(tgs.group_id, assignee)
            result.append({
                "id": tgs.group_id,
                "title": tgs.title,
                'todayNewAssignment': tg,
                'assigneedto_me': tug['assigneedto_me'],
                'unassignee': tug['unassignee'],
                'completed': tug['completed']
            })

        dict = {
            'result': result,
            'total': total_page,
            'yestdayComplete': td['yestdayComplete'],
            'monthComplete': td['monthComplete'],
        }
        return dict
    def my_statistics(self,assignee, password):
        processInsts = self.workflow.getActiveGroup(assignee, password, index=0, pagesize=9999)
        # print(processInsts)
        group_ids = [inst['businessKey'] for inst in processInsts]
        ui=uiapi()
        gc=ui.getCompleted(assignee)
        works_time=Flow.objects.filter(assignee=assignee,step_id__gt=0,
                                           step_id__lt=999).aggregate(Sum('works_time'))['works_time__sum']
        monthworks_time=Flow.objects.filter(assignee=assignee,step_id__gt=0,
                                           step_id__lt=999,start_time__gt=ui.this_month_startdaytime).aggregate(Sum('works_time'))['works_time__sum']
        data={
            'works_time': works_time,
            'monthworks_time': monthworks_time,
            'monthruninggroup':gc[0],
            'monthcompletedgroup':gc[1],
            'monthruningtask':gc[2],
            'monthcompletedtask':gc[3],
            'runinggroup':gc[4],
            'completedgroup':gc[5],
            'runingtask':gc[6],
            'completedtask':gc[7]

        }
        return data

    def get_assignee_group(self, assignee, password,status, index=0,pagesize=3):

        processInsts = self.workflow.getActiveGroup(assignee, password,index=0, pagesize=9999)
        print(processInsts)
        groups = self.build_group_data(processInsts,status,index,pagesize)

        return groups
        
    def get_all(self, assignee, password, index=0,pagesize=3):

        processInsts = self.workflow.getActiveGroup(assignee, password,index=0, pagesize=9999,byAssignee=False)
        groups = self.build_group_data(processInsts,index,pagesize)

        return groups

    def updateTaskStatus(self,assignee, password, group_id):
        active_tasks = self.workflow.getActiveTaskListByGroupId(assignee, password, group_id,1, 9999)

        # update task table
        for task in active_tasks:
            print(task)
            # """ update task set assignee={assignee}, status={task_name} where group_id={group_id} and task_id={task_id}""".format(assignee=task['assignee'], task_name=task['name'],group_id=group_id, task_id=task['variables']['TestCase']['value'])

            assigntask = Task.objects.get(group_id=group_id, task_id=task['variables']['TestCase']['value'])
            assigntask.owner = task['assignee']
            assigntask.status = task['name']
            assigntask.save()


    def start_cycle(self,assignee, password, group_id):

        group_inst_id = self.workflow.start_taskgroup(assignee, password,group_id)
        tasks = Task.objects.filter(group_id=group_id)
        taskidlist = [task.task_id for task in tasks]
        self.workflow.completePlanTask(assignee, password,group_id, taskidlist)
        self.updateTaskStatus(assignee,password,group_id)

        taskgroup = TaskGroup.objects.get(group_id=group_id)
        taskgroup.start_time = datetime.datetime.now()
        taskgroup.group_inst_id=group_inst_id
        taskgroup.save()

        return group_inst_id

    def roundrobin_assignment(self,group_id, team):
        assignment = {}
        tasks = Task.objects.filter(group_id = group_id, status="Assignment")
        i = 0
        teamsize = len(team)
        for task in tasks:
            assignment[task.task_id] = team[i%teamsize]
            i+=1

        return assignment

    def CompleteAssign(self,assigner, password, group_id, team ):
        
        assignment = self.roundrobin_assignment(group_id, team)
        print(assignment)
        active_tasks = self.workflow.getActiveTaskListByGroupId(assigner, password, group_id)
        task_inst_id_map = {
            task['variables']['TestCase']['value']: task for task in active_tasks
        }

        for task_id, assignee in assignment.items():
            task_inst = task_inst_id_map.get(task_id)
            if task_inst:
                self.workflow.completeAssignTask(assigner,password,task_inst['id'],assignee)

        active_tasks = self.workflow.getActiveTaskListByGroupId(assigner, password, group_id)
        task_inst_id_map = {
            task['variables']['TestCase']['value']: task for task in active_tasks
        }
        for task_id, assignee in assignment.items():
            task_inst = task_inst_id_map.get(task_id)
            if task_inst:
                task_execution_id = task_inst['executionId']
                if "CaseStep" in task_inst['variables']:
                    task_step_id = task_inst['variables']['CaseStep']['value']
                else:
                    task_step_id = "0"
                task_assignee = task_inst['assignee']
                task_inst_id = task_inst['id']
                print("flow insert item")
                print(task_id)
                print(group_id)
                flowitem = Flow(
                    group_id = group_id,
                    dsc_id = 0,
                    task_id = task_id,
                    step_id = task_step_id,
                    result = "",
                    assignee= task_assignee,
                    start_time= None,
                    end_time=None,
                    pause_time=None,
                    create_at= dt.datetime.utcnow().isoformat(timespec='seconds'),
                    task_inst_id=task_inst_id,
                    comments="",
                    execution_id=task_execution_id
                )
                flowitem.save()

            assigntask = Task.objects.get(group_id=group_id, task_id=task_id)
            assigntask.owner = assignee
            assigntask.start_time = datetime.datetime.now()
            assigntask.status = 'ReadExecutionSteps'
            assigntask.save()
        assigneetaskgroup=TaskGroup.objects.get(group_id=group_id)
        assigneetaskgroup.status ='AssignmentCompleted'
        assigneetaskgroup.start_time = datetime.datetime.now()
        assigneetaskgroup.save()

    def kill_cycle(self,assignee, password, group_id, reason, skipCustomListeners=True, skipSubprocesses=True):
        return self.camunda.killInstance(assignee,password,group_id, reason)


    def updateCompleteFlowItem(self, assignee, password, task_inst_id, comment=None):
        start_time, end_time = self.workflow.getTaskStepDuration(assignee, password, execution_id)
        # update flow table
        # 1. update comments
        # 2. update completed task's start, end time

        flowitem = Flow.objects.get(task_inst_id=task_inst_id)
        flowitem.start_time = start_time
        flowitem.end_time = end_time
        flowitem.save()

        

class TestCycleStaticsSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    startTime=serializers.DateTimeField()
    total = serializers.IntegerField()
    wip = serializers.IntegerField()
    notrun = serializers.IntegerField()
    complete=serializers.IntegerField()
class TestCycleSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    eta = serializers.CharField()
    team=serializers.CharField()
    size=serializers.IntegerField()
    status=serializers.CharField()
    configuration=serializers.CharField()
    owner=serializers.CharField()
    start_time=serializers.DateTimeField()
    executionsize = serializers.DictField()
    executiondata = serializers.DictField()

class TestCycleDetailsSerializer(serializers.Serializer):
    case_total = serializers.IntegerField()
    case_pass = serializers.IntegerField()
    case_fail = serializers.IntegerField()
    case_wip = serializers.IntegerField()
    case_notrun = serializers.IntegerField()
    case_block = serializers.IntegerField()
    configuration = serializers.CharField()

class TestStepSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    expect_result = serializers.CharField()

class TestCase():
    def __init__(self):
        self.workflow = EwmWorkFlow()

    def get_not_run(self,assignee,password,group_id,index,pagesize):
        return self.get_active_task_list(assignee, group_id, "ReadExecutionSteps", index, pagesize)


    def get_wip(self,assignee,password, group_id,index,pagesize):
        execution_tasks = self.get_active_task_list(assignee, group_id, "Execution", index, pagesize)
        confirmresult_tasks = self.get_active_task_list(assignee, group_id, "ConfirmResult", index, pagesize)
        total=(len(execution_tasks['result'])+len(confirmresult_tasks['result']))//pagesize+1
        return {
            "result": execution_tasks['result'] + confirmresult_tasks['result'],
            "total": total
        }

    def get_complete(self,assignee,password, group_id, index, pagesize):
        return self.get_active_task_list(assignee, group_id, "Completed", index, pagesize)

    def get_assignement(self, assignee, password,group_id,index,pagesize):
        return self.get_active_task_list(assignee, group_id, "Assignment", index, pagesize)

    def get_active_task_list(self,assignee, group_id,task_name, page_num ,page_size ):
        tg=TaskGroup.objects.get(group_id=group_id)
        tas=Task.objects.filter(group_id=group_id, owner = assignee, status = task_name)

        paginator=Paginator(tas,page_size)
        total_page = paginator.num_pages
        if total_page <= page_num:
            page_num=total_page-1
        tass=paginator.page(page_num+1)
        result=[]
        for ta in tass:
            result.append({
                'id':ta.task_id,
                'title':ta.task_title,
                'configuration':ta.configuration,
                'status':ta.status,
                'owner':ta.owner,
                'owner_team':tg.team,
                'tcd_id':ta.dsc_id,
                'running':ta.running
            })
        dict={
            'result':result,
            'total':total_page
        }

        return dict

    def get_all(self, assignee, password, group_id,index = 0, pagesize = 10):
        return {
            "Assignment": self.get_assignement(assignee, password, group_id, index, pagesize),
            "NotRun":self.get_not_run(assignee,password, group_id,index, pagesize),
            "WIP": self.get_wip(assignee, password, group_id, index, pagesize),
            "Completed": self.get_complete(assignee, password, group_id,index,pagesize)
        }

    def updateTaskStatus(self,assignee, password, group_id,task_id,taskinstid):
        active_tasks = self.workflow.getActiveTaskListByGroupId(assignee, password, group_id,1, 9999)
        for task in active_tasks:
            if task['variables']['TestCase']['value'] == task_id:
                task_execution_id = task['executionId']
                if "CaseStep" in task['variables']:
                    task_step_id = task['variables']['CaseStep']['value']
                else:
                    if task['name'] == "ConfirmResult":
                        task_step_id = "999"
                    else:
                        task_step_id = "0"
                task_assignee = task['assignee']
                task_inst_id = task['id']

                flowitem = Flow(
                    group_id = group_id,
                    dsc_id = 0,
                    task_id = task_id,
                    step_id = task_step_id,
                    result = "",
                    assignee= task_assignee,
                    start_time= None,
                    end_time=None,
                    pause_time=None,
                    create_at= dt.datetime.utcnow().isoformat(timespec='seconds'),
                    task_inst_id=task_inst_id,
                    comments="",
                    execution_id=task_execution_id
                )
                flowitem.save()
                break
        # update task table
        for task in active_tasks:
            # """ update task set assignee={assignee}, status={task_name} where group_id={group_id} and task_id={task_id}""".format(assignee=task['assignee'], task_name=task['name'],group_id=group_id, task_id=task['variables']['TestCase']['value'])

            assigntask = Task.objects.get(group_id=group_id, task_id=task['variables']['TestCase']['value'])
            if assigntask.status !='Completed':
                assigntask.owner = task['assignee']
                assigntask.status = task['name']
                assigntask.save()
        try:
            status=Flow.objects.get(group_id=group_id, task_id=task_id,step_id__gt='1',task_inst_id=taskinstid,result__in=['complete'])
        except Exception as e:
            print(e)
        else:
            task=Task.objects.get(group_id=group_id, task_id=task_id)
            task.status ='Completed'
            task.end_time=status.start_time
            task.save()



    def updateCompleteFlowItem(self, assignee, password, task_inst_id, result="complete", comment=None):
        start_time, end_time = self.workflow.getTaskStepDuration(assignee, password, task_inst_id)
        # update flow table
        # 1. update comments
        # 2. update completed task's start, end time

        print(task_inst_id)

        flowitem = Flow.objects.get(task_inst_id=task_inst_id)
        s=start_time[:10]+' '+start_time[11:19]
        start1_time=datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
        start2_time=start1_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
        if end_time:
            s1 = end_time[:10] + ' ' + end_time[11:19]
            end1_time=datetime.datetime.strptime(s1,'%Y-%m-%d %H:%M:%S')
            end2_time=end1_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            flowitem.works_time = (end2_time - start2_time).seconds
        else:
            end2_time=end_time
        flowitem.start_time = start2_time
        flowitem.end_time = end2_time
        flowitem.result = result
        flowitem.save()


    def createFlowItem(self, assignee, password, group_id, task_id):
        pass

    def CompleteReadExecutionStep(self, assignee, password, group_id, task_id):

        tasksteplist = self.getTestStepsArray(task_id)
        completed_task = self.workflow.completeReadExecutionSteps(assignee,password,group_id,task_id,tasksteplist)
        if completed_task:
            self.updateCompleteFlowItem(assignee, password, completed_task['id']) #,completed_task['variables']['result']['value'])
            self.createFlowItem(assignee, password, group_id, task_id)
            
            self.updateTaskStatus(assignee,password,group_id,task_id,taskinstid=None)

    def CompleteExecution(self,assignee, password,group_id,task_id, result,task_step_id):

        if result == "pass":
            completed_task = self.workflow.stepPass(assignee, password,group_id,task_id)
        elif result == "fail":
            completed_task = self.workflow.stepFail(assignee, password,group_id,task_id)
            ignored_tasks = self.workflow.ignoreLeftTasks(assignee, password, group_id, task_id)
        elif result == "block":
            completed_task = self.workflow.stepBlock(assignee, password,group_id,task_id)
            ignored_tasks = self.workflow.ignoreLeftTasks(assignee, password, group_id, task_id)
        elif result == "ignore":
            completed_task = self.workflow.stepIgnore(assignee, password,group_id,task_id)
        elif result == "execution":
            data={
                "user": assignee,
                "test_cycle_id": group_id,
                "test_case_id": task_id,
                "test_step_id": task_step_id,
            }
            send_command_to_inside_service(data)
            T=Task.objects.get(task_id=task_id)
            if T.running:
                return  Response({"message":"Task already running"}, status=103)
            T.running=True
            T.save()
            completed_task = False
        if completed_task:
            self.updateCompleteFlowItem(assignee, password, completed_task['id'],result) #,completed_task['variables']['result']['value'])
            self.createFlowItem(assignee, password, group_id, task_id)

            self.updateTaskStatus(assignee,password,group_id,task_id,taskinstid=None)
        

    def Complete(self,assignee, password, group_id, task_id, restart):

        completed_task = self.workflow.completeConfirmResult(assignee, password, group_id, task_id,restart)
        # print(completed_task)

        if completed_task:
            self.updateCompleteFlowItem(assignee, password, completed_task['id']) #,completed_task['variables']['result']['value'])
            self.createFlowItem(assignee, password, group_id, task_id)
            if restart:
                taskinstid=None
            else:
                taskinstid=completed_task['id']

            self.updateTaskStatus(assignee,password,group_id,task_id,taskinstid=taskinstid)


    def getTestStepsArray(self,testcase_id):
        ta=Task.objects.get(task_id=testcase_id)
        tcd_id=ta.dsc_id
        tds=TaskDsc.objects.filter(dsc_id=tcd_id)
        test_steps=[]
        for td in tds:
            test_steps.append({
                'action':td.action,
                'id':td.step_id,
                'expected_results':td.expection,
                'notes':td.notes,
                'update_by':ta.owner,
                'update_date':ta.end_time,
                'result':ta.result
            })

        return test_steps


    def stage(self,cycle_title,testcase_id):
        tasks = self.camunda.getActiveTasks("demo","demo",cycle_title)
        stage = ""
        for task in tasks:
            testid = task['variables'].get("TestCase",{}).get('value','')
            if testid == testcase_id:
                stage = task['name']
                if stage == "Execution":
                    stepid = task['variables'].get("CaseStep",{}).get('value','')
                    stage = "_".join((stage,stepid))
                break

        return stage

class TestCaseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    configuration = serializers.CharField()
    status = serializers.CharField()
    owner = serializers.CharField()
    owner_team = serializers.CharField()
    tcd_id = serializers.IntegerField()
    running = serializers.BooleanField()

class TestResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField()
    reason = serializers.CharField()
    tag = serializers.CharField()
    actual_start = serializers.DateTimeField()
    complete = serializers.IntegerField()
    pause_start = serializers.DateTimeField()
    start_date = serializers.DateTimeField()
    total_pause_time = serializers.IntegerField()
    submitter = serializers.CharField()
    submitted_date = serializers.DateTimeField()


class UserManagement():
    def __init__(self):
        self.camunda = CamundaApi()

    def importUser(self, assignee, password, user_set):
        for user_info in user_set:
            status_code = self.camunda.addUser(assignee, password, user_info)
            user = Usersrigra()
            user.username = user_info['idsid']
            user.password = user_info['password']
            user.first_name = user_info['firstname']
            user.last_name = user_info['lastname']
            user.email = user_info['email']
            user.role = user_info['role']
            user.save()

        return 0


class TestStepSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    expected_results = serializers.CharField()
    notes = serializers.CharField()
    active = serializers.BooleanField()
    stepstatus=serializers.CharField()
class TestStep():
    def __init__(self):
        # self.hsdes = HsdEsApi()
        self.camunda = CamundaApi()
        self.workflow=EwmWorkFlow()
    def get_all(self,assignee,password,group_id, test_case_id,page_size,page_num):
        # status_code, testcase = self.hsdes.getArticle(test_case_id)
        # tcd_id = testcase['data'][0]['parent_id']
        ta=Task.objects.get(task_id=test_case_id)
        tcd_id=ta.dsc_id
        active_tasks = self.workflow.getActiveTaskListByGroupId(assignee, password, group_id,1, 9999)
        task_execution_id=None
        for task in active_tasks:
            if task['variables']['TestCase']['value'] == test_case_id:
                task_execution_id = task['executionId']

        # current_step = self.current_step(cycle_title,test_case_id)
        current_step = Flow.objects.filter(task_id=test_case_id,execution_id=task_execution_id).aggregate(Max('step_id'))['step_id__max']
        tds = TaskDsc.objects.filter(dsc_id=tcd_id)
        paginator = Paginator(tds, page_size)
        # 获取每页商品数据

        page_tds = paginator.page(page_num+1)

        # 获取列表页总页数
        total_page = paginator.num_pages
        test_steps = []
        status=Task.objects.get(task_id=test_case_id).status
        description=Task.objects.get(task_id=test_case_id).description
        pre_condition=Task.objects.get(task_id=test_case_id).pre_condition
        for td in page_tds:
            try:
                stepstatus=Flow.objects.get(task_id=test_case_id,step_id=td.step_id,execution_id=task_execution_id).result
            except Exception as e:
                stepstatus=None
            if str(td.step_id) == current_step:
                test_steps.append({
                    'action': td.action,
                    'id': td.step_id,
                    'expected_results': td.expection,
                    'notes': td.notes,
                    'update_by': ta.owner,
                    'update_date': ta.end_time,
                    'result': ta.result,
                    'active':True,
                    'stepstatus':stepstatus
                })
            else:
                test_steps.append({
                    'action': td.action,
                    'id': td.step_id,
                    'expected_results': td.expection,
                    'notes': td.notes,
                    'update_by': ta.owner,
                    'update_date': ta.end_time,
                    'result': ta.result,
                    'active': False,
                    'stepstatus': stepstatus
                })
            dict={
                'test_steps':test_steps,
                'total':total_page,
                'status':status,
                'description':description,
                'pre_condition':pre_condition,
            }
        return dict

    def current_step(self,cycle_title,testcase_id):
        tasks = self.camunda.getActiveTasks("demo","demo",cycle_title)
        print(tasks)
        step = -1
        for task in tasks:
            testid = task['variables'].get("TestCase",{}).get('value','')
            if testid == testcase_id:
                stage = task['name']
                if stage == "Execution":
                    stepid = task['variables'].get("CaseStep",{}).get('value','')
                    step = stepid
                break

        return step


    def complete(self,cycle_title, testcase_id, step_id):
        tasks = self.camunda.getActiveTasks("demo","demo",cycle_title)
        execution_tasks = [task  for task in tasks if task['name'] == "Execution"]
        for task in execution_tasks:
            caseid = task['variables'].get("TestCase",{}).get('value','')
            stepid = task['variables'].get("CaseStep",{}).get('value','')
            if caseid == testcase_id and str(step_id) == stepid:
                self.camunda.completeTask(task['id'],{},"demo","demo")
                break
        else:
            print("no test step matches!!!", cycle_title,testcase_id,step_id)

        return task['id']

if __name__ == "__main__":
    t_c = TestStep()
    # print(t_c.get_all(15014046553,15013503671,5,1))
    # t_c = TestStep()
    # print(t_c.get_all())
    # print(t_c.get_details('bios.meteorlake.QS.Client-BIOS.M_BIOS_FV_v340300-corp_23ww40_5'))

    # ts = TestStep()
    # ts.get_all(16016296036)