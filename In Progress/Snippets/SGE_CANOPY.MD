# Using SGE on the CANOPY CLuster

## Helpful Links

## About the cluster environment

## Setting up your environment

source /usr/local/sge/default/common/settings.sh

## Setting up a job file

start file with 

#!/bin/bash

## * Send files to cluster (if not there already)

## Fix any non-unix characters in the script (if on windows)

dos2unix SGE_test.sh

##  Make the file executable

chmod u+x

## Submit you job

### Add positional arguments and optional flags

