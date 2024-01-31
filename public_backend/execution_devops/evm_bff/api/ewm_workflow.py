import datetime

from evm_bff.api.camunda_v2 import CamundaApi
from evm_bff.models import Task, TaskGroup, Usersrigra


class EwmWorkFlow():
    def __init__(self):
        self.camunda = CamundaApi()

    #
    # Task Group
    #

    def start_taskgroup(self, assignee, password, group_id):
        group_instid = self.camunda.startProcess(assignee,password, group_id)

        return group_instid
    
    def getActiveTaskListByAssignee(self, assignee,password, group_id, index=0,pagesize=5):
        task_list = self.camunda.getActiveTasks(assignee,password,group_id,index=0, pagesize=999)

        return task_list

    def getActiveTaskListByGroupId(self, assignee, password, group_id, index = 0, pagesize=9999):
        return self.camunda.getActiveTasks(assignee, password,group_id, index=0,pagesize=9999, user_specific=False)

    def getActiveGroup(self, assignee, password, index=0,pagesize=9999, byAssignee = True):

        processInsts = self.camunda.getProcessInsts(assignee,password,index, pagesize)
        result = []

        for item in processInsts:
            tasks = self.camunda.getActiveTasks(assignee,password,item['businessKey'],index, pagesize, user_specific=byAssignee)
            if tasks:
                result.append(item)

        return result

    
    def getGroupStatusByGroupId(self, assignee, password, group_id, index = 0, pagesize=9999):
        """
        1. get the number of WIP, Block, NotRun
        2. get the total number of tasks.
        """

        processInsts = self.camunda.getProcessInsts(assignee,password, group_id, index, pagesize)

        result = []
        for item in processInsts:
            group_starttime = item['startTime']
            tasks = self.camunda.getActiveTasks(assignee, password,group_id, index=0,pagesize=9999,user_specific=False)
            wip_num = len([task for task in tasks if task['name'] in ('ConfirmResult','Execution')])
            notrun_num = len([task for task in tasks if task['name'] in ('Assignment','ReadExecutionSteps')])
            plan_num = len([task for task in tasks if task['name'] in ('Plan')])
            if plan_num:
                wip_num=0
            result.append(
                {
                    "id":group_id,
                    "startTime":group_starttime,
                    "wip":wip_num,
                    "notrun":notrun_num,
                    "plan":plan_num
                }
            )
        return result

    def getGroupStatusByAssignee(self, assignee, password, index=0, pagesize=9999):
        processInsts = self.camunda.getProcessInsts(assignee,password, index, pagesize)

        result = []
        for item in processInsts:
            group_starttime = item['startTime']
            group_id = item['businessKey']
            tasks = self.camunda.getActiveTasks(assignee, password,group_id,index=0,pagesize=9999)
            if not tasks:
                continue
            wip_num = len([task for task in tasks if task['name'] in ('ConfirmResult','Execution')])
            notrun_num = len([task for task in tasks if task['name'] in ('Assignment','ReadExecutionSteps')])
            plan_num = len([task for task in tasks if task['name'] in ('Plan')])
            if plan_num:
                wip_num=0
            result.append(
                {
                    "id":group_id,
                    "startTime":group_starttime,
                    "wip":wip_num,
                    "notrun":notrun_num,
                    "plan":plan_num
                }
            )

        return result

    def getGroupStatusAll(self, assignee, password,index=0, pagesize=9999):
        processInsts = self.camunda.getProcessInsts(assignee,password,index,pagesize)

        result = []
        for item in processInsts:
            group_starttime = item['startTime']
            group_id = item['businessKey']
            tasks = self.camunda.getActiveTasks(assignee, password,group_id, index=0, pagesize=9999,user_specific=False)
            if not tasks:
                continue
            wip_num = len([task for task in tasks if task['name'] in ('ConfirmResult','Execution')])
            notrun_num = len([task for task in tasks if task['name'] in ('Assignment','ReadExecutionSteps')])
            plan_num = len([task for task in tasks if task['name'] in ('Plan')])
            if plan_num:
                wip_num=0
            result.append(
                {
                    "id":group_id,
                    "startTime":group_starttime,
                    "wip":wip_num,
                    "notrun":notrun_num,
                    "plan":plan_num
                }
            )

        return result

    #
    # Task
    #

    def getActiveTaskListByName(self, assignee, password, group_id, task_name, index, pagesize, byAssignee=True):
        activetasks = self.camunda.getActiveTasks(assignee,password,group_id, index, pagesize, byAssignee)
        result = [task for task in activetasks if task['name'] == task_name]

        return result


    def completePlanTask(self,assignee, password, group_id,taskidlist):
        """
        1. build the payload based on the tasklist
        2. get Plan task inst id
        3. call self.camunda.completeTask
        """
        status = 0
        payload = {}

        tc_ids = ["\"" + str(item) + "\"" for item in taskidlist]

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

        plan_task = None
        tasks = self.camunda.getActiveTasks(assignee,password,group_id)
        taskInstid = ""
        for task in tasks:
            if task['name'] == "Plan":
                taskInstid = task['id']
                plan_task = task
                break
        if taskInstid:
            self.camunda.completeTask(assignee, password, taskInstid,payload)

        return [plan_task] if plan_task else plan_task


    def assignTask(self, assigner, password, group_id, task_id, assignee):
        """
        1. get task instance based on the taskid
        2. assign assigneee to task instance
        """

        activeTasks = self.camunda.getActiveTasks(assigner,password,group_id, user_specific=True)
        assignTasks = [task for task in activeTasks if task['name']== "Assignment"]

        task_affected = None
        for task in assignTasks:
            if task['variable']['TestCase']['value'] == task_id:
                self.camunda.TaskAssign(assigner, password,task['id'], assignee)
                task_affected = task
                break

        return task_affected

    def completeAssignTask(self, assigner, password, task_inst_id, assignee):
        """
        1. call assignTask(taskid, assignee)
        2. call self.camunda.completeTask
        """

        payload = {
            "variables":{
                "Executor":{
                    "type":"String",
                    "value":assignee,
                }
            },
            "withVariablesInReturn":True
        }
        #self.camunda.setVariable(assignee, password, group_id, assigned_task[id],  "result","complete")
        self.camunda.completeTask(assigner,password,task_inst_id,payload)

        return task_inst_id

    def completeReadExecutionSteps(self, assignee, password, group_id, taskid, tasksteplist):
        """
        1. get task instance by taskid
        2. build payload
        3. call self.camunda.completeTask
        """
        task_inst_id = None
        active_tasks = self.camunda.getActiveTasks(assignee, password, group_id, user_specific=True)
        read_task = None
        for task in active_tasks:
            print(task['name'], task['assignee'], task['variables'])
            if task['name'] == "ReadExecutionSteps" and task['variables']['TestCase']['value'] == taskid:
                task_inst_id = task['id']
                read_task = task
                break
        else:
            return None
        
        step_str = ["\"" + str(item['id']) + "\"" for item in tasksteplist]

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
        
        #self.camunda.setVariable(assignee, password, group_id, task_inst_id,  "result","complete")
        data = self.camunda.completeTask(assignee,password, task_inst_id, camunda_variable)
        if data is None:
            print("complete task failed")

        return read_task
    #
    # Steps
    #
    def completeExecutionStep(self, assignee, password, group_id, taskid, result):
        """
        1. get task instance by stepid
        2. call self.camunda.completeTask
        """

        task_inst_id = None
        active_tasks = self.camunda.getActiveTasks(assignee, password, group_id, user_specific=True)
        exe_task = None
        for task in active_tasks:
            if task['name'] == "Execution" and task['variables']['TestCase']['value'] == taskid:
                task_inst_id = task['id']
                exe_task = task
                break
        else:
            print("no active execution task")
            return None

        #self.camunda.setVariable(assignee, password, group_id, task_inst_id,  "result",result)
        status_code = self.camunda.completeTask(assignee, password, task_inst_id, {})
        if status_code not in (204,200):
            print("complete task failed")

        return exe_task

    def stepPass(self,assignee,password,group_id, taskid):
        return self.completeExecutionStep(assignee, password, group_id, taskid, "pass")

    def stepFail(self,assignee,password,group_id, taskid) :
        affected_task = self.completeExecutionStep(assignee, password, group_id, taskid, "fail")
        self.ignoreLeftTasks(assignee, password,group_id,taskid)
        return affected_task

    def stepBlock(self,assignee,password,group_id, taskid):
        affected_task = self.completeExecutionStep(assignee, password, group_id, taskid,  "block")
        self.ignoreLeftTasks(assignee, password,group_id,taskid)
        return affected_task

    def stepIgnore(self,assignee,password,group_id, taskid):
        return self.completeExecutionStep(assignee, password, group_id, taskid, "ignore")

    def ignoreLeftTasks(self, assignee, password, group_id, taskid):
        task_inst_id = None
        exe_task = self.camunda.getActiveTasks(assignee, password, group_id, user_specific=True)

        ignored_tasks = []
        payload = {
            "variables":{
                "result":{
                    "type":"String",
                    "value":"ignore",
                }
            },
            "withVariablesInReturn":True
        }

        while True:
            for task in exe_task:
                if task['name'] == "Execution" and task['variables']['TestCase']['value'] == taskid:
                    task_inst_id = task['id']
                    ignored_tasks.append(task)
                    break
            else:
                break

            self.camunda.completeTask(assignee, password, task_inst_id, payload)
            exe_task = self.camunda.getActiveTasks(assignee, password, group_id, user_specific=True)

        return ignored_tasks

    def completeConfirmResult(self, assignee, password, group_id, taskid, restart=False):
        """
        1. get task instance by task name "ConfirmResult"
        2. call self.camunda.completeTask
        """
        task_inst_id = None
        active_tasks = self.camunda.getActiveTasks(assignee, password, group_id, user_specific=True)
        result_task = None
        for task in active_tasks:
            if task['name'] == "ConfirmResult" and task['variables']['TestCase']['value'] == taskid:
                task_inst_id = task['id']
                result_task = task
                break
        else:
            return None

        payload = {}
        if restart:
            payload = {
                "variables":{
                "restart":{
                    "type":"String",
                    "value":"true"
                    }
                },
                "withVariablesInReturn":True
            }
        else:
            payload = {
                "variables":{
                "restart":{
                    "type":"String",
                    "value":"false"
                    }
                },
                "withVariablesInReturn":True
            }


        print(payload)
        #self.camunda.setVariable(assignee, password, group_id, task_inst_id,  "result","complete")
        data = self.camunda.completeTask(assignee, password, task_inst_id, payload)
        print(data)

        if data is None:
            print("complete task failed")

        return result_task
    
    def getTaskDuration(self, assignee, password, assignmentExecutionId, resultconfirmExecutionId):
        """
        1. getPlanTaskStartTime
        2. getConfirmResultEndTime
        3. duration = ConfirmResultEndTime - getPlanTaskStartTime
        """
        assign_hist = self.camunda.getTaskhistory(assignee, password, assignmentExecutionId)
        taskstart_time = assign_hist[0]['startTime']
        result_hist = self.camunda.getTaskhistory(assignee, password, resultconfirmExecutionId)
        taskend_time = result_hist[0]['endTime']

        return taskstart_time, taskend_time

    def getTaskStepDuration(self, assignee, password, task_inst_id):
        hist = self.camunda.getTaskhistory(assignee, password, task_inst_id)
        taskstart_time = hist[0]['startTime']
        taskend_time = hist[0]['endTime']
        return taskstart_time, taskend_time


