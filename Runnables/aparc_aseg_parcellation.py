#!/usr/bin/env python3
import os
import nibabel as nib
from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker
from nilearn.input_data import NiftiMapsMasker
import datetime as dt
import argparse
import pandas as pd
import json
import hashlib
import numpy as np
import sys

sep = os.path.sep
source_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + sep
reference_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Resources','Parcellation')) + sep

def parse_args(args):
  parser = argparse.ArgumentParser(
      description='Converts files from .nii or .nii.gz to numpy files representing the BOLD timeseries within ROIs defined by a a segmentation file (aparc+aser.nii.gz) and a reference file specifying which values are to be used.\n\nAll extra arguments will be passes as Notes values in the meta-data json file.\n Example: \n\tpython3 /data/r2-home/kbaacke/usb1/Code/MSC_HCP/Parcellation/aparc_aseg_parcellation_runtime.py -input /mnt/usb1/HCP_1200/100307/MNINonLinear/Results/tfMRI_MOTOR_RL/tfMRI_MOTOR_RL.nii.gz -seg_path /mnt/usb1/HCP_1200/100307/MNINonLinear/aparc+aseg.nii.gz --metadata /data/r2-home/kbaacke/usb1/ \'No ICA-Aroma\''
    )
  parser.add_argument(
    "-input", help='Input nifty file.',required=True
  )
  parser.add_argument(
    "--output", help='Directory in which to store the output numpy file.\nIf None, numpy files will be saved in the same directory as the input file.', required=False
  )
  parser.add_argument(
    "--metadata", help='Directory in which to store the json file with information about parcellation options.\nIf None, numpy files will be saved in the same directory as the input file.\n*It is strongly reccomended to choose a base directory, not a subject directory. Choosing a subject directory will result in many json files being generated.',required=False
  )
  parser.add_argument(
    "--selection_path",
    help=f'Path to the .xlsx file indicating which values to use. Default is {reference_path}',
    required=False, default=reference_path
  )
  
  parser.add_argument(
    "-seg_path",
    help='''
      Path to segmentation file (/.../aparc+aseg.nii.gz)
    '''
  )
  parser.add_argument(
    '--confounds',
    help='''
      Optional. Path to .csv file containing motion and noise regressors.
    ''', required=False
  )
  parser.add_argument(
    '--confound_subset',
    help='''
      USe this to selecet a subset of the columns in the --confounds .csv file
    ''',nargs='*',required=False
  )
  return parser.parse_known_args(args)

def parsellate_aparc_aseg(nifty_file, aparc_fname, confounds=None):
  # Read in functional image
  raw_timeseries = nib.load(nifty_file)
  # Read in aprac+aseg.nii.gz file
  aparc = nib.load(aparc_fname)
  # Extract data from the aparc file
  aparc_array = np.array(aparc.dataobj)
  # Read in dataframe labeling which values to consider
  value_df = pd.read_excel(f'{args.reference_path}FreeSurferColorLUT_ValuesIn_aparc+aseg.xlsx')
  # Extract labels to put in meta_dict for later use
  labels_to_use = list(value_df.loc[value_df['Use']==1, 'Label'])
  # ID values to set to 0 (to exclude)
  values_not_to_use = list(value_df.loc[value_df['Use']!=1, '#No.'])
  for val in values_not_to_use:
    aparc_array = np.where(aparc_array == float(val), 0, aparc_array)
  # Generate new image object with filtered data
  aparc_aseg_filt = nib.Nifti1Image(aparc_array, aparc.affine, aparc.header)
  # Make masker object with new image object
  masker = NiftiLabelsMasker(labels_img=aparc_aseg_filt, standardize=True)
  masked_timeseries = []
  # Convert to numpy array with fit_transform
  if confounds is not None:
    masked_timeseries = masker.fit_transform(raw_timeseries, confounds=confounds)
  else:
    masked_timeseries = masker.fit_transform(raw_timeseries)
  return masked_timeseries

# if __name__=='__main__':
start_time = dt.datetime.now()
args, leftovers = parse_args(
  sys.argv[1:]
)
value_df = pd.read_excel(f'{args.reference_path}FreeSurferColorLUT_ValuesIn_aparc+aseg.xlsx')
# Extract labels to put in meta_dict for later use
labels_to_use = list(value_df.loc[value_df['Use']==1, 'Label'])

# Generate meta-dict
meta_dict = {
  'atlas_name' : 'MNINonLinear/aparc+aseg.nii.gz',
  'Labels':labels_to_use,
}
if args.confounds is not None:
  try:
    conf = pd.read_csv(args.confounds)
  except:
    raise Exception(f'Confounds file \'{args.confounds}\' not found.')
  if args.confound_subset is not None:
    try:
      conf = conf[args.confound_subset]
    except Exception as e:
      print(f'Error selecting confound columns: {e}')
  meta_dict['confounds'] = list(conf.columns)
else:
  meta_dict['confounds'] = None
  conf = None
if leftovers is not None:
  note_ind = 1
  for arg in leftovers:
    meta_dict[f'Note_{note_ind}'] = arg
    note_ind+=1

dhash = hashlib.md5()
encoded = json.dumps(meta_dict, sort_keys=True).encode()
dhash.update(encoded)
run_uid = dhash.hexdigest()[:8]

if args.output is not None:
  out_dir = args.output.replace('/', sep)
  try:
    os.makedirs(out_dir)
  except:
    pass
else:
  out_dir = os.path.dirname(args.input)

if '.nii.gz' in args.input:
  numpy_name = run_uid + '_' + os.path.basename(args.input)[:-7]
else:
  numpy_name = run_uid + '_' + os.path.basename(args.input)[:-4]
numpy_filepath = out_dir + sep + numpy_name

if args.metadata is not None:
  base_path = os.path.dirname(args.metadata)
  with open(base_path + sep + run_uid + '_parcellation-metadata.json', 'w') as outfile:
    json.dump(meta_dict, outfile)
else:
  base_path = os.path.dirname(args.input)
  try:
    os.makedirs(base_path.replace('/', sep))
  except:
    pass
  with open(base_path + sep + run_uid + '_parcellation-metadata.json', 'w') as outfile:
    json.dump(meta_dict, outfile)

ts = parsellate_aparc_aseg(args.input, args.seg_path, confounds = conf)

np.save(numpy_filepath, ts)

end_time = dt.datetime.now()
print('Parcellation complete. Runtime: {}\nOutput File: {}\nMetadata: {}'.format(str(end_time-start_time), numpy_filepath, str(base_path + sep + run_uid + '_parcellation-metadata.json')))