#!/usr/bin/python
# -*- coding: utf-8 -*-
#

DOCUMENTATION = '''
'''

EXAMPLES = '''
'''

import socket


try:
    import json
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True


class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
	self._taskId = module.params.get('taskId')
	self._taskType = module.params.get('taskType')
        self._hostname = module.params.get('server')
        self._validate_certs = module.params.get('validate_certs')


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

	self._uri = 'https://%s/mgmt/tm/asm/tasks/%s/%s' % (self._hostname, self._taskType, self._taskId)
        
	self._headers = {
            'Content-Type': 'application/json'
        }

        self._payload = {}


    def run(self):
	taskStatus = ""

        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)


        if resp.status_code == 200:
	    resultat = resp.json()

	    taskStatus = str(resultat['status'])

        else:
            res = resp.json()
            raise Exception(res['message'])
        return taskStatus


def main():
    changed = False

    module = AnsibleModule(
       argument_spec=dict(
            server=dict(required=True),
            taskType=dict(required=True, choices=['export-policy', 'import-policy', 'import-vulnerabilities', 'resolve-vulnerabilities']),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
	    taskId=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )
    )


    obj = BigIpRest(module)

#    if obj.run():
    taskStatus = obj.run()
    if taskStatus != "":
	changed = True
 
    module.exit_json(changed=changed, taskStatus=taskStatus)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()