class DBApi():
    pass

class uiapi():
    def __init__(self):
        self.db = DBApi()
        self.ewm = EwmWorkFlow()
        today = datetime.date.today()
        self.now = datetime.datetime.now()
        self.todayzero_time = datetime.datetime(today.year, today.month, today.day)
        self.this_month_startdaytime = datetime.datetime(today.year, today.month, 1)
        delta = datetime.timedelta(days=1)
        self.yestdaytimeold = self.todayzero_time - delta
        self.yestdaytime = self.yestdaytimeold.replace(tzinfo=datetime.timezone.utc)

    # Home page
    def getCompleteAccumulationByUser(self, assignee):
        "select count(*) from Tasktable where assignee = $assignee and start_time>$start and end_time<$end"

        yestdayComplete=Task.objects.filter(owner=assignee, start_time__gte=self.yestdaytime, end_time__lte=
        self.todayzero_time,status="Completed").count()
        monthComplete=Task.objects.filter(owner=assignee, start_time__gte=self.this_month_startdaytime, end_time__lte=
        self.now,status="Completed").count()
        result={
            'yestdayComplete':yestdayComplete,
            'monthComplete':monthComplete
        }
        return result
    def getNewAssignment(self,taskgroupid, assignee,start):
        """
        1. call camunda api historic_task with parameter
           1) taskAssignee
           2) taskname = "ReadExecutionSteps"
           3) businessKey
        2. cache the newassignment into db
        3. get number from db in next time call
        """

        todayNewAssignment=Task.objects.filter(group_id=taskgroupid, owner=assignee,
                        start_time__gte=self.todayzero_time).count()
        return todayNewAssignment

    def getUnAssigned(self, taskgroupid,assignee):
        """
        1. call camunda api task with parameter
            1) taskname = "Assignment"
            2) businessKey
        """
        assigneedto_me=Task.objects.filter(group_id=taskgroupid, owner=assignee).count()
        unassignee=Task.objects.filter(group_id=taskgroupid,status='Assignment').count()
        completed=Task.objects.filter(group_id=taskgroupid,status='Completed',owner=assignee).count()
        result={
            'assigneedto_me':assigneedto_me,
            'unassignee':unassignee,
            'completed':completed
        }
        return result

    def getCompleted(self,assignee):
        monthruninggroup=TaskGroup.objects.filter(status='AssignmentCompleted',start_time__gte=self.this_month_startdaytime).count()
        monthcompletedgroup=TaskGroup.objects.filter(status='Completed',start_time__gte=self.this_month_startdaytime).count()
        monthruningtask=Task.objects.filter(owner=assignee,status__in=['ReadExecutionSteps','Execution','ConfirmResult'],
                                            start_time__gt=self.this_month_startdaytime).count()
        monthcompletedtask=Task.objects.filter(owner=assignee,status='Completed',start_time__gte=self.this_month_startdaytime).count()
        runinggroup=TaskGroup.objects.filter(status='AssignmentCompleted',).count()
        completedgroup=TaskGroup.objects.filter(status='Completed',).count()
        runingtask=Task.objects.filter(owner=assignee,status__in=['ReadExecutionSteps','Execution','ConfirmResult'],).count()
        completedtask=Task.objects.filter(owner=assignee,status='Completed',).count()
        return monthruninggroup, monthcompletedgroup, monthruningtask, monthcompletedtask,runinggroup,completedgroup,runingtask,completedtask

    def getexecutiondetails(self,tg):
        data=[]
        date=[]
        begeningtime = datetime.date(tg.start_time.year, tg.start_time.month, tg.start_time.day)
        print(begeningtime)
        totledata = Task.objects.exclude(group_id=tg.group_id,status='Assignment').count()
        data.append(totledata)
        for i in range(0,14):
            executiondata=Task.objects.filter(status='Completed',end_time__gte=begeningtime,
                                              end_time__lte=begeningtime+datetime.timedelta(days=1)).count()
            totledata=totledata - executiondata
            if begeningtime <= datetime.date.today():
                data.append(totledata)
            date.append(begeningtime)
            begeningtime = begeningtime + datetime.timedelta(days=1)
        return data, date


    # Execution
    def getuserexcutor(self):
        users=Usersrigra.objects.all()
        result=[]
        for user in users:
            result.append(user.username)
        return result
    def getActiveTaskGroup(self):
        """
        1. call camunda api processinstance
        """

    def getActiveTask(self):
        """
        1. call camunda api task with:
        2. order the taks list within 3 boxes
            1) WIP: taskname in ["Execution","ConfirmResult"]
            2) NotRun: taskname in ["ReadExecutionSteps"]
        3. get complete task list
            select  count(*) from flow where assigee = $assignee and group_id = $group_id and status != NULL
        """

    def getActiveTaskStep(self):
        """
        1. call camunda api task with:
            1) taskname = "Execution"
        2. filter the tasks with variable testcase
        3. get the variable of teststep
        4. get all task steps from DB
        5. marked the current taskstep as current
        """

    def startExecution(self):
        """
        1. call completeReadExecutionSteps api
        """

    def submitResult(self):
        """
        1. call completeConfirmResult api
        """

    #Assignment
    def assignTasks(self, team, method):
        """
        1. design method is random
        2. implement a random assignment algorithm
        3. call camunda api to assign assignee
        """
    def getAssignment(self,taskgroup_id):
        """
        1. call camunda api task with:
            1) process instance id
        2. get variable testcase from each task

        return tasklist as
        [[taskid, tasktitle, assignee, taskinst_id],]
        """

    def adjustAssignment(self,taskinstid, assignee):
        """
        call camunda api
        """

    # Progress
    def getburndownchart(self):
        """
        return completetasks, current date, est deadline
        """

    # User Profile