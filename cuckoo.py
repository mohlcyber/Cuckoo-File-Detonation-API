import os
import sys
import requests
import time
import json

def upload(cuckoo_url, file):

    with open(file, "rb") as sample:
        path, filename = os.path.split(file)
        files = {"file": (filename, sample)}
        r = requests.post(cuckoo_url + '/tasks/create/file', files=files)

    if r.status_code <> 200:
        print('Something went wrong')

    try:
        taskid = r.json()['task_id']
    except Exception as e:
        print('Something went wrong {0}'.format(e))

    return taskid

def status(cuckoo_url, taskid):

    r = requests.get(cuckoo_url + '/tasks/view/{0}'.format(taskid))

    status = r.json()['task']['status']
    return status

def report(cuckoo_url, taskid):

    r = requests.get(cuckoo_url + '/tasks/report/{0}'.format(taskid))
    report = json.dumps(r.json())
    return report

if __name__ == "__main__":

    cuckoo_url = 'http://ip:8090'
    file = 'path to file'

    taskid = upload(cuckoo_url, file)
    print('Created new task with taskid {0}'.format(taskid))

    while True:
        process = status(cuckoo_url, taskid)
        if process == 'pending' or process == 'running':
            print('File analysis is {}'.format(process))
            time.sleep(30)
            pass
        elif process == 'completed':
            print('File analysis completed, not reported yet')
            time.sleep(30)
            pass
        elif process == 'reported':
            print('File analysis completed and reported - done')
            break

    report = report(cuckoo_url, taskid)
    print(report)

    print('done')
