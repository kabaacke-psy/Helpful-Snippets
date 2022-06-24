import os
import shutil
import datetime as dt
import pandas as pd
import paramiko
from scp import SCPClient
import zipfile
import getpass
username = 'kbaacke'#'corey'
hostname = 'r2.psych.uiuc.edu'

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

sep = os.path.sep
dest_sep = '/'
source_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + sep
base = f'S:\\\\Code\\'#f'/Users/cjrichier/Documents/GitHub/HCP-Analyses/'
dest_base = f'/data/hx-hx1/kbaacke/Code/'#'/mnt/usb1/Code/'


file_patterns = [
  (
    '{base}Helpful-Snippets{sep}In Progress{sep}Cluster Stuff{sep}MSC_Parcellation_v2.sh', 
    '{base}MSC_Parcellation_v2.sh'
  ),(
    '{base}Helpful-Snippets{sep}In Progress{sep}Cluster Stuff{sep}MSC_Parcellation_v3.sh', 
    '{base}MSC_Parcellation_v3.sh'
  )
  #,
  #,
]
# directory_patterns = [
#   (
#     '{base}MSC_HCP{sep}Parcellation{sep}','{base}Parcellation{sep}'
#   )#,
# ]

start_time = dt.datetime.now()
ssh = createSSHClient(f'{hostname}', 22, f'{username}', getpass.getpass(f'Password for {username}@{hostname}:'))
scp = SCPClient(ssh.get_transport())

for pattern in file_patterns:
  print(pattern[0].format(base = base, sep=sep), ' --> ', pattern[1].format(base = dest_base, sep=dest_sep))
  scp.put(pattern[0].format(base = base, sep=sep), pattern[1].format(base = dest_base, sep=dest_sep))

# for pattern in directory_patterns:
#   print(pattern[0].format(base = base, sep=sep), ' --> ', pattern[1].format(base = dest_base, sep=dest_sep))
#   scp.put(pattern[0].format(base = base, sep=sep), pattern[1].format(base = dest_base, sep=dest_sep), recursive=True)

end_time = dt.datetime.now()
print('Done. Runtime: ', end_time - start_time)
