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
        self._validate_certs = module.params.get('validate_certs')


class IPAMRest(IPAMCommon):
    def __init__(self, module):
        super(IPAMRest, self).__init__(module)

	self._uri = 'http://%s/api/%s/user/' % (self._hostname, self._appId) 
        
	self._headers = {
            'Content-Type': 'application/json'
        }

        self._payload = {}


    def run(self):
        resp = requests.post(self._uri,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs)



        if resp.status_code == 200:
	    resultat = resp.json()
	    token = str(resultat['data']['token'])


        else:
            res = resp.json()
            raise Exception(res['message'])
        return token


def main():
    changed = False


    module = AnsibleModule(
            argument_spec=dict(
            ipam=dict(required=True),
            appId=dict(default='rest'),
            user=dict(required=True, aliases=['username']),
            password=dict(required=True),
            validate_certs=dict(default='no', type='bool')
        )
    )

    ipam = module.params.get('ipam')
    appId = module.params.get('appId')
    username = module.params.get('user')
    password = module.params.get('password')
    

    obj = IPAMRest(module)

#    if obj.run():
    token = obj.run()
    changed = True
 
    module.exit_json(changed=changed, tokenId=token)
#    module.exit_json(transId=transaction)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()


