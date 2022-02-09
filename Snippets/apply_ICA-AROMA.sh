# @Authors: 
#   Kyle Baacke; kbaacke2@illinois.edu; https://github.com/kabaacke-psy
# @DateCreated: 02/07/2022
# @DateUpdated: 02/07/2022
# Description:
#   {DESCRIPTION}
# Notes and Qualifiers:
#   {NOTES}


FREESURFER_HOME=/home/kyle/freesurfer
FSLDIR=/home/kyle/fsl
OUTDIR=/mnt/s/HCP/HCP_1200
OUTDIR2=/mnt/s/HCP/HCP_1200_ICA-AROMA
source $FREESURFER_HOME/SetUpFreeSurfer.sh

ica_aroma(){
  local subject=$1
  local time=$2
  local run=$3
  echo 'Start time:'
    date "+%T"
    echo ${OUTDIR}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}_nilearn-smoothed.nii.gz
    if test -d ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}; then
      echo "${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run} already created"
    else
      mkdir ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}
    fi
    
    python2 ~/ICA-AROMA/ICA_AROMA.py -in ${OUTDIR}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}_nilearn-smoothed.nii.gz \
      -out ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA \
      -mc ${OUTDIR}/${subject}/MNINonLinear/Results/${time}_${run}/Movement_Regressors_6.par \
      -m ${OUTDIR}/${subject}/MNINonLinear/Results/${time}_${run}/brainmask_fs.2.nii.gz 
    if [ -f ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA.nii.gz ]; then
      echo "  ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA.nii.gz already created."
    else
      echo 'Start time:'
      date "+%T"
      fsl_regfilt -i ${OUTDIR}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}.nii.gz \
        -f $(cat ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA/classified_motion_ICs.txt) \
        -d ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA/melodic.ica/melodic_mix \
        -o ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA.nii.gz
      echo 'End time:'
      date "+%T"
    fi
    fslmeants -i ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA.nii.gz \
      -o ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA/${time}_${run}_WMnoise-nonsmoothed.1D \
      -m ${OUTDIR2}/${subject}/MNINonLinear/${subject}_wm-resample.nii.gz
    fslmeants -i ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA.nii.gz \
      -o ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA/${time}_${run}_CSFnoise-nonsmoothed.1D \
      -m ${OUTDIR2}/${subject}/MNINonLinear/${subject}_ventricles-resample.nii.gz
    3dTproject -input ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA.nii.gz \
      -prefix ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA-denoised-nonsmoothed.nii.gz \
      -ort ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA/${time}_${run}_WMnoise-nonsmoothed.1D \
      -ort ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/ICA_AROMA/${time}_${run}_CSFnoise-nonsmoothed.1D \
      -polort 1 \
      -passband 0.01 0.08 \
      -automask
    echo 'End time:'
    date "+%T"
}

FILENAME=/mnt/s/HCP/HCP_subject_list_subset_1.txt
N=7
for SUBJECT_LINE in $(cat $FILENAME); do
  SUBJECT=$(echo $SUBJECT_LINE | sed -e 's/\r//g')
  echo $SUBJECT
  for RUN in RL LR; do
    for TIME in tfMRI_WM; do
      ica_aroma "$SUBJECT" "$TIME" "$RUN" &
      if [[ $(jobs -r -p | wc -l) -ge $N ]]; then 
        wait -n #Only continue if the number of active jobs is less than $N
      fi
    done
  done
done

# SUBLIST=$( ls ${SUBDIR} | grep 'sub-*' )
# for SUBJECT in $SUBLIST; do