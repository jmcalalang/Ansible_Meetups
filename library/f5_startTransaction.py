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
        self._hostname = module.params.get('server')
        self._validate_certs = module.params.get('validate_certs')


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

	self._uri = 'https://%s/mgmt/tm/transaction' % (self._hostname)
        
	self._headers = {
            'Content-Type': 'application/json'
        }

        self._payload = {}


    def run(self):
	transId = ""

        resp = requests.post(self._uri,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)



        if resp.status_code == 200:
	    resultat = resp.json()
	    transId = str(resultat['transId'])


        else:
            #res = resp.json()
            raise Exception(res['message'])
        return transId


def main():
    changed = False


    module = AnsibleModule(
       argument_spec=dict(
            server=dict(required=True),
            partition=dict(default='Common'),
            name=dict(default=''),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )
    )


    obj = BigIpRest(module)

#    if obj.run():
    transaction = obj.run()
    changed = True
 
    module.exit_json(changed=changed, transId=transaction)
#    module.exit_json(transId=transaction)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()

