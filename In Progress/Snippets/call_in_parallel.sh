# @Authors: 
#   Kyle Baacke; kbaacke2@illinois.edu; https://github.com/kabaacke-psy
# @DateCreated: 02/07/2022
# @DateUpdated: 02/07/2022
# Description:
#   You may find yourself wanting to run a process in parallel (i.e. multiple processes running simultaneously) via the native shell (or zshell) native to your computational environment. This snippet provides an example of how to do so without the use of any non-generic packages or functions. This can enable you to make full use of the compute resources available without the additional overhead of installing other tools. The process can be divided into 3 main steps: 1) establishing the resource pool available to use, 2) defining a function to run in parallel if there are multipe components of a process that need to be run for each iteration, and 3) calling the function in parallel
# Notes and Qualifiers:
#   This code has been written and tested in BASH on native linux installations (OpenSUSE) and on Ubuntu for Windows (20.04.2 using WSL 2). 

# 1) Identifying your resource pool

# Before you run anyting in parallel, you should first establish how many CPUs ara avialble for use.
# The following command will give you details about the CPUs on the current machine
lscpu

# Always make sure you will not cause problems for other users by checking to see if anyone else is currenlty using the same machine.
# You can do this and learn more about the current memory and thread availability using either of the following commands. 

top
# or
htop

# This will give you an active diplay of the processes currently running on the machine, including CPU and memory usage and runtime.
# Use q to exit the top display.

# 2) Defining your function

# Now that you know what you have to work with, you need to set up a function to run in parallel
# The following function takes three arguements (subject, time, and run, in that order).
# It then uses these arguements to call a python function (nifty2numpy_parcellation.py).
# First, lets start with some global constant variables

OUTDIR2=/mnt/usb1/HCP_1200_ICA-AROMA
TIME=tfMRI_MOTOR
# We need a list of subjects to iterate through. The following command creates a list out of each folder in the directory we assigned to OUTDIR2
SUBLIST=$(ls $OUTDIR2)
# Now assign the number of threads to use as a variable
N=10

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

# 3) Calling in parallel

# We can iterate through the subjects in $SUBLIST and the runs within each subject using nested for loops
for SUBJECT in $SUBLIST; do
  for RUN in RL LR; do
    # First we call the function for a SUBJECT, RUN to start one process.
    parcellate "$SUBJECT" "$TIME" "$RUN" &
    # Then we check to see if the number of processes we have running matches the $N value that we set
    if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
      # If we are at our allotted ammount, then we will wait until one of our jobs is complete before starting another
      wait -n
    fi
   done
done

# Note that you can keep 'htop' running in a second window to track your use of resources in real time. This is a good way to keep track of how far along you are, as well as what bottlenecks you have when running N threads at a time. For instance, you may find that you can only run 4 at a time, even through you have 12 threads because of a memory constraint.