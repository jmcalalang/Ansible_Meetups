
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
        self._transactionId = module.params.get('transactionId')
        self._partition = module.params.get('partition')
        self._pool = module.params.get('pool')
        self._name = module.params.get("name")
        self._address = module.params.get("address")
        self._port = module.params.get('port')
        self._validate_certs = module.params.get('validate_certs')


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/ltm/pool/~%s~%s/members' % (self._hostname, self._partition, self._pool)
        self._headers = {
            'Content-Type': 'application/json',
		'X-F5-REST-Coordination-Id': self._transactionId
        }
        self._payload = {
            "name": self._name + ':' +self._port,
            "address": self._address
        }

    def read(self):
        resp = requests.get(self._uri,
                            headers=self._headers,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return False
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
           # raise Exception(res['message'])
	    changed = False
        return changed


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            transactionId=dict(required=True),
	        partition=dict(default='Common'),
            pool=dict(required=True),
	        name=dict(required=True),
            address=dict(required=True),
            port=dict(required=True),
            password=dict(required=True),
            user=dict(required=True, aliases=['username']),
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



