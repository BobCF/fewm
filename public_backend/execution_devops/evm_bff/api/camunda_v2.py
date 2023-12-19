from evm_bff.api.common import call_api,generate_url
from urllib.parse import urlencode, urljoin, quote

## Camunda Configuration
Config = {
    #"base_url": "https://camunda.k8s-bios.intel.com/engine-rest/",
    #"base_url": "http://localhost:8080/engine-rest/",
    "base_url": "http://172.17.0.2:8080/engine-rest/",
    "process_key": "FivValidation"
}

class CamundaApi():

    def getProcessDefId(self, user_name, password):
        endpoint = "process-definition"
        url = urljoin(Config['base_url'],endpoint)
        params = {
            "latestVersion": "true",
        }

        # Generate the complete URL using the generate_url function
        complete_url = generate_url(url, params)
        status_code , data = call_api(
            complete_url,
            user_name,
            password
        )

        if status_code == 200:
            process = [item for item in data if item['key'] == Config["process_key"]]
            processdef = process[0]
            return processdef['id']
        else:
            return None

    def startProcess(self,user_name, password,businesskey):
        process_endpoint = "process-definition"
        process_ins_id = self.getProcessDefId(user_name, password)
        complete_url = urljoin(Config['base_url'],quote("{endpoint}/{id}/start".format(endpoint=process_endpoint,id=process_ins_id)))
        payload = {
            "variables": {
                "ExecutionLead": {
                "value": user_name,
                "type": "String"
                }
            },
            "businessKey": businesskey
        }
        status_code, data = call_api(
            complete_url,
            user_name,
            password,
            method = "POST",
            data = payload
        )

        if status_code == 200:
            return data['id']
        else:
            print("start process failed", status_code)
            return None

    def getInstanceId(self,user_name,password,businessKey):
        process_endpoint = "process-instance"
        complete_url = generate_url(urljoin(Config['base_url'],process_endpoint), {"businessKey":businessKey})
        print(complete_url)

        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )
        instId = ""
        if status_code == 200:
            for item in data:
                if item['businessKey'] == businessKey:
                    instId = item['id']
                    break
        return instId

    def killInstance(self, user_name, password, businessKey, reason, skipCustomListeners=True, skipSubprocesses=True):
        process_endpoint = "process-instance/delete"
        instance_id = self.getInstanceId(user_name, password, businessKey)
        complete_url =urljoin(Config['base_url'],process_endpoint)
        status_code, data = call_api(
            complete_url,
            user_name,
            password,
            method = "POST",
            data = {
                "deleteReason": reason,
                "processInstanceIds":[instance_id],
                "skipCustomListeners":skipCustomListeners,
                "skipSubprocesses": skipSubprocesses
            }
        )

        return status_code, data

    def getProcessInsts(self, user_name, password, index=0, pagesize=9999, group_id=None):
        process_ins_endpoint = "process-instance"
        processDefId = self.getProcessDefId(user_name,password)

        params = {
            "processDefinitionId":processDefId, 
            "sortBy":"businessKey",
            "sortOrder":"desc",
            "firstResult":index,
            "maxResults":pagesize,
            }

        print(user_name, password, index, pagesize)

        complete_url = generate_url(urljoin(Config['base_url'],process_ins_endpoint), params)
        print(complete_url)
        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )
        pInsts = []
        if status_code == 200:
            for inst in data:
                if group_id and inst['businessKey'] != group_id:
                    continue
                state = self.getProcessState(user_name,password,inst['id'])
                pInsts.append({
                    "instance_id": inst["id"],
                    "businessKey": inst["businessKey"],
                    "startTime": state[0]['startTime']
                })

        return pInsts

    def getProcessState(self,user_name, password, processInsId):
        endpoint = "history/process-instance"
        url = urljoin(Config['base_url'],endpoint)
        params = {
            "processInstanceId": processInsId,
        }

        # Generate the complete URL using the generate_url function
        complete_url = generate_url(url, params)
        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )
        if status_code == 200:
            return data
        else:
            return {}

    def getProcessVariable(self,user_name, password,processInsId, variablename):
        endpoint = "process-instance"
        complete_url = urljoin(Config['base_url'],quote("{endpoint}/{id}/variables/{variable_name}".format(endpoint=endpoint,id=processInsId,variable_name=variablename)))

        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )
        print(complete_url)
        if status_code == 200:
            return data
        else:
            return None


    def getActiveTasks(self, user_name, password,businessKey, index=0, pagesize=9999, user_specific=True):
        task_endpoint = "task"

        #processInsId = self.getInstanceId(user_name, password,businessKey)

        params = {
            "sortBy":"executionId",
            "sortOrder":"desc",
            "firstResult":index,
            "maxResults":pagesize,
            "processInstanceBusinessKey": businessKey,
        }

        if user_specific:
            params['assignee'] = user_name

        complete_url = generate_url( 
            urljoin(
                Config["base_url"],
                task_endpoint
            ), 
            params
        )
        print(complete_url)
        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )

        if status_code == 200:
            for task in data:
                task_variables = self.getTaskVariables(user_name,password, task['id'])
                task['variables'] = task_variables
            return data
        else:
            return []

    def getTaskVariables(self,user_name, password, task_id):
        endpoint = "task"

        complete_url = urljoin(
                Config["base_url"],
                quote("{endpoint}/{id}/variables".format(endpoint=endpoint,id=task_id))
            ) 

        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )

        if status_code == 200:
            return data
        else:
            return None

    def completeTask(self,user_name, password, task_instid, payload):
        endpoint = "task"
        method = "POST"
        
        complete_url = urljoin(Config["base_url"], quote("{endpoint}/{id}/complete".format(endpoint=endpoint,id=task_instid)))

        print(complete_url)
        status_code, data = call_api(complete_url,user_name,password, method=method,data=payload)
        print(data)
        
        return status_code

    def TaskAssign(self,assigner, password, task_instid, assignee):
        endpoint = "task/"
        method = "POST"
        complete_url = urljoin(Config['base_url'],endpoint)

        complete_url = urljoin(complete_url, quote("{id}/assignee".format(id=task_instid)))

        payload = {
            "userId": assignee
        }

        print(complete_url)
        status_code, data = call_api(complete_url,assigner,password, method=method,data=payload)

        if status_code == 200:
            return data
        
        return None

    def getTaskhistory(self, assignee, password, task_inst_id):
        endpoint = "history/task/"
        method = "GET"

        complete_url = urljoin(Config["base_url"],endpoint)
        complete_url = generate_url(complete_url,{"taskId":task_inst_id})

        status_code, data = call_api(complete_url,assignee, password, method =method)
        if status_code == 200:
            return data

        return None

    def addUser(self,assignee, password, user_info):
        endpoint = "user/create"
        method = "POST"
        payload = {
            "profile": {
                "id": user_info['idsid'],
                "firstName": user_info['firstname'],
                "lastName": user_info['lastname'],
                "email":user_info["email"]
            },
            "credentials": {
                "password": user_info['password']
            }
        }

        compile_url = urljoin(Config['base_url'], endpoint)

        status_code, data = call_api(compile_url, assignee, password, method = method, data = payload)
        return status_code

if __name__ == "__main__":
    camunda = CamundaApi()
    instances = camunda.getProcessInsts("demo","demo")
    print(instances)