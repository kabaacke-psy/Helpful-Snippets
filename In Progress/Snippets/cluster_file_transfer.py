# @Authors: 
#   Kyle Baacke; kbaacke2@illinois.edu; https://github.com/kabaacke-psy
# @DateCreated: 02/07/2022
# @DateUpdated: 02/07/2022
# Description:
#   {DESCRIPTION}
# Notes and Qualifiers:
#   {NOTES}
# You may want to transfer a file or list of files to or from the cluster without using a physical drive. This can be accomplished over SSH using SCP. Alternatively, you can run SCP via python in order to streamline your analysis or data management processes.

# You will need the following python packages

import os
import shutil
import datetime as dt
import paramiko
from scp import SCPClient
import zipfile # Only required if you want to zip before sending
import getpass # Used for getting password from the user in a prompt rather than having your password in the code (which is a very, very bad practice)

# The following line is ot enable the script to work on all opreating systems by dynamically assigning what the file deliminer will be.
sep = os.path.sep

# This line is to specify what the deliminer is on the remote system. Since the cluster is linux, the following should always work
remote_sep = '/'

# The following function will create a virtual SSH session to be used ot call the SCP commands.
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


