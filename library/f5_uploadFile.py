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
        self._fileName = module.params.get('fileName')
	self._fileType = module.params.get('fileType')
        self._validate_certs = module.params.get('validate_certs')

class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

	self._headers = {
            'Content-Type': 'application/octet-stream'
        }

	if self._fileType == "policy":
        	self._uri = 'https://%s/mgmt/tm/asm/file-transfer/uploads/%s' % (self._hostname, self._fileName)
	elif self._fileType == "vulnerabilities":
                self._uri = 'https://%s/mgmt/tm/asm/file-transfer/uploads/%s' % (self._hostname, self._fileName)
	else:
		self._uri = 'https://%s/mgmt/shared/file-transfer/uploads/%s' % (self._hostname, self._fileName)


    def run(self):
        changed = False

	chunk_size = 512 * 1024

	fileobj = open(self._fileName, 'rb')
        filename = os.path.basename(self._fileName)

        requests.packages.urllib3.disable_warnings()
        size = os.path.getsize(self._fileName)

        start = 0

        while True:
                file_slice = fileobj.read(chunk_size)
                if not file_slice:
                	changed = True
		        break

                current_bytes = len(file_slice)
                if current_bytes < chunk_size:
                        end = size
                else:
                        end = start + current_bytes

                content_range = "%s-%s/%s" % (start, end - 1, size)
                self._headers['Content-Range'] = content_range
                resp = requests.post(self._uri,
			headers=self._headers,
                      	auth=(self._username, self._password),
                      	data=file_slice,
                      	verify=self._validate_certs)
		

                start += current_bytes

        return changed



def main():
    changed = False

    module = AnsibleModule(
       argument_spec=dict(
            server=dict(required=True),
            fileName=dict(required=True),
            fileType=dict(required=True, choices=['policy','vulnerabilities', 'cert', 'key']),
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


