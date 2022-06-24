#!/bin/bash
input=$1
output=$2
atlas=$3
metadata=$4
notes=$5

python3 /data/hx-hx1/kbaacke/Code/Parcellation/nifty2numpy_parcellation.py \
  -input $input \
  --output $output \
  -atlas $atlas \
  --metadata $metadata \
  $notes





