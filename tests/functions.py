#!/usr/bin/env python3

# Author: Eric Turgeon
# License: BSD

import requests
import select
import pybonjour
import json
import os
import re
from time import sleep
from subprocess import run, Popen, PIPE
from auto_config import default_api_url, api1_url, api2_url, user, password

global header
header = {'Content-Type': 'application/json', 'Vary': 'accept'}
global authentification
authentification = (user, password)

# used by reslove function
results = {}
resolved = []


def GET(testpath, **optional):
    if testpath.startswith('http'):
        getit = requests.get(testpath)
    else:
        if "api" in optional:
            api_v = optional.get('api', None)
            if api_v == "1":
                api_url = api1_url
            elif api_v == "2":
                api_url = api2_url
            else:
                raise ValueError('api parameter must be "1" or "2"')
        else:
            api_url = default_api_url
        if optional.pop("anonymous", False):
            auth = None
        else:
            auth = authentification
        getit = requests.get(api_url + testpath, headers=header,
                             auth=auth)
    return getit


def POST(testpath, payload=None, **optional):
    if "api" in optional:
        api_v = optional.get('api', None)
        if api_v == "1":
            api_url = api1_url
        elif api_v == "2":
            api_url = api2_url
        else:
            raise ValueError('api parameter should be "1" or "2"')
    else:
        api_url = default_api_url
    if optional.pop("anonymous", False):
        auth = None
    else:
        auth = authentification
    if payload is None:
        postit = requests.post(api_url + testpath, headers=header,
                               auth=auth)
    else:
        postit = requests.post(api_url + testpath, headers=header,
                               auth=auth, data=json.dumps(payload))
    return postit


def POST_TIMEOUT(testpath, payload, timeOut, **optional):
    if "api" in optional:
        api_v = optional.get('api', None)
        if api_v == "1":
            api_url = api1_url
        elif api_v == "2":
            api_url = api2_url
        else:
            raise ValueError('api parameter should be "1" or "2"')
    else:
        api_url = default_api_url
    if payload is None:
        postit = requests.post(api_url + testpath, headers=header,
                               auth=authentification, timeout=timeOut)
    else:
        postit = requests.post(api_url + testpath, headers=header,
                               auth=authentification, data=json.dumps(payload),
                               timeout=timeOut)
    return postit


def POSTNOJSON(testpath, payload, **optional):
    if "api" in optional:
        api_v = optional.get('api', None)
        if api_v == "1":
            api_url = api1_url
        elif api_v == "2":
            api_url = api2_url
        else:
            raise ValueError('api parameter should be "1" or "2"')
    else:
        api_url = default_api_url
    postit = requests.post(api_url + testpath, headers=header,
                           auth=authentification, data=payload)
    return postit


def PUT(testpath, payload, **optional):
    if "api" in optional:
        api_v = optional.get('api', None)
        if api_v == "1":
            api_url = api1_url
        elif api_v == "2":
            api_url = api2_url
        else:
            raise ValueError('api parameter should be "1" or "2"')
    else:
        api_url = default_api_url
    putit = requests.put(api_url + testpath, headers=header,
                         auth=authentification, data=json.dumps(payload))
    return putit


def PUT_TIMEOUT(testpath, payload, timeOut, **optional):
    if "api" in optional:
        api_v = optional.get('api', None)
        if api_v == "1":
            api_url = api1_url
        elif api_v == "2":
            api_url = api2_url
        else:
            raise ValueError('api parameter should be "1" or "2"')
    else:
        api_url = default_api_url
    putit = requests.put(api_url + testpath, headers=header,
                         auth=authentification, data=json.dumps(payload),
                         timeout=timeOut)
    return putit


def DELETE(testpath, payload=None, **optional):
    if "api" in optional:
        api_v = optional.get('api', None)
        if api_v == "1":
            api_url = api1_url
        elif api_v == "2":
            api_url = api2_url
        else:
            raise ValueError('api parameter should be "1" or "2"')
    else:
        api_url = default_api_url
    deleteit = requests.delete(api_url + testpath, headers=header,
                               auth=authentification,
                               data=json.dumps(payload) if payload else None)
    return deleteit


def SSH_TEST(command, username, passwrd, host):
    cmd = [] if passwrd is None else ["sshpass", "-p", passwrd]
    cmd += [
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-o",
        "VerifyHostKeyDNS=no",
        f"{username}@{host}",
        command
    ]
    process = run(cmd, stdout=PIPE, universal_newlines=True)
    output = process.stdout
    if process.returncode != 0:
        return {'result': False, 'output': output}
    else:
        return {'result': True, 'output': output}


