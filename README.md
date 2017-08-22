## F5 & Ansible Meetups - Setup and Demo

### This repository was created to help F5 engineers demo the capabilities of BIG-IP configured via Ansible
___

## Tool Kits

### Ansible
F5 builds and contributes to Ansible via social coding on Github. Once a version has passed testing it is submitted to Ansible and rolled into the next version release. As Ansible can accepted side loaded modules, if a release cycle is delayed or if you would like to contribute, the repository is below, you can also ***Watch*** this for changes.
[F5 Network's Ansible Modules](https://github.com/F5Networks/f5-ansible/tree/devel/library)

### F5 Super NetOps Container (Ansible Variant)
F5 has created an MVP solution for getting up and running with Ansible, the MVP includes the needed dependencies such as Ansible, Python, f5-python-sdk, bigsuds, ect. The MVP is delivered via code in this repository and runs in the F5 Super-Netops Container via ***Docker***. If you do not have Docker installed you can [Installing Ansible on a Mac Documentation](docs/INSTALL.md) directly.

The Super NetOps Container Variant (Ansible) we will be working with can be viewed on [Docker Hub](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)
___

## Important Files within the MVP

### user_repos.json File
The user_repos.json file is used to dynamically pull down whatever Github repository is specified, this enables continuously delivery of new content every time the container is started, or the repositories are refreshed. This also allows you to specify your own newly downloaded repository for future use against your custom environment.

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
This MVP code leverages the Ansible-Vault tool, and includes the encrypted password protected file [password.yml](password.yml). The Vault is used to contain the credentials of the BIG-IP(s) we'll be working with, in our demo environment the BIG-IP credentials are "admin" and "password", in your environment these will likely be different, change them as needed.
To edit the username and password run from the root of the Repository:
```
ansible-vault edit password.yml
```
The Ansible-Vault password for the password.yml file is *password*

### hosts File
The hosts file is used as a list of Ansible Endpoints, in our case this MVP is configured to execute on only a single specified host, changing this to your host(s) will allow you to run this demonstration against in your environment
```
[BIGI-IP]
10.1.1.5
```
[hosts](hosts)

### main.yml File
This code is the variables used in the scripts we will be executing, out en
[main.yml](/roles/operations/tasks)
___

## Running the Demo

### Starting the MVP Image
1. Clone/Download [this repository](https://github.com/jmcalalang/ansible_f5)
2. Once the Clone/Download is complete, note the location of the newly downloaded repository, you will need to specify the ***Full Path*** in the container launch script
3. Launch the container with the command below

```
docker run -p 8080:80 -p 2222:22 --rm -it -v "/GitHub Repository/Ansible_Meetups/misc/user_repos.json:/tmp/user_repos.json" -e SNOPS_GH_BRANCH=master f5devcentral/f5-super-netops-container:ansible
```

The exposed ports on the Super NetOps Container are used to interact with the solution, after the docker run command completes you will be placed directly into the container via a shell, this interaction can also be used instead of creating an SSH session to the container after being started. More instructions on the Super Netops Container [F5 Programmability Lab Class 2 - Super-NetOps-Container](http://clouddocs.f5.com/training/community/programmability/html/class2/class2.html) & [F5 Docker Hub ](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)

4. After a successful launch of the Super NetOps Container with the Ansible MVP code you should be dropped into a Shell

```
docker run -p 8080:80 -p 2222:22 --rm -it -v "/Volumes/JC Drive/GitHub Repository/Ansible_Meetups/misc/user_repos.json:/tmp/user_repos.json" -e SNOPS_GH_BRANCH=develop f5devcentral/f5-super-netops-container:develop-ansible
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
[environment] SNOPS_GH_BRANCH=develop
Reticulating splines...
Becoming self-aware...
[cloneGitRepos] Retrieving repository list from https://github.com/f5devcentral/f5-super-netops-container.git#develop
[updateRepos] Processing /tmp/snops-repo/images/ansible/fs/etc/snopsrepo.d/ansible.json
[updateRepos]  Processing /tmp/snops-repo/images/base/fs/etc/snopsrepo.d/base.json
[updateRepos] Processing /tmp/user_repos.json
[cloneGitRepos] Loading repositories from /home/snops/repos.json
[cloneGitRepos] Found 9 repositories to clone...
[cloneGitRepos][1/9] Cloning f5-sphinx-theme#master from https://github.com/f5devcentral/f5-sphinx-theme.git
[cloneGitRepos][1/9]  Installing f5-sphinx-theme#master
[cloneGitRepos][2/9] Cloning f5-super-netops-container#develop from https://github.com/f5devcentral/f5-super-netops-container.git
[cloneGitRepos][2/9]  Installing f5-super-netops-container#develop
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

To access these services you may need to remap ports on your host to the
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













## Useful Information about the MVP and Ansible

### Module Documentation
The MVP is also already setup with some working modules, for a more in-depth view of the modules we will be working with:
[Ansible Module Documents Used in this Collection](docs/MODULES.md)

### Ansible Roles
This ansible repository is organized into roles. Roles are collections of templates, files, tasks,
and variables. Tasks are organized based on the particular module they are implementing. For example,
the bigip_device_ntp module is a subdirectory under the onboarding role and has a task
set_ntp.yml (*roles/tasks/bigip_device_ntp/set_ntp.yml*).

### Ansible Playbooks
The playbooks in in the ansible playbook directory include the roles. For our demo and MVP we will be executing the **operation** Playbook.

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

### Useful vimrc macro for editing YaML files
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
