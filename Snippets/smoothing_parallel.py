from nilearn import plotting, image
import datetime as dt
import os
from joblib import Parallel, delayed
sep = os.path.sep

OUTDIR= sep + sep + 'dt1' + sep + 'S' + sep + 'MSC' + sep + 'ds000224-Output'
OUTDIR_hcp = sep + sep + 'dt1' + sep + 'S' + sep + 'HCP' + sep + 'HCP_1200'
#OUTDIR2= sep +sep + 'dt1' + sep + 'S' + sep + 'MSC' + sep + 'ds000224-Output-ICA-AROMA'
#SUBJECT='sub-MSC01'
#TIME='func01'
#RUN='task-motor_run-01_bold'
MSC_Subject_List = [
  'sub-MSC01', 'sub-MSC02', 'sub-MSC03', 'sub-MSC04', 'sub-MSC05',
  'sub-MSC06', 'sub-MSC07', 'sub-MSC08', 'sub-MSC09', 'sub-MSC10'
  ]
HCP_subject_list = os.listdir('\\\\dt1\\S\\HCP\\HCP_1200\\')
MSC_Session_list = [
  'ses-func01', 'ses-func02', 'ses-func03', 'ses-func04', 'ses-func05',
  'ses-func06', 'ses-func07', 'ses-func08', 'ses-func09', 'ses-func10'
  ]
HCP_Session_list = [
    # "tfMRI_MOTOR",
    "tfMRI_WM"#,
    # "tfMRI_EMOTION",
    # "tfMRI_GAMBLING",
    # "tfMRI_LANGUAGE",
    # "tfMRI_RELATIONAL",
    # "tfMRI_SOCIAL"
  ]
MSC_Run_list = ['task-motor_run-01_bold', 'task-motor_run-02_bold']
HCP_Run_list = ['RL','LR']

msc_pth = '{OUTDIR}' + sep + '{SUBJECT}' + sep + 'MNINonLinear' + sep + 'Results' + sep + '{TIME}_{RUN}' + sep + '{TIME}_{RUN}.nii.gz'
msc_output_path = '{OUTDIR}' + sep + '{SUBJECT}' + sep + 'MNINonLinear' + sep + 'Results' + sep + '{TIME}_{RUN}' + sep + '{TIME}_{RUN}_nilearn-smoothed.nii.gz'

def smooth_subject(SUBJECT):
  size_list = []
  for TIME in HCP_Session_list:
    for RUN in HCP_Run_list:
      try:
        smooth_img = image.smooth_img(
          msc_pth.format(
            OUTDIR = OUTDIR_hcp,
            SUBJECT = SUBJECT,
            TIME = TIME,
            RUN = RUN,
          ),
          6
        )
        smooth_img.to_filename(
          msc_output_path.format(
            OUTDIR = OUTDIR_hcp,
            SUBJECT = SUBJECT,
            TIME = TIME,
            RUN = RUN,
          )
        )
        size_list.append(os.path.getsize(msc_output_path.format(
            OUTDIR = OUTDIR_hcp,
            SUBJECT = SUBJECT,
            TIME = TIME,
            RUN = RUN,
          ))
        )
      except:
        print('File not found: ' + msc_pth.format(
                OUTDIR = OUTDIR_hcp,
                SUBJECT = SUBJECT,
                TIME = TIME,
                RUN = RUN,
                )
              )
  return sum(size_list)

if __name__=='__main__':
  start_time = dt.datetime.now()
  size_list = Parallel(n_jobs=6)(delayed(smooth_subject)(SUBJECT) for SUBJECT in HCP_subject_list[255:])
  end_time = dt.datetime.now()
  print('Done. ', end_time-start_time, round(float(sum(size_list))/1000000000.0, 4), ' GB')
