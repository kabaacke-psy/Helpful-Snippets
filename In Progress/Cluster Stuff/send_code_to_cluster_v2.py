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
base = f'S:\\\\Code\\MSC_HCP\\Data Managment\\'#f'/Users/cjrichier/Documents/GitHub/HCP-Analyses/'
dest_base = f'/data/r2-home/{username}/'#'/mnt/usb1/Code/'

# shutil.make_archive(f'{base}MSC_HCP', 'zip', f'{base}MSC_HCP')

# archive_pattern = '{base}MSC_HCP.zip'
archive_patterns = [
  # '{base}{sep}MSC_HCP{sep}Parcellation{sep}aparc_aseg_parcellation_runtime.py',
  # '{base}{sep}MSC_HCP{sep}Parcellation{sep}seg_to_npy_msc.job',
  # '{base}{sep}MSC_HCP{sep}Parcellation{sep}seg_to_npy_hcp.job',
  '{base}SGE_test.sh'
]
# psswd = getpass.getpass(f'Password for {username}@{hostname}:')
start_time = dt.datetime.now()
ssh = createSSHClient(f'{hostname}', 22, f'{username}', getpass.getpass(f'Password for {username}@{hostname}:'))
scp = SCPClient(ssh.get_transport())

for pattern in archive_patterns:
  scp.put(pattern.format(base = base, sep=sep), pattern.format(base = dest_base, sep=dest_sep))

end_time = dt.datetime.now()
print('Done. Runtime: ', end_time - start_time)
