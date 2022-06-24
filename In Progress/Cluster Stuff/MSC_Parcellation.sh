#!/bin/bash
subject=$1
time=$2
task=$3
ATLAS=$4
notes=$5

INDIR=/data/hx-hx1/kbaacke/datasets/MSC/ds000224-Output
OUTDIR=/data/hx-hx1/kbaacke/datasets/MSC/ds000224-Parcellation

echo ${INDIR}/${subject}/MNINonLinear/Results/ses-${time}_task-${task}_bold/ses-${time}_task-${task}_bold.nii.gz
python3 /data/hx-hx1/kbaacke/Code/Parcellation/nifty2numpy_parcellation.py \
  -input ${INDIR}/${subject}/MNINonLinear/Results/ses-${time}_task-${task}_bold/ses-${time}_task-${task}_bold.nii.gz \
  --output ${OUTDIR}/${subject}/MNINonLinear/Results/ses-${time}_task-${task}_bold/ \
  -atlas $ATLAS \
  --metadata ${OUTDIR} \
  $notes





