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

gen_masks(){
  local subject=$1
  if test -d ${OUTDIR}/${subject}; then
    echo "subject directory already created"
  else
    mkdir ${OUTDIR2}/${subject}
    mkdir ${OUTDIR2}/${subject}/MNINonLinear
    mkdir ${OUTDIR2}/${subject}/MNINonLinear/Results
  fi
  if [ -f ${OUTDIR2}/${subject}/MNINonLinear/${subject}_wm-resample.nii.gz ] && [ -f ${OUTDIR2}/${subject}/MNINonLinear/${subject}_ventricles-resample.nii.gz ]; then
    echo "   Individual masks already generated."
  else
    echo 'Generating Masks. Start Time:'
    date "+%T"
    mri_binarize --i ${OUTDIR}/${subject}/MNINonLinear/aparc+aseg.nii.gz \
      --ctx-wm \
      --o ${OUTDIR2}/${subject}/MNINonLinear/${subject}_wm.nii.gz

    flirt -in ${OUTDIR2}/${subject}/MNINonLinear/${subject}_wm.nii.gz \
      -ref $FSLDIR/data/standard/MNI152_T1_2mm \
      -applyxfm \
      -usesqform \
      -interp nearestneighbour \
      -interp nearestneighbour \
      -out ${OUTDIR2}/${subject}/MNINonLinear/${subject}_wm-resample.nii.gz
      

    mri_binarize --i ${OUTDIR}/${subject}/MNINonLinear/aparc+aseg.nii.gz \
      --ventricles \
      --o ${OUTDIR2}/${subject}/MNINonLinear/${subject}_ventricles.nii.gz

    flirt -in ${OUTDIR2}/${subject}/MNINonLinear/${subject}_ventricles.nii.gz \
      -ref $FSLDIR/data/standard/MNI152_T1_2mm \
      -applyxfm \
      -usesqform \
      -interp nearestneighbour \
      -interp nearestneighbour \
      -out ${OUTDIR2}/${subject}/MNINonLinear/${subject}_ventricles-resample.nii.gz
    echo 'End Time:'
    date "+%T"
  fi
}

FILENAME=/mnt/s/HCP/HCP_subject_list_subset_1.txt
N=7
for SUBJECT in $(cat $FILENAME); do
  gen_masks "$SUBJECT" &
  if [[ $(jobs -r -p | wc -l) -ge $N ]]; then 
    wait -n #Only continue if the number of active jobs is less than $N
  fi
done

# SUBLIST=$( ls ${SUBDIR} | grep 'sub-*' )
# for SUBJECT in $SUBLIST; do