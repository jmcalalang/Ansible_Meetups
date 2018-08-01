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
	self._fqdn = module.params.get('fqdn')
        self._ip = module.params.get('ipAddress')
        self._validate_certs = module.params.get('validate_certs')


class IPAMRest(IPAMCommon):
    def __init__(self, module):
        super(IPAMRest, self).__init__(module)

    	self._uri = 'http://%s/api/%s/addresses/' % (self._hostname, self._appId) 
        
    	self._headers = {
            'token': self._token,
            'Content-Type': 'application/json'
        }

    	self._payload = {
            "hostname": self._fqdn,
            "subnetId": self._tenant,
            "ip": self._ip 
        }


    def run(self):
        resp = requests.post(self._uri,
			    headers=self._headers,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)


        if resp.status_code == 201:
        	resultat = resp.json()
        	respString = str(resultat)

        else:
		res = resp.json()
            	raise Exception(res['message'])
        return respString


def main():
    changed = False


    module = AnsibleModule(
            argument_spec=dict(
            ipam=dict(required=True),
            token=dict(required=True),
            tenant=dict(required=True),
            appId=dict(default='rest'),
	    fqdn=dict(required=True),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            ipAddress=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )
    )

    ipam = module.params.get('ipam')
    appId = module.params.get('appId')
    token = module.params.get('token')
    tenant = module.params.get('tenant')
    fqdn = module.params.get('fqdn')
    username = module.params.get('user')
    password = module.params.get('password')
    ipAddress = module.params.get('ipAddress')    

    obj = IPAMRest(module)

#    if obj.run():
    resp = obj.run()
    changed = True
 
 
    module.exit_json(changed=changed)
#    module.exit_json(transId=transaction)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
