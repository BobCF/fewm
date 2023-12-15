from evm_bff.api.common import call_api,generate_url
from urllib.parse import urlencode, urljoin, quote

## Camunda Configuration
Config = {
    "base_url": "https://camunda.k8s-bios.intel.com/engine-rest/",
    "process_key": "FivValidation",
    "username":"demo",
    "token":"demo"
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

    def startProcess(self,user_name, password,businesskey,variables):
        process_endpoint = "process-definition"
        process_ins_id = self.getProcessDefId(user_name, password)
        complete_url = urljoin(Config['base_url'],quote("{endpoint}/{id}/start".format(endpoint=process_endpoint,id=process_ins_id)))
        status_code, data = call_api(
            complete_url,
            user_name,
            password,
            method = "POST",
            data = {
                "variables": {
                    "testcycle_id": {
                    "value": variables,
                    "type": "String"
                    }
                },
                "businessKey": businesskey
                }
        )

        if status_code == 200:
            return data['id']
        else:
            print("start process failed", status_code)
            return None

    def getInstanceId(self,user_name,password,businessKey):
        process_endpoint = "process-instance"
        complete_url = generate_url(urljoin(Config['base_url'],process_endpoint), {"businesskey":businessKey})
        print(complete_url)

        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )
        instId = ""
        print(data)
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

    def getProcessInsts(self, user_name, password):
        process_ins_endpoint = "process-instance"
        processDefId = self.getProcessDefId(user_name,password)

        complete_url = generate_url(urljoin(Config['base_url'],process_ins_endpoint), {"processDefinitionId":processDefId})
        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )
        pInsts = []
        if status_code == 200:
            for inst in data:
                var = self.getProcessVariable(user_name, password, inst['id'],'testcycle_id')
                state = self.getProcessState(user_name,password,inst['id'])
                pInsts.append({
                    "instance_id": inst["id"],
                    "businessKey": inst["businessKey"],
                    "testcycle_id": var['value'],
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
        print(status_code,data)
        if status_code == 200:
            return data
        else:
            return None



    def getActivities(self, user_name, password):
        process_ins_endpoint = "process-instance"

        processIns = self.getProcessInst(user_name,password)
        if processIns:
            processInsId = processIns["id"]
        else:
            print("Can't get Process Instance")
            return None
            
        complete_url = generate_url( 
            urljoin(
                Config["base_url"],
                quote("{endpoint}/{id}/activity-instances".format(endpoint=process_ins_endpoint,id=processInsId))
            ), 
            {"businessKey":self.business_key}
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

    def getActiveTasks(self, user_name, password,businessKey, user_specific=True):
        task_endpoint = "task"

        processInsId = self.getInstanceId(user_name, password,businessKey)

        complete_url = generate_url( 
            urljoin(
                Config["base_url"],
                task_endpoint
            ), 
            {"processInstanceId": processInsId,
             "assignee":user_name
             } if user_specific else {"processInstanceId": processInsId}

        )

        status_code, data = call_api(
            complete_url,
            user_name,
            password
        )

        if status_code == 200:
            for task in data:
                task_variables = self.getTaskVariables(task['id'],user_name,password)
                task['variables'] = task_variables
            return data
        else:
            return None

    def getTaskVariables(self,task_id, user_name, password):
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

    def completeTask(self,taskid, payload, user_name, password):
        endpoint = "task"
        method = "POST"
        
        complete_url = urljoin(Config["base_url"], quote("{endpoint}/{id}/complete".format(endpoint=endpoint,id=taskid)))

        print(complete_url)
        status_code, data = call_api(complete_url,user_name,password, method=method,data=payload)

        if status_code in (204,200):
            return data
        
        return None

if __name__ == "__main__":
    camunda = CamundaApi()
    instances = camunda.getProcessInsts("demo","demo")
    print(instances)