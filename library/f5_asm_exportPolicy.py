#!/usr/bin/python
# -*- coding: utf-8 -*-
#


DOCUMENTATION = '''
---

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
        self._hostname = module.params.get('server')
        self._serviceName = module.params.get('serviceName')
        self._policyId = module.params.get('policyId')
        self._validate_certs = module.params.get('validate_certs')

class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/asm/tasks/export-policy' % (self._hostname)

        self._headers = {'Content-Type': 'application/json'}
        
	self._payload = {
            'filename': self._serviceName + '.xml', 
            'policyReference': { 'link': 'https://localhost/mgmt/tm/asm/policies/' + self._policyId }
        }


    def run(self):
        changed = False
        exportTask = ""

        resp = requests.post(self._uri,
                            headers=self._headers,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)



        if resp.status_code == 201:
	    changed = True
	    resultat = resp.json()
	    exportTask = resultat['id']

        else:
	    res = resp.json()
	    raise Exception(res['message'])
	    changed = False

        return exportTask



def main():
    changed = False

    module = AnsibleModule(
       argument_spec=dict(
            server=dict(required=True),
            serviceName=dict(required=True),
            policyId=dict(default=''),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )

    )


    obj = BigIpRest(module)


    exportTask=obj.run()
    if exportTask != "":
	    changed = True
 
    module.exit_json(changed=changed,exportTask=exportTask)



from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()


