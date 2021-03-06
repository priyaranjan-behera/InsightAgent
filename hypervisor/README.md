# InsightAgent: hypervisor
Agent Type: hypervisor

Platform: VMkernel

InsightFinder agent can be used to monitor system performance metrics of hypervisor hosts.

##### Instructions to register a project in Insightfinder.com
- Go to the link https://insightfinder.com/
- Sign in with the user credentials or sign up for a new account.
- Go to Settings and Register for a project under "Insight Agent" tab.
- Give a project name, select Project Type as "Private Cloud".
- Note down license key which is available in "User Account Information". To go to "User Account Information", click the userid on the top right corner.

##### Pre-requisites:
This pre-requisite is needed on the machine which launches deployInsightAgent.py.
For Debian and Ubuntu, the following command will ensure that the required dependencies are installed:
```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```
For Fedora and RHEL-derivatives, the following command will ensure that the required dependencies are installed:
```
sudo yum install gcc libffi-devel python-devel openssl-devel
```

##### To deploy agent on multiple hosts:

- Get the deployment script from github using below command:
```
wget --no-check-certificate https://raw.githubusercontent.com/insightfinder/InsightAgent/master/deployment/deployInsightAgent.sh
```
and change the permissions with the command.
```
 chmod 755 deployInsightAgent.sh
```
- Get IP address of all machines (or hosts) on which InsightFinder agent needs to be installed.
- All machines should have same login username and password.
- Include IP address of all hosts in hostlist.txt and enter one IP address per line.
- To deploy run the following command:
```
./deployInsightAgent.sh -n USER_NAME_IN_HOST
                             -i PROJECT_NAME_IN_INSIGHTFINDER
                             -u USER_NAME_IN_INSIGHTFINDER
                             -k LICENSE_KEY
                             -s SAMPLING_INTERVAL_MINUTE
                             -r REPORTING_INTERVAL_MINUTE
                             -t AGENT_TYPE
AGENT_TYPE is *hypervisor*.
```
- When the above script is run, if prompted for password, enter either the password or the name of the identity file along with file path.
Example: /home/insight/.ssh/id_rsa


##### To get more details on the command, run
```
./deployInsightAgent.sh
```

##### To undo agent deployment on multiple hosts:
- Get the script for stopping agents from github using below command:
```
wget --no-check-certificate https://raw.githubusercontent.com/insightfinder/InsightAgent/master/hypervisor/stopcron.sh
```
and change the permissions with the command.
```
 chmod 755 stopcron.sh
```
- Include IP address of all hosts in hostlist.txt and enter one IP address per line.
- To stop the agent run the following command:
```
./stopcron.sh -n USER_NAME_IN_HOST -p PASSWORD

USER_NAME_IN_HOST - username used to login into the host machines
PASSWORD - password or name of the identity file along with path
```

##### To install agent on local machine:
```
./hypervisor/install.sh -i PROJECT_NAME -u USER_NAME -k LICENSE_KEY -s SAMPLING_INTERVAL_MINUTE -r REPORTING_INTERVAL_MINUTE -t AGENT_TYPE
```

