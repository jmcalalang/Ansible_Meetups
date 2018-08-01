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
        self._policyId = module.params.get("policyId")
	self._entity = module.params.get("entity")
        self._validate_certs = module.params.get('validate_certs')


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/asm/policies/%s/%s' % (self._hostname, self._policyId, self._entity)
        self._headers = {
            'Content-Type': 'application/json',
        }
        self._payload = {
        }

    def getWildcardId(self):
	entityId = ""
        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)
        
	if resp.status_code == 200:
        	res = resp.json()
		for entities in res["items"]:
			if ( entities["name"] == "*" ):
				entityId = entities["id"]		
            
            	return entityId
        else:
            return resp.json() #['name']	


    def run(self):
        changed = False
        current = self.getWildcardId()

        if current == "":
            return False
	
	rmURI = 'https://%s/mgmt/tm/asm/policies/%s/%s/%s' % (self._hostname, self._policyId, self._entity, current)
	
        resp = requests.delete(rmURI,
			    headers=self._headers,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)


        if resp.status_code == 201:
            changed = True
        else:
            res = resp.json()
            raise Exception(res['message'])
        return changed


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            validate_certs=dict(default='no', type='bool'),
            password=dict(required=True),
            user=dict(required=True, aliases=['username']),
            policyId=dict(required=True),
	    entity=dict(required=True, choices=['urls', 'filetypes', 'parameters'])
        )
    )


    obj = BigIpRest(module)

    if obj.run():
        changed = True
    
    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()


