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
	self._azPublicIP = module.params.get('azPublicIP')
	self._fqdn = module.params.get('fqdn')

class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

	self._uri = 'https://%s/mgmt/tm/transaction' % (self._hostname)
        
	self._headers = {
            'Content-Type': 'application/json'
        }

        self._payload = {
	    "fqdn": self._fqdn,
            "azPublicIP": self._azPublicIP,
	}


    def run(self):
	transId = ""

        resp = requests.post(self._uri,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)



        if resp.status_code == 200:
#            f.write("response code: " + str(resp) + "\n")
	    resultat = resp.json()
	    f = open("/tmp/outLogs.txt","w")
            f.write("URI: " + self._uri + "\n")
            f.write("Headers: " + str(resp.headers) + "\n")
            f.write("Payload: " + str(json.dumps(self._payload)) + "\n")
            f.write("Response: " + str(resp.json()) + "\n")
            f.close()


        else:
            #res = resp.json()
            raise Exception(res['message'])
	   # f.write("RESULT: " + resp.text + "\n")
        return changed


def main():
    changed = False


    module = AnsibleModule(
       argument_spec=dict(
            connection=dict(default='rest', choices=['icontrol', 'rest']),
            server=dict(required=True),
            partition=dict(default='Common'),
            name=dict(default=''),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')

    obj = BigIpRest(module)

#    if obj.run():
    transaction = obj.run()
    changed = True
    f = open("outLogs.txt","w")
    f.write("OBJ: " + transaction + "\n")
    f.close()    
 
    module.exit_json(changed=changed, transId=transaction)
#    module.exit_json(transId=transaction)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()

