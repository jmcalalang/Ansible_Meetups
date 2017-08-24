## F5 & Ansible Meetups - Setup and Demo

This repository has been created to help F5 engineers demo the capabilities of BIG-IP configured via Ansible. For our demo purposes, we will run an ***Operations*** playbook, this quick demo will create new objects (Nodes, Pool, Profiles, iRules and Virtual Server), along with upload and configure an App_Svcs iApp. Since the Ansible modules are [Idempotent](http://www.restapitutorial.com/lessons/idempotency.html), the same modules can be used for updating a service as needed. After the services are deployed we will tear down the created items, showing lifecycle of an application from a code perspective.

### Order of Operations

The order of operations from beginning to end can be a learning curve; this is because as Engineers we're used to modifying configuration directly, with Infrastructure as Code we're setting our desired state in Code and then letting Orchestration carry the solution to end (Declarative). The Helper Script is the starting point to executing our Order of Operations; after the desired state is defined (main.yml) we start the process by executing the [Helper Script](https://github.com/jmcalalang/Ansible_Meetups/blob/master/run_ansible.sh), which calls our [Playbook](https://github.com/jmcalalang/Ansible_Meetups/blob/master/playbooks/operations.yml), the Playbook specifies a [Role](https://github.com/jmcalalang/Ansible_Meetups/tree/master/roles/operations) which contains [Tasks](https://github.com/jmcalalang/Ansible_Meetups/tree/master/roles/operations/tasks), the Tasks are executed in order with variables defined by our [main.yml](https://github.com/jmcalalang/Ansible_Meetups/blob/master/roles/operations/tasks/main.yml) file. The main.yml file is the desired end state, Tasks, Modules, Role(s) and Playbook(s) get you there.
___

## Tool Kits

### Ansible
F5 builds and contributes to Ansible via [Social Coding](https://youtu.be/vTiINnsHSc4) with Github. Once a version has passed testing it is submitted to Ansible and rolled into the next version release. F5 modules can come from software editions of Ansible (2.1,2.2,2.3 etc), or can be side-loaded via an Ansible library path. If you would like to contribute, view what’s available, or acquire modules to side-load, the repository is listed below. You can also ***Watch*** this Repository for changes/fixes.
[F5 Network's Ansible Modules](https://github.com/F5Networks/f5-ansible/tree/devel/library)

### F5 Super NetOps Container (Ansible Variant)
F5 has created an MVP solution for getting up and running with Ansible and BIG-IP/iWorkflow. The MVP includes the needed dependencies such as Ansible, Python, [f5-common-python](https://github.com/F5Networks/f5-common-python), bigsuds, etc. The MVP is delivered via code in this repository and runs within the F5 Super NetOps Container via ***Docker***. If you do not have Docker installed you can [Install Ansible on a Mac Doc](docs/INSTALL.md) directly.

The Super NetOps Container Variant (Ansible) we will be working with can be viewed on [Docker Hub](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)
___

## Important Files within the MVP

### user_repos.json File
The user_repos.json file is used to dynamically pull down whatever Github repository is specified in its json body. Utilizing this enables Continuously Delivery of new content every time the container is started, or the repositories are refreshed. This also allows you to specify your own downloaded/forked/cloned repository for use against your custom environment.

```
{
	"repos": [
		{
			"name":"Ansible_Meetups",
			"repo":"https://github.com/jmcalalang/Ansible_Meetups.git",
			"branch":"master",
			"skip":false,
			"skipinstall":true
		}
	]
}
```
[user_repos.json](misc/user_repos.json)

### Ansible Vault
This MVP code leverages the Ansible-Vault tool, the MVP includes an encrypted password protected file [password.yml](password.yml) for use with playbooks. The Ansible-Vault password.yml file contains the credentials of the BIG-IP we'll be working with, in our demo environment the BIG-IP credentials are "admin" and "password", in your environment these will likely be different, change them as needed.
To edit password.yml to a different username and password run the following command from the mapped repository directory in the Super NetOps Container.
```
ansible-vault edit password.yml
```
The Ansible-Vault password for the password.yml file is ***password***

### hosts File
The hosts file is used as a list of Ansible Inventory, in our case the MVP is configured to execute on only a single specified host, changing this file to reflect your Inventory will allow you to run this demonstration against your environment
```
[BIG-IPA]
10.1.1.6
```
[hosts](hosts)

### main.yml File
This file contains the variables used in the various Ansible scripts we will be executing, changing the variables in this file reflect what Ansible will deploy to a BIG-IP, for custom environments this **will need** to be modified. In the MVP, there are currently main.yml files for every playbook; our demo ***operations*** playbook will utilize an already configured one to create things like Nodes/Pools and Virtual Servers.

[main.yml](roles/operations/tasks/main.yml)
___

## Running the Demo

### Staging the Environment
For F5 Engineers a UDF **2.0** Blueprint has been created, the ```main.yml```, ```hosts```, ```password.yml``` have all been configured to use UDF, you will need to modify the ```user_repos.json``` file, as this UDF Blueprint is used for several different solutions. If you are running this demo from another environment you will need to update all these files respectively.

1. Login to UDF via Federate
2. Deploy UDF Blueprint "F5 Super-NetOps & Ansible MVP"
![image_003](/misc/images/image_003.png)
3. Once deployed, make sure you start all VM's
4. Login to the ```Windows Host``` via RDP (Credentials are user/user)
![image_004](/misc/images/image_004.png)
5. After you are on the ```Windows Host``` open application Putty (Located on the Task Bar)
6. From the Putty window connect to the ```Docker Host``` (Credentials are ```ubuntu``` no password)
![image_001](/misc/images/image_001.png)
![image_002](/misc/images/image_002.png)


### Using the MVP Image
1. Within the ```Docker Host``` is a staged ```user_repos.json``` file, located in the home directory (/home/ubuntu/user_repos.json) of your ```ubuntu``` user. Modify the staged user_repos.json to reflect the below. [VI](https://www.cs.colostate.edu/helpdocs/vi.html) is installed on the Docker Host for you, and works as expected.
```
{
	"repos": [
		{
			"name":"Ansible_Meetups",
			"repo":"https://github.com/jmcalalang/Ansible_Meetups.git",
			"branch":"master",
			"skip":false,
			"skipinstall":true
		}
	]
}
```
2. Launch the container with the command below from the shell window of the ```Docker Host```

```
sudo docker run -p 8080:80 -p 2222:22 --rm -it -v "/home/ubuntu/user_repos.json:/tmp/user_repos.json" -e SNOPS_GH_BRANCH=master f5devcentral/f5-super-netops-container:ansible

```

The exposed ports on the Super NetOps Container are used to interact with the solution; though the Super NetOps Container does have an exposed SSH port, we'll use the dropped into shell to run the MVP. More information on the Super NetOps Container can be found in [F5 Programmability Lab Class 2 - Super-NetOps-Container](http://clouddocs.f5.com/training/community/programmability/html/class2/class2.html) & [F5 Docker Hub ](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)

3. After the successful launch of the Super NetOps Container you should be dropped into its shell:

```
ubuntu@ip-10-1-1-4:~$ sudo docker run -p 8080:80 -p 2222:22 --rm -it -v "/home/ubuntu/user_repos.json:/tmp/user_repos.json" -e SNOPS_GH_BRANCH=master f5devcentral/f5-super-netops-container:ansible
[s6-init] making user provided files available at /var/run/s6/etc...exited 0.
[s6-init] ensuring user provided files have correct perms...exited 0.
[fix-attrs.d] applying ownership & permissions fixes...
[fix-attrs.d] done.
[cont-init.d] executing container initialization scripts...
[cont-init.d] done.
[services.d] starting services
[services.d] done.
[environment] SNOPS_HOST_SSH=2222
[environment] SNOPS_REPO=https://github.com/f5devcentral/f5-super-netops-container.git
[environment] SNOPS_AUTOCLONE=1
[environment] SNOPS_HOST_IP=172.17.0.2
[environment] SNOPS_ISALIVE=1
[environment] SNOPS_GIT_HOST=github.com
[environment] SNOPS_REVEALJS_DEV=0
[environment] SNOPS_HOST_HTTP=8080
[environment] SNOPS_IMAGE=ansible
[environment] SNOPS_GH_BRANCH=master
Reticulating splines...
Becoming self-aware...
[cloneGitRepos] Retrieving repository list from https://github.com/f5devcentral/f5-super-netops-container.git#master
[updateRepos] Processing /tmp/snops-repo/images/ansible/fs/etc/snopsrepo.d/ansible.json
[updateRepos]  Processing /tmp/snops-repo/images/base/fs/etc/snopsrepo.d/base.json
[updateRepos] Processing /tmp/user_repos.json
[cloneGitRepos] Loading repositories from /home/snops/repos.json
[cloneGitRepos] Found 9 repositories to clone...
[cloneGitRepos][1/9] Cloning f5-sphinx-theme#master from https://github.com/f5devcentral/f5-sphinx-theme.git
[cloneGitRepos][1/9]  Installing f5-sphinx-theme#master
[cloneGitRepos][2/9] Cloning f5-super-netops-container#master from https://github.com/f5devcentral/f5-super-netops-container.git
[cloneGitRepos][2/9]  Installing f5-super-netops-container#master
[cloneGitRepos][3/9] Cloning f5-application-services-integration-iApp#master from https://github.com/F5Networks/f5-application-services-integration-iApp.git
[cloneGitRepos][3/9]  Installing f5-application-services-integration-iApp#master
[cloneGitRepos][4/9] Cloning f5-postman-workflows#develop from https://github.com/0xHiteshPatel/f5-postman-workflows.git
[cloneGitRepos][4/9]  Installing f5-postman-workflows#develop
[cloneGitRepos][5/9] Cloning f5-automation-labs#master from https://github.com/f5devcentral/f5-automation-labs.git
[cloneGitRepos][5/9]  Installing f5-automation-labs#master
[cloneGitRepos][6/9] Cloning ultimate-vimrc#master from https://github.com/amix/vimrc.git
[cloneGitRepos][6/9]  Installing ultimate-vimrc#master
[cloneGitRepos][7/9] Cloning reveal-js#master from https://github.com/hakimel/reveal.js.git
[cloneGitRepos][7/9]  Installing reveal-js#master
[cloneGitRepos][8/9] Cloning f5-ansible#master from https://github.com/F5Networks/f5-ansible.git
[cloneGitRepos][8/9]  Installing f5-ansible#master
[cloneGitRepos][9/9] Cloning Ansible_Meetups#master from https://github.com/jmcalalang/Ansible_Meetups.git
[cloneGitRepos][9/9]  Skipping install
                                .----------.
                               /          /
                              /   ______.'
                        _.._ /   /_
                      .' .._/      '''--.
                      | '  '___          `.
                    __| |__    `'.         |
                   |__   __|      )        |
                      | | ......-'        /
                      | | \          _..'`
                      | |  '------'''
                      | |                      _
                      |_|                     | |
 ___ _   _ _ __   ___ _ __          _ __   ___| |_ ___  _ __  ___
/ __| | | | '_ \ / _ \ '__| ______ | '_ \ / _ \ __/ _ \| '_ \/ __|
\__ \ |_| | |_) |  __/ |   |______|| | | |  __/ || (_) | |_) \__ \
|___/\__,_| .__/ \___|_|           |_| |_|\___|\__\___/| .__/|___/
          | |                                          | |
          |_|                                          |_|

Welcome to the f5-super-netops-container.  This image has the following
services running:

 SSH  tcp/22
 HTTP tcp/80

To access these services, you may need to remap ports on your host to the
local container using the command:

 docker run -p 8080:80 -p 2222:22 -it f5devcentral/f5-super-netops-container:base

From the HOST perspective, this results in:

 localhost:2222 -> f5-super-netops-container:22
 localhost:8080 -> f5-super-netops-container:80

You can then connect using the following:

 HTTP: http://localhost:8080
 SSH:  ssh -p 2222 snops@localhost

Default Credentials:

 snops/default
 root/default

Go forth and automate!

(you can now detach by using Ctrl+P+Q)

[root@f5-super-netops] [/] #

```
4. Change directory to the user_repos.json mapped Repository ```cd /home/snops/Ansible_Meetups```
5. Open Chrome from the ```Windows Host``` and validate the ```LAMP``` bookmark does not load, also verify via the ```BIG-IP A``` bookmark (Credentials admin/password) the configuration is blank, no objects exist yet
![image_005](/misc/images/image_005.png)
![image_011](/misc/images/image_011.png)
6. Return to the MVP and run the Ansible ***operations*** Playbook with Helper Script ```./run_ansible.sh -o```
7. Enter the Ansible-Vault password ```password```
![image_006](/misc/images/image_006.png)
8. Verify the Ansible Run success
![image_007](/misc/images/image_007.png)
9. Check BIG-IP A via the GUI for the newly created Node/Pool/Profiles/iRules and Virtual, and also the App_Svcs iApp deployment. The ```LAMP``` bookmark should also now function, loading the BIG-IP platform page
10. Run the Ansible ***operations*** Teardown Playbook with Helper Script ```./run_ansible.sh -t```
11. Enter the Ansible-Vault password ```password```
![image_009](/misc/images/image_009.png)
12. Verify the Ansible Run success
![image_010](/misc/images/image_010.png)
13. Check BIG-IP A via the GUI for the removed objects and iApp
![image_011](/misc/images/image_011.png)
14. Demo complete, eat Cake.
___

## Useful Information about the MVP and Ansible

### Module Documentation
The MVP is also already setup all current F5 modules, for a more in-depth view of the modules we will be working with:
[Ansible Module Documents Used in this Collection](docs/MODULES.md)

### Ansible Roles
This Ansible repository is organized into roles. Roles are collections of templates, files, tasks,
and variables. Tasks are organized based on the particular module they are implementing. For example,
the bigip_device_ntp module is a subdirectory under the onboarding role and has a task
set_ntp.yml (*roles/tasks/bigip_device_ntp/set_ntp.yml*).

### Ansible Playbooks
The playbooks in in the ansible playbook directory include the roles. For our demo and MVP, we execuded the **operation** Playbook.

```
$ANSIBLE_HOME_DIRECTORY/site.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/onboarding.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/operation.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/teardown.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/today.yml
```

### Running the Ansible Code
This Ansible code base comes with a shell helper script that runs the playbooks. The
```
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --all
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --onboarding
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --operation
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --teardown
```

### YAML Syntax Overview
The MVP is already setup with some configuration, which needs only small modification to support working in your environment, if you would like a deeper understanding of Ansible code language YAML, it can be found at:
[YAML Syntax Overview](https://learn.getgrav.org/advanced/yaml)

### Ansible Variable Precedence
[Ansible 2.x Order of Variable Precedence](docs/PRECEDENCE.md)

### Useful vimrc macro for editing YAML files
```
autocmd FileType yaml setlocal ai ts=2 sw=2 et colorcolumn=1,3,5,7,9,11,13 nu
```

## Infrastructure as Code Principles, Practices and Patterns
[Infrastructure as Code Benefits](docs/IAC.md)
___

## License
__

### Apache V2.0

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
