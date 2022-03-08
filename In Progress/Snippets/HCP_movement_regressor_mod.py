import pandas as pd
import re
import numpy as np
import os
import datetime as dt

sep = os.path.sep

df1 = pd.read_csv('S:\\MSC\\ds000224-Output\\sub-MSC01\\ses-func01_task-motor_run-01_bold\\Movement_Regressors.txt', sep = '\t', header=None)

def convert_hcp_movement_regressors(input_path, output_path=None, subset_path = None, original_columns = 12, new_columns = 6):
  df1 = pd.read_csv(input_path, sep = '\t', header=None)
  df1.columns = ['full']
  # Define lambda function to extract foloat value patterns from a varying length substrings 
  def extract_float(source_string, start_index):
    return float(re.search(('[\w]*([-]*[0-9].+?[0-9])[\w]*'), source_string[start_index:]).group(0))
  # Utility function to keep track of the positions of the last substing extracted
  def update_start_ind(source_string, start_index):
    return re.search(('[\w]*([-]*[0-9].+?[0-9])[\w]*'), source_string[start_index:]).span()[1] + start_index
  df1['start_ind'] = 0 
  for x in range(original_columns):
    df1[str(x)] = df1.apply(lambda row: extract_float(row['full'], row['start_ind']), axis=1)
    df1['start_ind'] = df1.apply(lambda row: update_start_ind(row['full'], row['start_ind']), axis=1)
  # Save optional output files
  if output_path is not None:
    #df1[df1.columns[2:]].to_csv(output_path, sep = '\t', header=None, index=False)
    np.savetxt(output_path, df1[df1.columns[2:]], delimiter = '  ', fmt='%f')
  if subset_path is not None:
    #df1[df1.columns[2:(new_columns+2)]].to_csv(subset_path, sep = '\t', header=None, index=False)
    np.savetxt(subset_path, df1[df1.columns[2:(new_columns+2)]], delimiter = '  ', fmt='%f')
  return df1[df1.columns[2:]], df1[df1.columns[2:(new_columns+2)]]

if __name__ == '__main__':
  # input_path_example = 'S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\Movement_Regressors.txt'
  # output_path_example = 'S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\Movement_Regressors.par'
  # subset_example_path = 'S:\\MSC\\ds000224-Output\\sub-MSC01\\MNINonLinear\\Results\\ses-func01_task-motor_run-01_bold\\Movement_Regressors_6.par'
  start_time = dt.datetime.now()

  input_msc_pth = '{OUTDIR}' + sep + '{SUBJECT}' + sep + 'MNINonLinear' + sep + 'Results' + sep + '{TIME}_{RUN}' + sep + 'Movement_Regressors.txt'
  output_msc_pth = '{OUTDIR}' + sep + '{SUBJECT}' + sep + 'MNINonLinear' + sep + 'Results' + sep + '{TIME}_{RUN}' + sep + 'Movement_Regressors.par'
  subset_msc_pth = '{OUTDIR}' + sep + '{SUBJECT}' + sep + 'MNINonLinear' + sep + 'Results' + sep + '{TIME}_{RUN}' + sep + 'Movement_Regressors_6.par'

  HCP_subject_list = os.listdir('S:\\HCP\\HCP_1200_NumPy\\')
  HCP_Session_list = [
    # "tfMRI_MOTOR"
    "tfMRI_WM",
    "tfMRI_EMOTION",
    "tfMRI_GAMBLING",
    "tfMRI_LANGUAGE",
    "tfMRI_RELATIONAL",
    "tfMRI_SOCIAL"
  ]
  HCP_Run_list = ['RL','LR']

  MSC_Subject_List = [
    'sub-MSC01', 'sub-MSC02', 'sub-MSC03', 'sub-MSC04', 'sub-MSC05',
    'sub-MSC06', 'sub-MSC07', 'sub-MSC08', 'sub-MSC09', 'sub-MSC10'
    ]
  MSC_Session_list = [
    'ses-func01', 'ses-func02', 'ses-func03', 'ses-func04', 'ses-func05',
    'ses-func06', 'ses-func07', 'ses-func08', 'ses-func09', 'ses-func10'
    ]

  MSC_Run_list = ['task-motor_run-01_bold', 'task-motor_run-02_bold']
  OUTDIR= 'S:' + sep + 'MSC' + sep + 'ds000224-Output'
  OUTDIR_hcp = 'S:' + sep + 'HCP' + sep + 'HCP_1200'

  # for SUBJECT in [MSC_Subject_List[0]]:
  #   for TIME in MSC_Session_list:
  #     for RUN in MSC_Run_list:
  #       try:
  #         # print(input_msc_pth.format(OUTDIR = OUTDIR,SUBJECT = SUBJECT,TIME = TIME,RUN = RUN))
  #         # print(output_msc_pth.format(OUTDIR = OUTDIR,SUBJECT = SUBJECT,TIME = TIME,RUN = RUN))
  #         # print(subset_msc_pth.format(OUTDIR = OUTDIR,SUBJECT = SUBJECT,TIME = TIME,RUN = RUN))
  #         new_df, subset_df = convert_hcp_movement_regressors(
  #           input_msc_pth.format(
  #             OUTDIR = OUTDIR,
  #             SUBJECT = SUBJECT,
  #             TIME = TIME,
  #             RUN = RUN
  #           ),
  #           output_path=output_msc_pth.format(
  #             OUTDIR = OUTDIR,
  #             SUBJECT = SUBJECT,
  #             TIME = TIME,
  #             RUN = RUN
  #           ), 
  #           subset_path=subset_msc_pth.format(
  #             OUTDIR = OUTDIR,
  #             SUBJECT = SUBJECT,
  #             TIME = TIME,
  #             RUN = RUN
  #           ))
  #       except Exception as e:
  #         print(e)

  for SUBJECT in HCP_subject_list:
    print(SUBJECT)
    for TIME in HCP_Session_list:
      for RUN in HCP_Run_list:
        try:
          # print(input_msc_pth.format(OUTDIR = OUTDIR,SUBJECT = SUBJECT,TIME = TIME,RUN = RUN))
          # print(output_msc_pth.format(OUTDIR = OUTDIR,SUBJECT = SUBJECT,TIME = TIME,RUN = RUN))
          # print(subset_msc_pth.format(OUTDIR = OUTDIR,SUBJECT = SUBJECT,TIME = TIME,RUN = RUN))
          new_df, subset_df = convert_hcp_movement_regressors(
            input_msc_pth.format(
              OUTDIR = OUTDIR_hcp,
              SUBJECT = SUBJECT,
              TIME = TIME,
              RUN = RUN
            ),
            output_path=output_msc_pth.format(
              OUTDIR = OUTDIR_hcp,
              SUBJECT = SUBJECT,
              TIME = TIME,
              RUN = RUN
            ), 
            subset_path=subset_msc_pth.format(
              OUTDIR = OUTDIR_hcp,
              SUBJECT = SUBJECT,
              TIME = TIME,
              RUN = RUN
            ))
        except Exception as e:
          print(e)
  
  end_time = dt.datetime.now()
  print('Done. ', end_time-start_time)