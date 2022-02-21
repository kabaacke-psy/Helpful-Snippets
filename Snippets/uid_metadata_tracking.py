# @Authors: 
#   Kyle Baacke; kbaacke2@illinois.edu; https://github.com/kabaacke-psy
# @DateCreated: 02/07/2022
# @DateUpdated: 02/21/2022
# Description:
#   There are at least as many naming conventions for files as there are researchers. Contrary to most naming conventions using abbreviations stringed together, this snippit describes a way to track as many researcher degrees of freedom (analysis metadata) as you would like, without lengthening the file name. Instead of attaching this metadata information to each file by embedding the information in the filename, the prefix or suffix on the filename is a unique identifier {UID} that points to a separate metadata file. This metadata file ({UID}_metadata.json) can then contain as many key, value pairs as you want for any given pipeline. This removes any enticement to limit the number of metadata attributes saved on each run, further enabling reproducibility and clarity in analytical choices.

# 0) Setup
import json
import hashlib
import os
import pandas as pd
# Get the file deliminer for the OS you are working on
sep = os.path.sep
# Get the folder containing your python script
source_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + sep

# 1) Generate metadata dictionary
# Your metadata will initially be stored as a python dictionary containing key, value pairs 
metadata = {
  # The objects can be base python classes like strings, lists, integers, and bools. Do not use Pandas DataFrame objects
  'atlas_name':'Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm',
  'confounds': [
    "Movement_RelativeRMS",
    "trans_x_dt", "trans_y_dt", "trans_z_dt",
    "rot_x_dt", "rot_y_dt", "rot_z_dt",
    "trans_dx_dt", "trans_dy_dt", "trans_dz_dt",
    "rot_dx_dt", "rot_dy_dt", "rot_dz_dt"
  ],
  'n_parcels':200,
  'smoothed':False
}

# You can also add values to the dictionary after it has been created 
metadata['Note'] = 'This is an additional note'

# 2) Generate the unique identifier for the run
# Once you have settled on the metadata that you will use for that run, you can use the 
dhash = hashlib.md5()
encoded = json.dumps(metadata, sort_keys=True).encode()
dhash.update(encoded)
# You can change the 8 value to change the number of characters in the unique id via truncation.
run_uid = dhash.hexdigest()[:8]

# 3) Save metadata file
# Create an output folder (out_dir)
try:
  out_dir = f'{source_path}Output{sep}{run_uid}{sep}'
  os.makedirs(out_dir)
except:
  # Folder may already exist
  pass
with open(f'{out_dir}{run_uid}_metadata.json', 'w') as outfile:
  json.dump(metadata, outfile)

# Now, when you save any output, you can save it to the 'out_dir' directory.
# Additionally, you can save individual files with the unique identifier by including the run_uid in the filenames
dummy_output = pd.DataFrame()
dummy_output.to_csv(f'{out_dir}_empty_csv_example.csv', index=False)

# 4) Programatically read in the metadata file
# In addition to being able to read the metadata json objects in any text editor (e.g. notepad), you can also read the information in when using the output from an analysis.
metadata_2 = json.load(open(f'{out_dir}{run_uid}_metadata.json'))

