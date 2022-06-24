import os
import shutil
import datetime as dt
import pandas as pd
import paramiko
from scp import SCPClient
import zipfile
import getpass
username = 'kbaacke'#'corey'
hostname = 'hx.psych.uiuc.edu'

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

sep = os.path.sep
dest_sep = '/'
source_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + sep
base = f'S:\\\\MSC\\'#f'/Users/cjrichier/Documents/GitHub/HCP-Analyses/'
dest_base = f'/data/hx-hx1/{username}/datasets/MSC/'#'/mnt/usb1/Code/'


file_patterns = [
  (
    '{base}ds000224-Output{sep}sub-MSC02{sep}MNINonLinear{sep}Results{sep}ses-{time}_task-{task}_bold{sep}ses-{time}_task-{task}_bold.nii.gz', 
    '{base}ds000224-Output{sep}sub-MSC02{sep}MNINonLinear{sep}Results{sep}ses-{time}_task-{task}_bold{sep}ses-{time}_task-{task}_bold.nii.gz'
  )
]

times = [
  # 'func01', 'func02', 
  'func03', 'func04', 'func05', 
  'func06', 'func07', 'func08', 'func09', 'func10'
]

tasks = [
  # 'motor_run-01',
  # 'motor_run-02',
  'glasslexical_run-01',
  'glasslexical_run-02',
  'memoryfaces',
  'memoryscenes',
  'memorywords',
  'memoryfaces',
]

start_time = dt.datetime.now()
ssh = createSSHClient(f'{hostname}', 22, f'{username}', getpass.getpass(f'Password for {username}@{hostname}:'))
scp = SCPClient(ssh.get_transport())

for pattern in file_patterns:
  for time in times:
    for task in tasks:
      try:
        print(
          pattern[0].format(base = base, sep=sep, task=task, time=time),
          ' --> ',
          pattern[1].format(base = dest_base, sep=dest_sep, task=task, time=time)
        )
        scp.put(
          pattern[0].format(base = base, sep=sep, task=task, time=time),
          pattern[1].format(base = dest_base, sep=dest_sep, task=task, time=time)
        )
      except Exception as e:
        print(e)


end_time = dt.datetime.now()
print('Done. Runtime: ', end_time - start_time)