def send_file(file, destination, username, passwrd, host):
    cmd = [] if passwrd is None else ["sshpass", "-p", passwrd]
    cmd += [
        "scp",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-o",
        "VerifyHostKeyDNS=no",
        file,
        f"{user}@{host}:{destination}"
    ]
    process = run(cmd, stdout=PIPE, universal_newlines=True)
    output = process.stdout
    if process.returncode != 0:
        return {'result': False, 'output': output}
    else:
        return {'result': True, 'output': output}


def get_file(file, destination, username, passwrd, host):
    cmd = [] if passwrd is None else ["sshpass", "-p", passwrd]
    cmd += [
        "scp",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-o",
        "VerifyHostKeyDNS=no",
        f"{user}@{host}:{file}",
        destination
    ]
    process = run(cmd, stdout=PIPE, universal_newlines=True)
    output = process.stdout
    if process.returncode != 0:
        return {'result': False, 'output': output}
    else:
        return {'result': True, 'output': output}


def RC_TEST(command):
    process = run(command, shell=True)
    if process.returncode != 0:
        return False
    else:
        return True


def return_output(command):
    process = Popen(command, shell=True, stdout=PIPE, universal_newlines=True)
    output = process.stdout.readlines()
    if len(output) == 0:
        return None
    else:
        return output[0].strip()


def cmd_test(command):
    process = run(command, shell=True, stdout=PIPE, universal_newlines=True)
    output = process.stdout
    if process.returncode != 0:
        return {'result': False, 'output': output}
    else:
        return {'result': True, 'output': output}


def start_ssh_agent():
    process = run(['ssh-agent', '-s'], stdout=PIPE, universal_newlines=True)
    to_recompile = 'SSH_AUTH_SOCK=(?P<socket>[^;]+).*SSH_AGENT_PID=(?P<pid>\d+)'
    OUTPUT_PATTERN = re.compile(to_recompile, re.MULTILINE | re.DOTALL)
    match = OUTPUT_PATTERN.search(process.stdout)
    if match is None:
        return False
    else:
        agentData = match.groupdict()
        os.environ['SSH_AUTH_SOCK'] = agentData['socket']
        os.environ['SSH_AGENT_PID'] = agentData['pid']
        return True


def is_agent_setup():
    return os.environ.get('SSH_AUTH_SOCK') is not None


def setup_ssh_agent():
    if is_agent_setup():
        return True
    else:
        return start_ssh_agent()


def create_key(keyPath):
    process = run('ssh-keygen -t rsa -f %s -q -N ""' % keyPath, shell=True)
    if process.returncode != 0:
        return False
    else:
        return True


def if_key_listed():
    process = run('ssh-add -L', shell=True)
    if process.returncode != 0:
        return False
    else:
        return True


def add_ssh_key(keyPath):
    process = run(['ssh-add', keyPath])
    if process.returncode != 0:
        return False
    else:
        return True


def vm_state(vm_name):
    cmd = f'vm info {vm_name} | grep state:'
    process = run(cmd, shell=True, stdout=PIPE, universal_newlines=True)
    output = process.stdout
    return output.partition(':')[2].strip()


def vm_start(vm_name):
    cmd = ['vm', 'start', vm_name]
    process = run(cmd)
    if process.returncode != 0:
        return False
    else:
        return True


def ping_host(host, count):
    process = run(['ping', '-c', f'{count}', host])
    if process.returncode != 0:
        return False
    else:
        return True


def wait_on_job(job_id, max_timeout):
    global job_results
    timeout = 0
    while True:
        job_results = GET(f'/core/get_jobs/?id={job_id}')
        job_state = job_results.json()[0]['state']
        if job_state in ('RUNNING', 'WAITING'):
            sleep(5)
        elif job_state in ('SUCCESS', 'FAILED'):
            return {'state': job_state, 'results': job_results.json()[0]}
        if timeout >= max_timeout:
            return {'state': 'TIMEOUT', 'results': job_results.json()[0]}
        timeout += 5


def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                     hosttarget, port, txtRecord):
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    results.update({
        'fullname': fullname,
        'hosttarget': hosttarget,
        'port': port,
        'txtrecord': txtRecord
    })


# Example of hostname is 'freenas', domain is 'local' regtype is '_middleware._tcp.'
def dns_service_resolve(hostname=None, domain=None, regtype=None):
    results.clear()
    resolved.clear()
    resolve_sdRef = pybonjour.DNSServiceResolve(0, pybonjour.kDNSServiceInterfaceIndexAny, hostname, regtype, domain, resolve_callback)
    try:
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], 1)
            if resolve_sdRef not in ready[0]:
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()
    if results == {}:
        return {'status': False, 'results': results}
    else:
        return {'status': True, 'results': results}
