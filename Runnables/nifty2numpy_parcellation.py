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

def parcellate_timeseries(nifty_file, atlas_name, confounds=None):
  # Other atlases in MNI found here: https://www.lead-dbs.org/helpsupport/knowledge-base/atlasesresources/cortical-atlas-parcellations-mni-space/
  raw_timeseries = nib.load(nifty_file)
  if atlas_name=='harvard_oxford':
    atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm', symmetric_split=True)
    atlas_filename = atlas.maps
    masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)
  elif atlas_name == 'msdl':
    atlas = datasets.fetch_atlas_msdl()
    atlas_filename = atlas.maps
    masker = NiftiMapsMasker(maps_img=atlas_filename, standardize=True, memory='nilearn_cache')
  elif 'yeo' in atlas_name:
    yeo = datasets.fetch_atlas_yeo_2011()
    if atlas_name == 'yeo_7_thin':
      masker = NiftiLabelsMasker(labels_img=yeo['thin_7'], standardize=True,memory='nilearn_cache')
    elif atlas_name == 'yeo_7_thick':
      masker = NiftiLabelsMasker(labels_img=yeo['thick_7'], standardize=True,memory='nilearn_cache')
    elif atlas_name == 'yeo_17_thin':
      masker = NiftiLabelsMasker(labels_img=yeo['thin_17'], standardize=True,memory='nilearn_cache')
    elif atlas_name == 'yeo_17_thick':
      masker = NiftiLabelsMasker(labels_img=yeo['thick_17'], standardize=True,memory='nilearn_cache')
  elif atlas_name == 'mni_glasser':
    atas_glasser_01_filename = source_path + 'MMP_in_MNI_corr.nii.gz' # Downlaoded from https://neurovault.org/collections/1549/
    masker = NiftiLabelsMasker(labels_img=atas_glasser_01_filename, standardize=True)
  elif 'Schaefer2018_' in atlas_name:
    atlas_filename = source_path + atlas_name + '.nii.gz'
    masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)
  else:
    return NotImplementedError
  #Transform the motor task imaging data with the masker and check the shape
  masked_timeseries = []
  if confounds is not None:
    masked_timeseries = masker.fit_transform(raw_timeseries, confounds = confounds)
  else:
    masked_timeseries = masker.fit_transform(raw_timeseries)
  return masked_timeseries

def parse_args(args):
  parser = argparse.ArgumentParser(
      description='Converts files from .nii or .nii.gz to numpy files representing the BOLD timeseries within ROIs defined by parcellation atlases. All parcellations are based on the assumption of FSLMNI_152_2MM space input files.\nAll extra arguments will be passes as Notes values in the meta-data json file.\n Example: \n\tpython3 nifty2numpy_parcellation.py -input S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\ses-func01_task-motor_run-01_bold.nii.gz -atlas Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm --confounds S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\sub-MSC01_ses-func01_01_full-confounds.csv --confound_subset Movement_RelativeRMS --metadata S:\\MSC\\ds000224-Output\\ \'Example note for netadata json\''
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
    "-atlas",
    help='''
      Use to specify which atlas to use. Options:
      harvard_oxford     From nilearn.datasets.fetch_atlas_harvard_oxford(\'cort-maxprob-thr25-2mm\'symmetric_split=True
      \'msdl\'                From nilearn.datasets.fetch_atlas_msdl().maps
      yeo_7_thin, yeo_7_thick, yeo_17_thin, yeo_17_thick  From nilearn.datasets.fetch_atlas_yeo_2011()
      mni_glasser         'MMP_in_MNI_corr.nii.gz' from https://neurovault.org/collections/1549/
      Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm,       Schaefer2018_100Parcels_17Networks_order_FSLMNI152_2mm,       Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm,       Schaefer2018_200Parcels_17Networks_order_FSLMNI152_2mm,       Schaefer2018_300Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_300Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_400Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_400Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_500Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_500Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_600Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_600Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_700Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_700Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_800Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_800Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_900Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_900Parcels_17Networks_order_FSLMNI152_2mm,      Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm,      Schaefer2018_1000Parcels_17Networks_order_FSLMNI152_2mm     From https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI
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

args, leftovers = parse_args(#['-h']
  sys.argv[1:]
  # [
  #   '-input',
  #   'S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\ses-func01_task-motor_run-01_bold.nii.gz',
  #   '-atlas',
  #   'Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm',
  #   '--confounds',
  #   'S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\sub-MSC01_ses-func01_01_full-confounds.csv',
  #   '--confound_subset',
  #   'Movement_RelativeRMS',
  #   '--metadata',
  #   'S:\\MSC\\ds000224-Output\\',
  #   'Example note for netadata json'
  # ]
)
#--confounds S:\MSC\ds000224-Output\sub-MSC01\MNINonLinear\Results\ses-func01_task-motor_run-01_bold\sub-MSC01_ses-func01_01_full-confounds.csv --confound_subset trans_x_dt trans_y_dt	trans_z_dt rot_x_dt rot_y_dt rot_z_dt trans_dx_dt trans_dy_dt trans_dz_dt rot_dx_dt rot_dy_dt rot_dz_dt Movement_RelativeRMS


start_time = dt.datetime.now()
meta_dict = {
    'atlas_name' : args.atlas,
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
if os.path.exists(numpy_filepath): #This does not work yet
  print(f'An analysis with this same metadata dictionary has been run: {run_uid}')
  print('Would you like to re-run? (y/n)')
  if not 'y' in input().lower():
    raise Exception('Analyses halted.')

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


ts = parcellate_timeseries(args.input, args.atlas, confounds = conf)

np.save(numpy_filepath, ts)

end_time = dt.datetime.now()
print('Parcellation complete. Runtime: {}\nOutput File: {}\nMetadata: {}'.format(str(end_time-start_time), numpy_filepath, str(base_path + sep + run_uid + '_parcellation-metadata.json')))