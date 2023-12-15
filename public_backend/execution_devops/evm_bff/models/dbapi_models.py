import http
import os
import django
from django.core.paginator import Paginator, EmptyPage

# 设置 DJANGO_SETTINGS_MODULE 环境变量（引入settings文件）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'execution_devops.settings')
# 加载 Django 项目配置
django.setup()
from evm_bff.models.db_models import TaskGroup,Task,TaskDsc
# from evm_bff.api.hsdes import HsdEsApi
from evm_bff.api.camunda import CamundaApi
#from api.camunda import CamundaApi
#from api.hsdes import HsdEsApi
from rest_framework import serializers
from rest_framework import serializers
import pandas as pd
import json
# from evm_bff.models.db_models import TaskGroup

# Create your models here.


class TestCycle():
    def __init__(self):
        self.camunda = CamundaApi()

    def get_all_statics(self):
        processInsts = self.camunda.getProcessInsts("demo","demo")
        testcycle_ids = [inst['testcycle_id'] for inst in processInsts]

        result = []
        for item in processInsts:
            testcycle_id = item['testcycle_id']
            testcycle_title = item['businessKey']
            print('testcycle_title=%s'%testcycle_title)
            print('testcycle_id=%s'%testcycle_id)
            testcycle_starttime = item['startTime']
            tasks = self.camunda.getActiveTasks("demo","demo",testcycle_title)
            wip_num = len([task for task in tasks if task['name'] in ('ConfirmResult','Execution')])
            notrun_num = len([task for task in tasks if task['name'] in ('Assignment','ReadExecutionSteps')])
            plan_num = len([task for task in tasks if task['name'] in ('Plan')])
            # status_code, total_re = self.hsdes.getTestCaseNum(testcycle_title)
            # total = total_re['total']
            try:
                tg = TaskGroup.objects.get(title=testcycle_title)
            except Exception as e:
                print(e)
                break
            else:
                total = tg.size
            print('totole=%s'%total)
            if plan_num:
                finished_num = 0
                wip_num=0
                notrun_num = total
            else:
                finished_num = total - wip_num - notrun_num
            result.append(
                {
                    "id":testcycle_id,
                    "title":testcycle_title,
                    "startTime":testcycle_starttime,
                    "total":total,
                    "wip":wip_num,
                    "notrun":notrun_num,
                    "complete":finished_num
                }
            )
        return result

    def get_all(self,page_num=1,page_size=3):
        processInsts = self.camunda.getProcessInsts("demo","demo")
        pInst_df = pd.DataFrame(processInsts)
        testcycle_ids = [inst['testcycle_id'] for inst in processInsts]
        # paginator=Paginator(testcycle_ids,page_size)
        # testcycle_idss = paginator.page(page_num)
        print(testcycle_ids)
        page_testcycle=testcycle_ids[0:len(testcycle_ids):int(page_size)]
        print(page_testcycle)
        print(page_size)
        total_page = len(testcycle_ids)//int(page_size)+1
        print(total_page)
        result=[]
        for testcycle_id in page_testcycle:
            try:
                tg=TaskGroup.objects.get(group_id=testcycle_id)
            except Exception as e:
                print(e)
                break
            else:
                completesize=Task.objects.filter(group_id=testcycle_id,status='complete').count()
                runningsize=Task.objects.filter(group_id=testcycle_id,status='running').count()
                opensize=Task.objects.filter(group_id=testcycle_id,status='open').count()
                result.append({
                    'id':tg.group_id,
                    "title": tg.title,
                    "eta": tg.eta,
                    "team": tg.team,
                    "size": tg.size,
                    "status": tg.status,
                    "start_time":tg.start_time,
                    "configuration":tg.configuration,
                    "owner":tg.assignee,
                    'executionsize':{
                        'complete':completesize,
                        'running':2,
                        'open':opensize
                    },
                    'executiondata':{
                        'data':[600,500,400,300,200,100,0],
                        'date':['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                    }
                })
        dict={
            'result':result,
            'total':total_page
        }
        print(dict['result'])
        return dict

        # status, active_testcycles = self.hsdes.getTestCycle(testcycle_ids)
        # print(testcycle_ids)
        # print(active_testcycles)
        # testcycle_df = pd.DataFrame(active_testcycles['data'])
        # print(testcycle_df)
        # merged = testcycle_df.merge(pInst_df, how="left",left_on="id",right_on="testcycle_id")
        #
        # result_df = pd.DataFrame()
        # result_df['id'] = merged['id']
        # result_df['title'] = merged['title']
        # result_df['eta_request_ww'] = merged['central_firmware.milestone.eta_request']
        # result_df['release'] = merged['central_firmware.milestone.release']
        # result_df['plc_milestone'] = merged['central_firmware.milestone.plc_milestone']
        # result_df['milestone_breakdown'] = merged['central_firmware.milestone.milestone_breakdown']
        # result_df['owner'] = merged['owner']
        # result_df['owner_team'] = merged['central_firmware.milestone.owner_team']
        # result_df['startTime'] = merged['startTime']
        # result_df['instance_id'] = merged['instance_id']
        # return result_df.to_dict('records')


    def get_cycle_title(self,cycle_id):
        try:
            tg = TaskGroup.objects.get(group_id=cycle_id)
        except Exception as e:
            print(e)
        else:
            title=tg.title
        return title
        # status_code, cycle = self.hsdes.getArticle(cycle_id)
        # return cycle['data'][0]['title']

    def get_details(self,testcycle_title="bios.oakstream_diamondrapids.PSS0.5.Server-BIOS.Update phoenix with Android mobile Demo Mode"):
        tc_status_code, tc_data = self.hsdes.getTestCases(testcycle_title)
        tr_status_code, tr_data = self.hsdes.getTestResult(testcycle_title)
        print(tr_status_code,tr_data)
        test_result_df = None
        if tr_status_code == 200 and tr_data['data']:
            test_result_df = pd.DataFrame(tr_data['data'])

        test_case_df = None
        if tc_status_code == 200 and tc_data['data']:
            test_case_df = pd.DataFrame(tc_data['data'])

        details = {}
        if test_case_df is not None:
            details['case_total'] = test_case_df.shape[0]
            if test_result_df is not None:
                merged = test_case_df.merge(test_result_df, how="left",left_on="id", right_on="parent_id")
                status_reason_values = merged['status_reason'].value_counts(dropna=False)
                status_values = merged['status_y'].value_counts(dropna=False)
                details['case_pass'] = status_reason_values['complete.pass'] if 'complete.pass' in status_reason_values else 0
                details['case_block'] = status_values['blocked'] if 'blocked' in status_values else 0
                details['case_notrun'] = merged['parent_id_y'].isnull().sum()
                details['case_fail'] = status_reason_values['complete.fail'] if 'complete.fail' in status_reason_values else 0
                details['case_wip'] = status_values['open'] if 'open' in status_values else 0
            else:
                details['case_pass'] = 0
                details['case_block'] = 0
                details['case_notrun'] = test_case_df.shape[0]
                details['case_fail'] = 0
                details['case_wip'] = 0

            details['configurations'] = test_case_df['central_firmware.test_case.configuration'].unique().tolist()

        return details

    def start_cycle(self,cycle_id):
        title = self.get_cycle_title(cycle_id)
        instances = self.camunda.getProcessInsts("demo","demo")
        instance_id = ""
        for ins in instances:
            # print(ins)
            if title == ins["businessKey"]:
                instance_id = ins["instance_id"]
                break
        else:
            instance_id = self.camunda.startProcess("demo","demo",title,cycle_id)
        tc_data=Task.objects.filter(group_id=cycle_id)
        print(tc_data)
        # tc_status_code, tc_data = self.hsdes.getTestCases(title)
        # print(tc_status_code)
        payload = {}
        if tc_data:
            tc_ids = ["\"" + str(item.task_id) + "\"" for item in tc_data]

            plan_variable = {
                "variables":{
                    "TestSuite":{
                        "type":"Object",
                        "value":"[" + ",".join(tc_ids) + "]",
                        "valueInfo": {
                            "objectTypeName": "java.util.ArrayList<java.lang.String>",
                            "serializationDataFormat":"application/json"
                        }
                    }
                },
                "withVariablesInReturn":True
            }
            payload = plan_variable

        tasks = self.camunda.getActiveTasks("demo","demo",title)
        taskid = ""
        for task in tasks:
            if task['name'] == "Plan":
                taskid = task['id']
                break
        if taskid:
            self.camunda.completeTask(taskid,payload,"demo","demo")

        return instance_id

    def kill_cycle(self,cycle_id, reason, skipCustomListeners=True, skipSubprocesses=True):
        title = self.get_cycle_title(cycle_id)
        print(title)
        return self.camunda.killInstance("demo","demo",title, reason)

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
    executionsize=serializers.DictField()
    executiondata=serializers.DictField()
# class TestCycleSerializer(serializers.Serializer):
#     id = serializers.CharField()
#     title = serializers.CharField()
#     eta_request_ww = serializers.CharField()
#     '''
#     case_complete = serializers.IntegerField()
#     case_wip = serializers.IntegerField()
#     case_notrun = serializers.IntegerField()
#     case_blocked = serializers.IntegerField()
#     '''
#     release = serializers.CharField()
#     plc_milestone = serializers.CharField()
#     milestone_breakdown = serializers.CharField()
#     owner = serializers.CharField()
#     owner_team = serializers.CharField()
#     startTime = serializers.DateTimeField()
#     instance_id = serializers.CharField()

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
        # self.hsdes = HsdEsApi()
        self.camunda = CamundaApi()

    def get_all(self,testcycle_title,page_num =1,page_size = 10):
        try:
            tg=TaskGroup.objects.get(title=testcycle_title)
            tas=Task.objects.filter(group_id=tg.group_id)
        except Exception as e:
            print(e)

        paginator=Paginator(tas,page_size)
        tass=paginator.page(page_num)
        total_page = paginator.num_pages
        result=[]
        for ta in tass:
            result.append({
                'id':ta.task_id,
                'title':ta.task_title,
                'configuration':ta.configuration,
                'status':ta.status,
                'owner':ta.owner,
                'owner_team':tg.team,
                'tcd_id':ta.dsc_id
            })
        dict={
            'result':result,
            'total':total_page
        }

        return dict
        # tc_status_code, tc_data = self.hsdes.getTestCases(testcycle_title)
        # tr_status_code, tr_data = self.hsdes.getTestResult(testcycle_title)
        # print()
        # test_result_df = None
        # if tr_status_code == 200 and tr_data['data']:
        #     test_result_df = pd.DataFrame(tr_data['data'])
        #
        # test_case_df = None
        # if tc_status_code == 200 and tc_data['data']:
        #     test_case_df = pd.DataFrame(tc_data['data'])
        #
        # details = pd.DataFrame(columns=[
        #     'id','title','configuration','status','owner','owner_team','tcd_id'
        # ])
        # if test_case_df is not None:
        #     if test_result_df is not None:
        #         merged = test_case_df.merge(test_result_df, how="left",left_on="id", right_on="parent_id")
        #         print(merged.columns)
        #         details.id = merged.id_x
        #         details.title = merged.title_x
        #         details.configuration = merged["central_firmware.test_case.configuration"]
        #         details.status = merged.status_reason
        #         details.status = details.status.fillna("NotRun")
        #         details.owner = merged.owner_x
        #         details.owner_team = merged['central_firmware.test_case.owner_team']
        #         details.tcd_id = merged.parent_id_x
        #
        # return details.to_dict('records')

    def CompleteAssign(self,title, testcase_id, userid):
        active_tasks = self.camunda.getActiveTasks("demo","demo",title)
        taskid = ""
        for task in active_tasks:
            print(task)
            if task['name'] == "Assignment":
                testid = task['variables'].get("TestCase",{}).get('value','')
                if testid == testcase_id:
                    taskid = task['id']

        self.camunda.completeTask(taskid,{},"demo","demo")


    def Complete(self,title="bios.oakstream_diamondrapids.PSS0.5.Server-BIOS.Update phoenix with Android mobile Demo Mode",testcase_id=15013496220):
        active_tasks = self.camunda.getActiveTasks("demo","demo",title)
        taskid = ""
        for task in active_tasks:
            # print(task)
            if task['name'] == "ConfirmResult":
                testid = task['variables'].get("TestCase",{}).get('value','')
                if testid == testcase_id:
                    taskid = task['id']

        # status_code, data = self.hsdes.getArticle(testcase_id)
        # testcase = data['data'][0]
        # print(testcase)
        testcase=Task.objects.get(task_id=testcase_id)
        tg=TaskGroup.objects.get(title=title)
        result = {
            "title":testcase.task_title,
            "owner":"bfeng1",
            "tc_id":testcase_id,
            "owner_team":tg.team,
            "family":'firmware',
            "release":None,
            "configuration":testcase.configuration,
            "test_cycle":title,
            "status":"complete",
            "reason":"pass",
            "tag":""
        }
        status_code, new_id = self.hsdes.createTestResult(result)
        print(status_code,new_id)
        self.camunda.completeTask(taskid,{},"demo","demo")


    def getTestStepsArray(self,testcase_id):
        # status_code, testcase = self.hsdes.getArticle(testcase_id)
        # print(status_code,testcase)
        # tcd_id = testcase['data'][0]['parent_id']
        # status_code, tcd = self.hsdes.getArticle(tcd_id)
        # print(tcd)
        # test_steps = json.loads(tcd['data'][0]['test_case_definition.test_steps'])
        # for index, step in enumerate(test_steps):
        #     print(index)
        #     step['id'] = index
        ta=Task.objects.get(task_id=testcase_id)
        tcd_id=ta.dsc_id
        print(tcd_id)
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

    def StartExecution(self,title,testcase_id):
        test_steps = self.getTestStepsArray(testcase_id)

        step_str = ["\"" + str(item['id']) + "\"" for item in test_steps]
        print("=======================")
        print(step_str)

        camunda_variable = {
            "variables":{
                "TestCaseSteps":{
                    "type":"Object",
                    "value":"[" + ",".join(step_str) + "]",
                    "valueInfo": {
                        "objectTypeName": "java.util.ArrayList<java.lang.String>",
                        "serializationDataFormat":"application/json"
                    }
                }
            },
            "withVariablesInReturn":True
        }

        active_tasks = self.camunda.getActiveTasks("demo","demo",title)
        taskid = ""
        for task in active_tasks:
            print(task)
            if task['name'] == "ReadExecutionSteps":
                testid = task['variables'].get("TestCase",{}).get('value','')
                print(testid)
                print(testcase_id)
                if testid == testcase_id:
                    taskid = task['id']
                    break

        print(camunda_variable)
        print(taskid)
        print("=======================")

        self.camunda.completeTask(taskid, camunda_variable,"demo","demo")

    def stage(self,cycle_title,testcase_id):
        tasks = self.camunda.getActiveTasks("demo","demo",cycle_title)
        print("888888888888")
        print(cycle_title)
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



class TestStepSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    expected_results = serializers.CharField()
    notes = serializers.CharField()
    active = serializers.BooleanField()
class TestStep():
    def __init__(self):
        # self.hsdes = HsdEsApi()
        self.camunda = CamundaApi()
    def get_all(self,cycle_title, test_case_id,page_size,page_num):
        # status_code, testcase = self.hsdes.getArticle(test_case_id)
        # tcd_id = testcase['data'][0]['parent_id']
        ta=Task.objects.get(task_id=test_case_id)
        tcd_id=ta.dsc_id
        current_step = self.current_step(cycle_title,test_case_id)
        print("00000000000000")
        print(current_step)
        # status_code, tcd = self.hsdes.getArticle(tcd_id)
        # test_steps = json.loads(tcd['data'][0]['test_case_definition.test_steps'])
        # print(test_steps)
        # for index, step in enumerate(test_steps):
        #     if str(index) == current_step:
        #         step['active'] = True
        #     else:
        #         step['active'] = False
        #     step['id'] = index
        tds = TaskDsc.objects.filter(dsc_id=tcd_id)
        paginator = Paginator(tds, page_size)
        # 获取每页商品数据

        page_tds = paginator.page(page_num)

        # 获取列表页总页数
        total_page = paginator.num_pages
        test_steps = []
        for td in page_tds:
            if td.step_id == current_step:
                test_steps.append({
                    'action': td.action,
                    'id': td.step_id,
                    'expected_results': td.expection,
                    'notes': td.notes,
                    'update_by': ta.owner,
                    'update_date': ta.end_time,
                    'result': ta.result,
                    'active':True
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
                    'active': False
                })
            dict={
                'test_steps':test_steps,
                'total':total_page
            }
        return dict

    def current_step(self,cycle_title,testcase_id):
        tasks = self.camunda.getActiveTasks("demo","demo",cycle_title)
        print("888888888888")
        print(cycle_title)
        step = -1
        for task in tasks:
            testid = task['variables'].get("TestCase",{}).get('value','')
            print(type(testid),testid)
            print(type(testcase_id),testcase_id)
            if testid == testcase_id:
                stage = task['name']
                if stage == "Execution":
                    stepid = task['variables'].get("CaseStep",{}).get('value','')
                    print(stepid)
                    step = stepid
                break

        return step


    def complete(self,cycle_title, testcase_id, step_id):
        tasks = self.camunda.getActiveTasks("demo","demo",cycle_title)
        execution_tasks = [task  for task in tasks if task['name'] == "Execution"]
        for task in execution_tasks:
            caseid = task['variables'].get("TestCase",{}).get('value','')
            stepid = task['variables'].get("CaseStep",{}).get('value','')
            print(type(caseid),caseid, type(stepid),stepid)
            print(type(testcase_id),testcase_id, type(step_id),step_id)
            if caseid == testcase_id and str(step_id) == stepid:
                self.camunda.completeTask(task['id'],{},"demo","demo")
                break
        else:
            print("no test step matches!!!", cycle_title,testcase_id,step_id)

        return task['id']

if __name__ == "__main__":
    t_c = TestCycle()
    print(t_c.get_all())
    # t_c = TestStep()
    # print(t_c.get_all())
    # print(t_c.get_details('bios.meteorlake.QS.Client-BIOS.M_BIOS_FV_v340300-corp_23ww40_5'))

    # ts = TestStep()
    # ts.get_all(16016296036)