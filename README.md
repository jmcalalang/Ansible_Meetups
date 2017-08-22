## Ansible Library
F5 builds and contributes to Ansible via social coding on Github. Once a version has passed testing it is submitted to Ansible and rolled into the next version release. As Ansible can accepted side loaded modules, if a release cycle is delayed or if you would like to contribute, the repository is below, you can also ***Watch*** this for changes.
[F5 Network's Ansible Modules](https://github.com/F5Networks/f5-ansible/tree/devel/library)

## Social Coding with Github
[![Social Coding with Github](https://img.youtube.com/vi/vTiINnsHSc4/0.jpg)](https://youtu.be/vTiINnsHSc4 "Social Coding with Github")

## F5 Super NetOps Container (Ansible Variant)
F5 has created an MVP solution for getting up and running with Ansible, the MVP includes the needed dependencies such as Ansible, Python, f5-python-sdk, bigsuds, ect. The MVP is delivered via code in this repository and runs in the F5 Super-Netops Container via ***Docker***. If you do not have Docker installed you can [Installing Ansible on a Mac Documentation](docs/INSTALL.md) directly.

**First Steps to get the MVP running**
1. Clone/Download [this repository](https://github.com/jmcalalang/ansible_f5)
2. Once the Clone/Download are complete, note the location of the newly downloaded repository, you will need to specify the ***Full Path*** in the container launch script
3. Launch the container with the command below

```
docker run -p 8080:80 -p 2222:22 --rm -it -v "/GitHub Repository/ansible_f5/misc/user_repos.json:/tmp/user_repos.json" -e SNOPS_GH_BRANCH=master f5devcentral/f5-super-netops-container:ansible
```

The exposed ports on the Super NetOps Container are used to interact with the solution, after the docker run command completes you will be placed directly into the container via a shell, this interaction can also be used instead of creating an SSH session to the container after being started. More instructions on the Super Netops Container [F5 Programmability Lab Class 2 - Super-NetOps-Container](http://clouddocs.f5.com/training/community/programmability/html/class2/class2.html) & [F5 Docker Hub ](https://hub.docker.com/r/f5devcentral/f5-super-netops-container/)

## user_repos.json File
The user_repos.json file that you are referencing above is used to dynamically pull down whatever Github repository is specified, this enables continuously delivery of new content every time the container is started or repositories are refreshed. This will also allow you to specify your own newly downloaded repository for future use against your custom environment.

```
{
	"repos": [
		{
			"name":"jmcalalang-ansible_f5",
			"repo":"https://github.com/jmcalalang/ansible_f5.git",
			"branch":"master",
			"skip":false,
			"skipinstall":true
		}
	]
}
```
[user_repos.json](misc/user_repos.json)

## YAML Syntax Overview
The MVP is already setup with some configuration, which needs only small modification to support working in your environment, if you would like a deeper understanding of Ansible code language YAML, it can be found at:
[YAML Syntax Overview](https://learn.getgrav.org/advanced/yaml)

## Module Documentation
The MVP is also already setup with some working modules, for a more in-depth view of the modules we will be working with:
[Ansible Module Documents Used in this Collection](docs/MODULES.md)

## Ansible Vault
This MVP code leverages the Ansible-Vault tool, and includes the encrypted password protected file [password.yml](password.yml). The Vault is used to contain the credentials of the BIG-IP(s) we'll be working with, in our demo environment the BIG-IP credentials are "admin" and "password", in your environment these will likely be different, change them as needed.
To edit the username and password run from the root of the Repository:
```
ansible-vault edit password.yml
```
The password for the password file is *password*

## hosts File
The hosts file is used as a list of Ansible Endpoints, in our case this MVP is configured to execute on only a single specified host, changing this to your host(s) will allow you to run this demonstration against in your environment
```
[BIGI-IP]
10.1.1.5
```
[hosts](hosts)

## main.yml File
This code is the variables used in the scripts we will be executing, out en
[main.yml](/roles/operations/tasks)

## Ansible Roles
This ansible repository is organized into roles. Roles are collections of templates, files, tasks,
and variables. Tasks are organized based on the particular module they are implementing. For example,
the bigip_device_ntp module is a subdirectory under the onboarding role and has a task
set_ntp.yml (*roles/tasks/bigip_device_ntp/set_ntp.yml*).

## Ansible Playbooks
The playbooks in in the ansible playbook directory include the roles. For our demo and MVP we will be executing the **onboarding** Playbook.

```
$ANSIBLE_HOME_DIRECTORY/site.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/onboarding.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/operation.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/teardown.yml
$ANSIBLE_HOME_DIRECTORY/playbooks/today.yml
```

## Running the Ansible Code
This Ansible code base comes with a shell helper script that runs the playbooks. The
```
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --all
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --onboarding
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --operation
$ANSIBLE_HOME_DIRECTORY/run_ansible.sh --teardown
```

## Running the Demo












## Ansible Variable Precedence

[Ansible 2.x Order of Variable Precedence](docs/PRECEDENCE.md)

## Useful vimrc macro for editing YaML files
```
autocmd FileType yaml setlocal ai ts=2 sw=2 et colorcolumn=1,3,5,7,9,11,13 nu
```

## Infrastructure as Code Principles, Practices and Patterns
[Infrastructure as Code Benefits](docs/IAC.md)

## License
### Apache V2.0

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
