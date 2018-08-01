#!/usr/bin/python
# -*- coding: utf-8 -*-
#


DOCUMENTATION = '''
---

'''

EXAMPLES = '''


'''

import socket
from ansible.module_utils.basic import env_fallback

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
        self._transactionId = module.params.get('transactionId')
        self._partition = module.params.get('partition')
        self._name = module.params.get('name')
        self._description = module.params.get('description')
        self._hasParent = module.params.get('hasParent')
        self._virtual = module.params.get('virtual')
        self._parentPolicyName = module.params.get('parentPolicyName')
		self._policyTemplate = module.params.get('policyTemplate')
        self._appLang = module.params.get('lang')
        self._enforceMode = module.params.get('enforcementMode')
        self._validate_certs = module.params.get('validate_certs')
		self._virtualServers = ["/" + self._partition + "/" + self._virtual]

class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/asm/policies' % (self._hostname)

        self._headers = {'Content-Type': 'application/json', 'X-F5-REST-Coordination-Id': self._transactionId}

	if self._hasParent == 'false':
		self._payload = {
	            	"name": self._name, 
            		"description": self._description,
            		"partition": self._partition,
            		"hasParent": self._hasParent,
	    			"templateReference": self._policyTemplate,
	    			"virtualServers": self._virtualServers, 
            		"applicationLanguage": self._appLang,
            		"enforcementMode": self._enforceMode
        	}
	else:
		self._payload = {
	            	"name": self._name, 
             		"description": self._description,
            		"partition": self._partition,
            		"hasParent": self._hasParent,
	    			"parentPolicyName": self._parentPolicyName,
	    			"virtualServers": self._virtualServers, 
            		"applicationLanguage": self._appLang,
            		"enforcementMode": self._enforceMode
        	}

    def read(self):
        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return {}
        else:
            return resp.json() #['name']

    def run(self):
        changed = False
        current = self.read()

        if current == self._name:
            return False

        resp = requests.post(self._uri,
                            headers=self._headers,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)


        if resp.status_code == 200:
	    changed = True
        else:
	    res = resp.json()
	    #raise Exception(res['message'])
	    changed = False
        return changed



def main():
    changed = False

    module = AnsibleModule(
       argument_spec=dict(
            server=dict(
		    required=True,
	    	    aliases=['hostname'],
	    	    fallback=(env_fallback, ['F5_SERVER'])
	           ),
            transactionId=dict(default=''),
            partition=dict(
		    	default='Common',
                 	fallback=(env_fallback, ['F5_PARTITION'])
	    		),
            name=dict(required=True),
            description=dict(default=''),
	    virtual=dict(required=True),
	    hasParent=dict(default='false'),
	    parentPolicyName=dict(default=''),
	    policyTemplate=dict(default=''),
	    caseInsensitive=dict(default='false', type='bool'),
            lang=dict(default='utf-8', choices=['utf-8', 'western']),
            enforcementMode=dict(default='blocking', choices=['blocking', 'transparent']),
            user=dict(
		    required=True, 
		    aliases=['username'],
	    	    fallback=(env_fallback, ['F5_USER'])
	    	),
            password=dict(
		    required=True,
	            aliases=['passwd'],
	            fallback=(env_fallback, ['F5_PASSWORD'])
                    ),
            validate_certs=dict(
		    default='no',
		    type='bool',
	    	    fallback=(env_fallback, ['F5_VALIDATE_CERTS'])
	    )
        )
)

    obj = BigIpRest(module)


    asmpolicy = obj.run()
    if asmpolicy:
        changed = True
 
    module.exit_json(changed=changed, policy=asmpolicy)



from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()


