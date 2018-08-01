#!/usr/bin/python
# -*- coding: utf-8 -*-
#


import socket


try:
    import json
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True


class IPAMCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._appId = module.params.get('appId')
        self._hostname = module.params.get('ipam')
        self._token = module.params.get('token')
        self._tenant = module.params.get('tenant')
        self._validate_certs = module.params.get('validate_certs')


class IPAMRest(IPAMCommon):
    def __init__(self, module):
        super(IPAMRest, self).__init__(module)

    	self._uri = 'http://%s/api/%s/subnets/%s/first_free/' % (self._hostname, self._appId, self._tenant)
        
    	self._headers = {
            'token': self._token,
            'Content-Type': 'application/json'
        }

    	self._payload = {}



    def run(self):
        resp = requests.get(self._uri,
			    headers=self._headers,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)



        if resp.status_code == 200:
        	resultat = resp.json()
        	ipAddress = str(resultat['data'])

        else:
            res = resp.json()
            raise Exception(res['message'])
        return ipAddress


def main():
    changed = False


    module = AnsibleModule(
            argument_spec=dict(
            ipam=dict(required=True),
            token=dict(required=True),
            tenant=dict(required=True),
            appId=dict(default='rest'),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )
    )

    ipam = module.params.get('ipam')
    appId = module.params.get('appId')
    token = module.params.get('token')
    tenant = module.params.get('tenant')
    username = module.params.get('user')
    password = module.params.get('password')

    

    obj = IPAMRest(module)

#    if obj.run():
    ipAddress = obj.run()
    changed = True
 
    module.exit_json(changed=changed, ipAddress=ipAddress)
#    module.exit_json(transId=transaction)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
