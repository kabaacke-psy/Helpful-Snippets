cd /mnt/s/Code/MSC_HCP/Parcellation
parcellate(){
  local subject=$1
  local time=$2
  local run=$3
  echo ${OUTDIR2}/${subject}/MNINonLinear/Results/ses-${time}_${run}/${time}_${run}-AROMA-denoised-nonsmoothed.nii.gz
  python3 /mnt/s/Code/MSC_HCP/Parcellation/nifty2numpy_parcellation.py \
    echo ${INDIR}/${subject}/MNINonLinear/Results/ses-${time}_task-${task}_bold/ses-${time}_task-${task}_bold.nii.gz \
    --output ${OUTDIR}/${subject}/MNINonLinear/Results/ses-${time}_task-${task}_bold/ \
    -atlas $ATLAS \
    --metadata ${OUTDIR} \
    'No Smoothing, no Confounds'
}


INDIR=/mnt/s/MSC/ds000224-Output
OUTDIR==/mnt/s/MSC/ds000224-Parcellation
SUBJECT='sub-MSC02'
N=10
for TIME in func01 func02 func03 func04 func05 func06 func07 func08 func09 func10; do
  for RUN in motor_run-01 motor_run-02 glasslexical_run-01 glasslexical_run-02 memoryfaces memoryscenes memorywords; do
    parcellate "$SUBJECT" "$TIME" "$RUN" &
    if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
      wait -n
    fi
  done
done