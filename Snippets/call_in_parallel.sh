# Running terminal commans in parallel is a great way to take advantage of the compute resources available to you.
# Before you run anyting in parallel, you should first establish how many CPUs ara avialble for use.
# The following command will give you details about the CPUs on the current machine
lscpu


# Always make sure you will not cause problems for other users by checking to see if anyone else is currenlty using the same machine.
# You can do this and leanr more about the currenly memory availability using the following command.

top

# This will give you an active diplay of the processes currently running on the machine, including their CPU and memory usage, as well as how long they have been running
# Use q to exit the top display.

q

# Now that you know what you have to work with, you need to set up a function to run in paralell
# The following function takes three arguements (subject, time, and run, in that order).
# It then uses these arguements to call a python function (nifty2numpy_parcellation.py) with three addiitonal arguements
OUTDIR2=/mnt/usb1/HCP_1200_ICA-AROMA
TIME=tfMRI_MOTOR
parcellate(){
  # Use $ fllowed by a number to take an arguement passed to the function and assign it to a variable
  local subject=$1
  local time=$2
  local run=$3
  # This prints the target path to the terminal so we know which image we are targetting. In the event that re run into an error, we can check this against the true path as a way to check if the path is correct
  echo ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA-denoised-nonsmoothed.nii.gz
  python3 nifty2numpy_parcellation.py \
    -input ${OUTDIR2}/${subject}/MNINonLinear/Results/${time}_${run}/${time}_${run}-AROMA-denoised-nonsmoothed.nii.gz \
    -atlas Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm \
    --metadata /mnt/usb1/Code/MSC_HCP/
}

# Now we need a list of subjects to iterate through. The following command creates a list out of each folder in the directory we assigned to OUTDIR2
SUBLIST=$(ls $OUTDIR2)
# Now lets assign the number of threads to use as a variable
N=10
# Now we can iterate through the subjects in $SUBLIST and the runs within eahc subject using nested for loops
for SUBJECT in $SUBLIST; do
  for RUN in RL LR; do
    # First we call our function for a SUBJECT, RUN 
    parcellate "$SUBJECT" "$TIME" "$RUN" &
    # Then we check to see if the number of processes we have running matches the $N value that we set
    if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
      # If we are at our allotted ammount, then we will wait until one of our jobs is complete before starting another
      wait -n
    fi
   done
done

