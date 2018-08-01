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
        self._validate_certs = module.params.get('validate_certs')
        self._transactionId = module.params.get('transactionId')
        self._partition = module.params.get('partition')
        self._virtual = module.params.get('virtual')
        self._name = module.params.get('name')
        self._context = module.params.get('context')


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/ltm/virtual/~%s~%s/profiles' % (self._hostname, self._partition, self._virtual)

        self._headers = {
            'Content-Type': 'application/json',
            'X-F5-REST-Coordination-Id': self._transactionId
        }
        self._payload = {
            "name": self._name,
            "context": self._context
        }

    def read(self):
        resp = requests.get(self._uri,
                            headers=self._headers,
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
            raise Exception(res['message'])
	    #changed = False
        return changed


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            transactionId=dict(required=True),
            partition=dict(default='Common'),
            virtual=dict(required=True),
            name=dict(required=True),
            context=dict(default='all', choices=['clientside', 'serverside', 'all']),
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


