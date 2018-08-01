#!/usr/bin/python
# -*- coding: utf-8 -*-
#


DOCUMENTATION = '''
---

'''

EXAMPLES = '''
      - name: Create SSL Profile
        f5_sslProfile:
            server: "{{ inventory_hostname }}"
            transactionId: "{{transId.transId}}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            name: "{{appName}}_SSLProfile"
            side: "client"
            parent: "client-ssl"
            cert: "{{ cert.certName }}"
            key: "{{ key.keyName }}"
        delegate_to: localhost
        register: result

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
	self._parent = module.params.get('parent')
        self._name = module.params.get('name')
        self._side = module.params.get('side')
        self._cert = module.params.get('cert')
        self._key = module.params.get('key')





class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

	self._uri = 'https://%s/mgmt/tm/ltm/profile/%s-ssl' % (self._hostname, self._side)

        self._headers = {
            'Content-Type': 'application/json',
            'X-F5-REST-Coordination-Id': self._transactionId
        }

        self._payload = {
            "name": self._name,
            "cert": self._cert,
            "key": self._key,
            "defaultsFrom": self._parent 
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
	    	changed = False
        return changed


def main():
    changed = False


    module = AnsibleModule(
       argument_spec=dict(
            server=dict(required=True),
            transactionId=dict(default=''),
            partition=dict(default='Common'),
            name=dict(required=True),
            side=dict(required=True, choices=['client', 'server']),
	    parent=dict(required=True),
            cert=dict(required=True),
            key=dict(required=True),
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
