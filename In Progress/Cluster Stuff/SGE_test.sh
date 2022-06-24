#!/bin/bash
IND=$1
USR=$2
output_directory=/data/r2-home/kbaacke/temp/cluster_testing/
echo $IND
touch ${output_directory}${IND}.txt
command | tee ${output_directory}${IND}.txt
date | tee -a ${output_directory}${IND}.txt
hostnamectl | tee -a ${output_directory}${IND}.txt



