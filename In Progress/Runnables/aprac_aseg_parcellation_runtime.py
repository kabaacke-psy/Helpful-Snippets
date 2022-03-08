import os
import nibabel as nib
from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker
from nilearn.input_data import NiftiMapsMasker
import datetime as dt
import argparse
import pandas as pd
import json # Not on Cluster
import hashlib # Not on Cluster
import numpy as np
import sys

sep = os.path.sep
source_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + sep

def parse_args(args):
  parser = argparse.ArgumentParser(
      description='Converts files from .nii or .nii.gz to numpy files based on parcellation atlasses.\nAll Parcellations are based on the assumption of FSLMNI_152 space input files.\nAll extra arguments will be passes as Notes values in the meta-data json file.\n Example: \n\tpython3 nifty2numpy_parcellation.py -input S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\ses-func01_task-motor_run-01_bold.nii.gz -atlas Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm --confounds S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\sub-MSC01_ses-func01_01_full-confounds.csv --confound_subset Movement_RelativeRMS --metadata S:\\MSC\\ds000224-Output\\ \'Example note for netadata json\''
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
  value_df = pd.read_excel(f'{source_path}FreeSurferColorLUT_ValuesIn_aparc+aseg.xlsx')
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
value_df = pd.read_excel(f'{source_path}FreeSurferColorLUT_ValuesIn_aparc+aseg.xlsx')
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