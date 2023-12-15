import logging
from urllib.parse import urljoin,quote, urlencode
from evm_bff.api.common import call_api
import json
from markdownify import markdownify as md

hsdes_base_url = "https://hsdes-api.intel.com/rest/auth/"
hsdes_pre_base_url = "https://hsdes-api-pre.intel.com/rest/auth/"
MAX_RESULTS = 9999
username = "bfeng1"
token = "3104a8e0-ee21-453e-844d-5deed2760555"
logger = logging.getLogger(__name__)

class HsdEsApi():

    def getArticle(self,hsdes_id):
        endpoint = "article/{id}".format(id=hsdes_id)
        url = urljoin(hsdes_base_url,endpoint)
        return call_api(url,username,token)

    def query(self,eql,max_results=MAX_RESULTS):
        query_params = urlencode({'start_at':1,'max_results':max_results})
        endpoint = "query/execution/eql?{}".format(query_params)
        url = urljoin(hsdes_base_url,endpoint)
        return call_api(url,username,token,"POST",data = {'eql':eql})

    def getTestCaseNum(self,cycle_title):
        eql = "SELECT id\
        WHERE tenant = 'central_firmware' AND subject = 'test_case' AND status != 'rejected'\
        AND central_firmware.test_case.test_cycle contains '{}'".format(cycle_title)

        return self.query(eql,max_results=1)

    def getTestCycle(self, hsdes_ids):
        hsdes_ids_str = [str(id) for id in hsdes_ids]
        hsdes_ids_con_str = "id IN (" + ",".join(hsdes_ids_str) + ")"
        eql = "SELECT id,title,status,reason, owner, \
        central_firmware.milestone.release, \
        central_firmware.milestone.owner_team, \
        central_firmware.milestone.submitted_date, \
        central_firmware.milestone.updated_date, \
        central_firmware.milestone.eta_request, \
        central_firmware.milestone.plc_milestone, \
        central_firmware.milestone.milestone_breakdown \
        WHERE tenant = 'central_firmware' AND status != 'rejected'\
        " + "AND " + hsdes_ids_con_str

        return self.query(eql)

    def getTestResult(self,cycle_title):
        eql = "SELECT id,title,status,reason,status_reason,release,release_affected,family,tenant,rev,parent_id, \
        owner,central_firmware.test_result.owner_team, \
        central_firmware.test_result.test_cycle, \
        updated_date,submitted_date,priority,tag,submitted_by,test_result.blocked_date, \
        test_result.closed_date,updated_by,closed_by \
        WHERE tenant = 'central_firmware' AND subject = 'test_result' AND status != 'rejected'\
        AND test_cycle contains '{}'".format(cycle_title)

        return self.query(eql)

    def getTestCases(self,cycle_title):
        eql = "SELECT id,title,status,reason,release,release_affected,family,tenant,rev,parent_id, \
        central_firmware.test_case.configuration, \
        owner, central_firmware.test_case.owner_team, \
        central_firmware.test_case.test_cycle,\
        central_firmware.test_case.trash,\
        central_firmware.test_case.trash_initiated_date,\
        central_firmware.test_case.planned_for,\
        updated_date,submitted_date,closed_date,priority,tag,submitted_by,updated_by,closed_by\
        WHERE tenant = 'central_firmware' AND subject = 'test_case' AND status != 'rejected'\
        AND central_firmware.test_case.test_cycle contains '{}'".format(cycle_title)

        return self.query(eql)

    def getTestSteps(self, tcd_id):
        eql = "SELECT id,title,description,status,reason,component,component_affected,owner,\
        central_firmware.test_case_definition.validation_env,\
        central_firmware.test_case_definition.fw_subcomponent,\
        central_firmware.test_case_definition.release_completed,\
        central_firmware.test_case_definition.processor,\
        central_firmware.test_case_definition.test_category,\
        central_firmware.test_case_definition.test_approach, \
        central_firmware.test_case_definition.domain, \
        release,release_affected,family,tenant,rev,parent_id,updated_date, \
        submitted_date,priority,tag,submitted_by,closed_date,closed_by,updated_by, \
        test_case_definition.test_steps, central_firmware.test_case_definition.pre_condition \
        WHERE tenant = 'central_firmware' AND subject = 'test_case_definition' AND status != 'rejected' \
        AND id={}".format(tcd_id)

        status_code, resp = self.query(eql)
        if status_code == 200:
            steps = json.loads(resp['data'][0]['test_case_definition.test_steps'])
            test_steps=[]
            for step in steps:
                test_steps.append({
                    "action":md(step['action']),
                    "expected_results":md(step.get('expected_results',"")),
                    "notes":md(step.get("note",""))
                })
            
            return 200, test_steps
        else:
            return status_code, {}

    def getTestInstructions(self,tcd_id):
        eql = "SELECT id,title,description,status,reason,component,component_affected,owner,\
        central_firmware.test_case_definition.validation_env,\
        central_firmware.test_case_definition.fw_subcomponent,\
        central_firmware.test_case_definition.release_completed,\
        central_firmware.test_case_definition.processor,\
        central_firmware.test_case_definition.test_category,\
        central_firmware.test_case_definition.test_approach, \
        central_firmware.test_case_definition.domain, \
        release,release_affected,family,tenant,rev,parent_id,updated_date, \
        submitted_date,priority,tag,submitted_by,closed_date,closed_by,updated_by, \
        test_case_definition.test_steps, central_firmware.test_case_definition.pre_condition \
        WHERE tenant = 'central_firmware' AND subject = 'test_case_definition' AND status != 'rejected' \
        AND id={}".format(tcd_id)

        status_code, resp = self.query(eql)
        instructions = {}
        if status_code == 200:
            print(resp)
            test_steps = json.loads(resp['data'][0]['test_case_definition.test_steps'])
            instructions['description'] = md(resp['data'][0]['description'])
            instructions['pre_condition'] = md(resp['data'][0]['central_firmware.test_case_definition.pre_condition'])
            instructions['steps'] = test_steps
            return 200, instructions
        else:
            return status_code, {}


    def createTestResult(self,result):
        payload = {
                "tenant": "central_firmware",
                "subject": "test_result",
                "fieldValues": [
                    {
                        "title": result['title']
                    },
                    {
                        "send_mail": False
                    },
                    {
                        "owner": result['owner']
                    },
                    {
                        "parent_id": result['tc_id']
                    },
                    {
                        "test_result.owner_team": result['owner_team']
                    },
                    {
                        "family": result['family']
                    },
                    {
                        "release": result['release']
                    },
                    {
                        "test_result.configuration": result['configuration']
                    },
                    {
                        "test_result.test_cycle": result['test_cycle']
                    },
                    {
                        "status": result['status']
                    },
                    {
                        "reason": result['reason']
                    },
                    {
                        "tag": result['tag']
                    }
                ]
            }
        endpoint = "article"
        url = urljoin(hsdes_base_url,endpoint)
        print(payload)
        status_code, data = call_api(url,username,token,'POST',payload)
        new_id = None
        if status_code == 200:
            new_id = data['new_id']
        return status_code, new_id

    def updateTestResult(self,tr_id,result):
        payload = {
                "tenant": "central_firmware",
                "subject": "test_result",
                "fieldValues": [
                    {
                        "send_mail": False
                    },
                    {
                        "owner": result['owner']
                    },
                    {
                        "test_result.owner_team": result['owner_team']
                    },
                    {
                        "family": result['family']
                    },
                    {
                        "status": result['status']
                    },
                    {
                        "reason": result['reason']
                    },
                    {
                        "tag": result['tag']
                    }
                ]
            }

        endpoint = "article/{}?fetch=true".format(tr_id)
        url = urljoin(hsdes_pre_base_url,endpoint)

        return call_api(url,username,token,'PUT',payload)

    def dumpTestCycle(self, testcycle_id):
        taskpackage = {}
        status_code, data = self.getTestCycle([testcycle_id])
        testcycle = data['data'][0]
        status_code, data = self.getTestCases(testcycle['title'])
        testcases = data['data']
        configuration_list = list(set([tc['central_firmware.test_case.configuration'] for tc in testcases]))
        taskpackage["id"] = testcycle['id']
        taskpackage["title"] = testcycle['title']
        taskpackage['eta'] = testcycle['central_firmware.milestone.eta_request']
        taskpackage['team'] = testcycle['central_firmware.milestone.owner_team']
        taskpackage['size'] = len(testcases)
        taskpackage['status'] = testcycle['status']
        taskpackage['configuration'] = configuration_list
        taskpackage['owner'] = "someone@intel.com"
        taskpackage['tasklist'] = []
        for tc in testcases:
            parent_id = tc['parent_id']
            status_code, instrus = self.getTestInstructions(parent_id)
            steps = instrus['steps']
            instruction = [{
                "action":md(step['action']),
                "expected_results":md(step.get('expected_results',"")),
                "notes":md(step.get("note",""))
                } for step in steps]

            taskpackage['tasklist'].append(
                {
                    "id":tc['id'],
                    "title":tc['title'],
                    "configuration": tc['central_firmware.test_case.configuration'],
                    "owner":tc['owner'],
                    "status":tc['status'],
                    "description":instrus['description'],
                    "pre_condition":instrus['pre_condition'],
                    "dsc_id": tc['parent_id'],
                    "steps": instruction
                }
            )

        filename = str(testcycle_id) +".json"
        with open(filename,"w") as fw:
            fw.write(json.dumps(taskpackage))


if __name__ == "__main__":
    hsdes = HsdEsApi()
    #status, data = hsdes.getArticle("15014046553")
    #print(data)
    #print(hsdes.getTestCycle([15014046553]))
    #print(hsdes.getTestCases("bios.oakstream_diamondrapids.PSS0.5.Server-BIOS.Update phoenix with Android mobile Demo Mode"))
    #print(hsdes.getTestResult("mobile Demo"))
    print(hsdes.getTestInstructions(1508609551))
    hsdes.dumpTestCycle(15014046553)
    #print(hsdes.getTestSteps(1508609551))
    result = {
        'title':'test code',
        'owner':'bfeng1',
        'tc_id':'1308082906',
        'owner_team':'Others',
        'family':'firmware',
        'release':'bios.alderlake',
        'test_cycle':'bios.alderlake..test team.test1031',
        'tag':'',
        'configuration':'bios.alderlake-test-adl-1022',
        'status':'complete',
        'reason':'pass'
    }
    #code, data = hsdes.updateTestResult(1606133868,result)
    #print(code)
    #print(data)

