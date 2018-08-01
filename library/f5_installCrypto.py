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
        self._fileName = module.params.get('fileName')
        self._fileType = module.params.get('fileType')
        self._validate_certs = module.params.get('validate_certs')

class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/sys/crypto/%s' % (self._hostname, self._fileType)

        self._headers = {'Content-Type': 'application/json'}
        
	self._payload = {
	    'command': 'install',
            'name': self._serviceName, 
            'from-local-file': '/var/config/rest/downloads/' + self._fileName 
        }


    def run(self):
        changed = False

        resp = requests.post(self._uri,
                            headers=self._headers,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)



        if resp.status_code == 200:
	    changed = True
	    resultat = resp.json()
        else:
	    res = resp.json()
	    raise Exception(res['message'])
	    changed = False
        return changed



def main():
    changed = False

    module = AnsibleModule(
       argument_spec=dict(
            server=dict(required=True),
            serviceName=dict(required=True),
            fileName=dict(default=''),
	    fileType=dict(required=True, choices=['key', 'cert']),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )

    )


    obj = BigIpRest(module)


    if obj.run():
	    changed = True
 
    module.exit_json(changed=changed)



from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()


