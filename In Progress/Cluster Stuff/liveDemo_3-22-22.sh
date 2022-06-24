# Login with htop windows in background 

source /usr/local/sge/default/common/settings.sh

# Show cross-mounted drives

df -h

cd /data

ls

cd hx-hx1/kbaacke

cd Code

ls

cat MSC_Parcellation.sh

python3 /data/hx-hx1/kbaacke/Code/Parcellation/nifty2numpy_parcellation.py -h

cd /data/hx-hx1/kbaacke/Code

dos2unix MSC_Parcellation_v2.sh

chmod u+x MSC_Parcellation_v2.sh

dos2unix MSC_Parcellation_v3.sh

chmod u+x MSC_Parcellation_v3.sh

ls ../datasets/MSC/ds000224-Output/sub-MSC02/MNINonLinear/Results/

SUBJECT='sub-MSC02'

echo $SUBJECT

TIME=func01

TASK=motor_run-01

qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N ${SUBJECT}_${TIME}_${TASK} /data/hx-hx1/kbaacke/Code/MSC_Parcellation.sh "$SUBJECT" "$TIME" "$TASK" "Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm"

qstat
# for TIME in func01 func02 func03 func04 func05 func06 func07 func08 func09 func10; do # Iterate through sessions
#   for TASK in motor_run-01 motor_run-02 glasslexical_run-01 glasslexical_run-02 memoryfaces memoryscenes memorywords; do # Iterate through tasks
#     qsub \ # '\' tells the console to ignore the newline character and continue the qsub command on the next line
#       -e /data/hx-hx1/kbaacke/SGE_Output/ \ # the '-e' flag indicates where the error file should be stored
#       -N ${SUBJECT}_${TIME}_${TASK} \ # the '-N' flag indicates a name for the 
#       /data/hx-hx1/kbaacke/Code/MSC_Parcellation.sh "$SUBJECT" "$TIME" "$TASK" "Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm" # Call the job file with four positional arguments
#   done
# done

SUBJECT='sub-MSC02'
for TIME in func01 func02 func03 func04 func05 func06 func07 func08 func09 func10; do # Iterate through sessions
  for TASK in motor_run-01 motor_run-02 glasslexical_run-01 glasslexical_run-02 memoryfaces memoryscenes memorywords; do # Iterate through tasks
    qsub -e /data/hx-hx1/kbaacke/SGE_Output/ -N ${SUBJECT}_${TIME}_${TASK} /data/hx-hx1/kbaacke/Code/MSC_Parcellation.sh "$SUBJECT" "$TIME" "$TASK" "Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm" # Call the job file with four positional arguments
  done
done
qstat

cd /data/hx-hx1/kbaacke/datasets/MSC/ds000224-Parcellation/sub-MSC02/MNINonLinear/Results/
ls

cd /data/hx-hx1/kbaacke/SGE_Output/
ls -lh
