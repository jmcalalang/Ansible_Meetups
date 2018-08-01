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
        self._validate_certs = module.params.get('validate_certs')


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/transaction/%s' % (self._hostname, self._transactionId)
        self._headers = {
            'Content-Type': 'application/json',
            'X-F5-REST-Coordination-Id': self._transactionId
        }
        self._payload = {
            "state":"VALIDATING"
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
        policyId = ""

        current = self.read()

        if current == self._transactionId:
            return False

        resp = requests.patch(self._uri,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)

        if resp.status_code == 200:
            changed = True
        else:
            res = resp.json()
	    f = open("/tmp/commit.txt","w")
            f.write(str(res) + "\n")
            f.close()


            raise Exception(res['message'])
        return changed


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            transactionId=dict(required=True),
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


