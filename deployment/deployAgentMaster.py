#!/usr/bin/python

import argparse
import getpass
import subprocess
import os
import sys

'''
This script will start two scripts for deploying insightagent to hosts
'''

def get_args():
    parser = argparse.ArgumentParser(description='Script retrieves arguments for insightfinder agent.')
    parser.add_argument('-i', '--PROJECT_NAME_IN_INSIGHTFINDER', type=str, help='Project Name registered in Insightfinder', required=True)
    parser.add_argument('-n', '--USER_NAME_IN_HOST', type=str, help='User Name in Hosts', required=True)
    parser.add_argument('-u', '--USER_NAME_IN_INSIGHTFINDER', type=str, help='User Name in Insightfinder', required=True)
    parser.add_argument('-k', '--LICENSE_KEY', type=str, help='License key for the user', required=True)
    parser.add_argument('-s', '--SAMPLING_INTERVAL_MINUTE', type=str, help='Sampling Interval Minutes', required=True)
    parser.add_argument('-r', '--REPORTING_INTERVAL_MINUTE', type=str, help='Reporting Interval Minutes', required=True)
    parser.add_argument('-t', '--AGENT_TYPE', type=str, help='Agent type: proc or cadvisor or docker_remote_api or cgroup or daemonset or elasticsearch or collectd or hypervisor or ec2monitoring or jolokia', choices=['proc', 'cadvisor', 'docker_remote_api', 'cgroup', 'daemonset', 'elasticsearch', 'collectd', 'hypervisor', 'ec2monitoring', 'jolokia'],required=True)
    args = parser.parse_args()
    projectName = args.PROJECT_NAME_IN_INSIGHTFINDER
    user = args.USER_NAME_IN_HOST
    userInsightfinder = args.USER_NAME_IN_INSIGHTFINDER
    licenseKey = args.LICENSE_KEY
    samplingInterval = args.SAMPLING_INTERVAL_MINUTE
    reportingInterval = args.REPORTING_INTERVAL_MINUTE
    agentType = args.AGENT_TYPE
    return projectName, user, userInsightfinder, licenseKey, samplingInterval, reportingInterval, agentType

downloadFiles = ["installAgentMaster.sh"]
homepath = os.getcwd()

def removeFile(filename):
    proc = subprocess.Popen("rm "+filename+"*", cwd=homepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()

def clearDownloads():
    for eachFile in downloadFiles:
        removeFile(eachFile)

def downloadFile(filename):
    proc = subprocess.Popen("wget --no-check-certificate https://raw.githubusercontent.com/insightfinder/InsightAgent/master/deployment/"+filename, cwd=homepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()
    if "failed" in str(err) or "ERROR" in str(err):
        sys.exit(err)
    os.chmod(filename,0755)

def downloadRequiredFiles():
    for eachFile in downloadFiles:
        downloadFile(eachFile)

def stopCronHypervisor():
    global user
    global password
    removeFile("stopcron.py")
    proc = subprocess.Popen("wget --no-check-certificate https://raw.githubusercontent.com/insightfinder/InsightAgent/master/hypervisor/stopcron.py", cwd=homepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()
    if "failed" in str(err) or "ERROR" in str(err):
        print "Can't download stopcron.py"
        return
    os.chmod("stopcron.py",0755)
    proc = subprocess.Popen(["pyenv/bin/python "+os.path.join(homepath,"stopcron.py")+" -n "+user+" -p "+password], cwd=homepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()
    if "failed" in str(err) or "error" in str(err):
        print "Can't stop agent in some machines"
    removeFile("stopcron.py")

def stopCron():
    global user
    global password
    removeFile("stopcron.py")
    proc = subprocess.Popen("wget --no-check-certificate https://raw.githubusercontent.com/insightfinder/InsightAgent/master/deployment/stopcron.py", cwd=homepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()
    if "failed" in str(err) or "ERROR" in str(err):
        print "Can't download stopcron.py"
        return
    os.chmod("stopcron.py",0755)
    proc = subprocess.Popen(["pyenv/bin/python "+os.path.join(homepath,"stopcron.py")+" -n "+user+" -p "+password], cwd=homepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()
    if "failed" in str(err) or "error" in str(err):
        print "Can't stop agent in some machines"
    removeFile("stopcron.py")

if __name__ == '__main__':
    global projectName
    global user
    global host
    global password
    global hostfile
    global userInsightfinder
    global licenseKey
    global samplingInterval
    global reportingInterval
    global agentType

    projectName, user, userInsightfinder, licenseKey, samplingInterval, reportingInterval, agentType = get_args()
    retryOptionAttempts = 3
    retryKeyAttempts = 3
    while retryOptionAttempts:
        passOrKey = raw_input("Enter one of the option:\n[p] for password authentiication\n[k] for key based authentication\n")
        if passOrKey == 'p':
            password=getpass.getpass("Enter %s's password for the deploying hosts:"%user)
            break
        elif passOrKey == 'k':
            password = raw_input("Enter name of identify file with path:")
            while os.path.isfile(password) == False and retryKeyAttempts != 0:
                retryKeyAttempts-=1
                password = raw_input("Invalid file/filepath. Please Enter again:")
            break
        else:
            retryOptionAttempts-=1
            continue
    if retryOptionAttempts == 0 or retryKeyAttempts == 0:
        print "Retry attempts exceeded. Exiting now"
        sys.exit()

    #if agentType == "hypervisor":
    #    stopCronHypervisor()
    #else:
    #    stopCron()
    clearDownloads()
    downloadRequiredFiles()

    print "Starting Deployment"
    print "Homepath: ", homepath
    downloadFile("agentMaster.py");
    command = ""+os.path.join(homepath,"installAgentMaster.sh")+ " -i " +projectName+" -u "+userInsightfinder+" -k "+licenseKey+" -s "+samplingInterval+" -r "+reportingInterval+" -t "+agentType+" -p "+password+" -c "+"60"
    print "Command", command
    proc = subprocess.Popen([command], cwd=homepath, stdout=subprocess.PIPE, shell=True)
    
    (out,err) = proc.communicate()
    print out
    clearDownloads()
    removeFile("deployAgentMaster.py")
    
