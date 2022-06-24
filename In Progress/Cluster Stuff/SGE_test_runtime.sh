#!/bin/bash

chmod u+x SGE_test.sh

for ind in ind01 ind02 ind03 ind04 ind05 ind06 ind07 ind08 ind09 ind10 ind11 ind12 ind13 ind14 ind15 ind16 ind17 ind18 ind19 ind20 ind21 ind22 ind23 ind24 ind25 ind26 ind27 ind28 ind29 ind30 ind31 ind32 ind33 ind34 ind35 ind36 ind37 ind38 ind39; do
  qsub SGE_test.sh $ind
done
