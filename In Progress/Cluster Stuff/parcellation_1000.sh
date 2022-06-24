source /usr/local/sge/default/common/settings.sh

dos2unix MSC_Parcellation_v2.sh

chmod u+x MSC_Parcellation_v2.sh

INDIR=/data/hx-hx1/kbaacke/datasets/MSC/ds000224-Output
#5384cc6b

for SUBJECT in 'sub-MSC01' 'sub-MSC02' 'sub-MSC03' 'sub-MSC04' 'sub-MSC05' 'sub-MSC06' 'sub-MSC07' 'sub-MSC08' 'sub-MSC09' 'sub-MSC10'; do
  for TIME in func01 func02 func03 func04 func05 func06 func07 func08 func09 func10; do
    for TASK in motor_run-01 motor_run-02; do
      qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N ${SUBJECT}_${TIME}_${TASK} /data/hx-hx1/kbaacke/Code/MSC_Parcellation_v2.sh ${INDIR}/${SUBJECT}/MNINonLinear/Results/ses-${TIME}_task-${TASK}_bold/ses-${TIME}_task-${TASK}_bold.nii.gz ${INDIR}/${SUBJECT}/MNINonLinear/Results/ses-${TIME}_task-${TASK}_bold/ "Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm" /data/hx-hx1/kbaacke/datasets/parcellation_metadata "No Smoothing, no Confounds"
    done
  done
done


INDIR=/data/hx-hx1/kbaacke/datasets/MSC/ds000224-Output-ICA-AROMA
#7e91a520

for SUBJECT in 'sub-MSC01' 'sub-MSC02' 'sub-MSC03' 'sub-MSC04' 'sub-MSC05' 'sub-MSC06' 'sub-MSC07' 'sub-MSC08' 'sub-MSC09' 'sub-MSC10'; do
  for TIME in func01 func02 func03 func04 func05 func06 func07 func08 func09 func10; do
    for TASK in motor_run-01 motor_run-02; do
      qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N ${SUBJECT}_${TIME}_${TASK} /data/hx-hx1/kbaacke/Code/MSC_Parcellation_v2.sh ${INDIR}/${SUBJECT}/MNINonLinear/Results/ses-${TIME}_task-${TASK}_bold/${TIME}_task-${TASK}_bold-AROMA-denoised-nonsmoothed.nii.gz ${INDIR}/${SUBJECT}/MNINonLinear/Results/ses-${TIME}_task-${TASK}_bold/ "Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm" /data/hx-hx1/kbaacke/datasets/parcellation_metadata "Nonsmoothed with ICA-AROMA"
    done
  done
done


# HCP
#5384cc6b
INDIR=/data/hx-hx1/kbaacke/datasets/HCP/HCP_1200
INDIRICA=/data/hx-hx1/kbaacke/datasets/HCP/HCP_1200_ICA-AROMA
SUBLIST=$(ls $INDIRICA)
TIME=tfMRI_MOTOR
for SUBJECT in $SUBLIST; do
  for RUN in RL LR; do
    qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N _${SUBJECT}_${RUN} /data/hx-hx1/kbaacke/Code/MSC_Parcellation_v2.sh ${INDIR}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/${TIME}_${RUN}.nii.gz ${INDIR}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/ "Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm" /data/hx-hx1/kbaacke/datasets/parcellation_metadata "No Smoothing, no Confounds"
  done
done


#7e91a520
INDIRICA=/data/hx-hx1/kbaacke/datasets/HCP/HCP_1200_ICA-AROMA
SUBLIST=$(ls $INDIRICA)
TIME=tfMRI_MOTOR
for SUBJECT in $SUBLIST; do
  for RUN in RL LR; do
    qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N _${SUBJECT}_${RUN}_Aroma /data/hx-hx1/kbaacke/Code/MSC_Parcellation_v2.sh ${INDIRICA}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/${TIME}_${RUN}-AROMA-denoised-nonsmoothed.nii.gz ${INDIRICA}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/ "Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm" /data/hx-hx1/kbaacke/datasets/parcellation_metadata "Nonsmoothed with ICA-AROMA"
  done
done


# HCP Other Tasks
#5384cc6b

INDIR=/data/hx-hx1/kbaacke/datasets/HCP/HCP_1200
INDIRICA=/data/hx-hx1/kbaacke/datasets/HCP/HCP_1200_ICA-AROMA
SUBLIST=$(ls $INDIRICA)
for SUBJECT in $SUBLIST; do
  for TIME in tfMRI_WM tfMRI_EMOTION tfMRI_GAMBLING tfMRI_LANGUAGE tfMRI_RELATIONAL tfMRI_SOCIAL; do
    for RUN in RL LR; do
      qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N _${SUBJECT}_${RUN}_${TIME} /data/hx-hx1/kbaacke/Code/MSC_Parcellation_v2.sh ${INDIR}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/${TIME}_${RUN}.nii.gz ${INDIR}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/ "Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm" /data/hx-hx1/kbaacke/datasets/parcellation_metadata/ "No Smoothing, no Confounds"
    done
  done
done

#7e91a520

INDIRICA=/data/hx-hx1/kbaacke/datasets/HCP/HCP_1200_ICA-AROMA
SUBLIST=$(ls $INDIRICA)
for SUBJECT in $SUBLIST; do
  for TIME in tfMRI_WM tfMRI_EMOTION tfMRI_GAMBLING tfMRI_LANGUAGE tfMRI_RELATIONAL tfMRI_SOCIAL; do
    for RUN in RL LR; do
      qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N _${SUBJECT}_${RUN}_${TIME}_Aroma /data/hx-hx1/kbaacke/Code/MSC_Parcellation_v2.sh ${INDIRICA}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/${TIME}_${RUN}-AROMA-denoised-nonsmoothed.nii.gz ${INDIRICA}/${SUBJECT}/MNINonLinear/Results/${TIME}_${RUN}/ "Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm" /data/hx-hx1/kbaacke/datasets/parcellation_metadata/ "Nonsmoothed with ICA-AROMA"
    done
  done
done


