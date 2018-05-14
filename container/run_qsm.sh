#!/bin/bash
#
# run.sh - This is the main pipeline script for the dicom2cloud.
#    This script calls the other scripts that actually do the heavy lifting.
#
# Copyright 2017 Dicom2clound Team
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

echo "Starting the qsm pipeline"

cd /home/neuro

echo "Doing QSM processing"
directory=`ls -d */`;

echo "found this directory:"
echo $directory

ls $directory

heudiconv -d '{subject}/*/*' -s $directory -f /home/neuro/heudiconv_bids_qsm.py

#dcm2niix -o ./ -f magnitude /home/neuro/testdata/GR_M_5_QSM_p2_1mmIso_TE20/

#dcm2niix -o ./ -f phase GR_P_6_QSM_p2_1mmIso_TE20/

#bet2 magnitude.nii magnitude_bet2

#tgv_qsm -p phase.nii -m magnitude_bet2_mask.nii.gz -f 2.89 -t 0.02 -s -o qsm

# Create outputfile to tell GUI that we are done inside the container with this session
touch done


ll /home/neuro
ll /home/neuro/$directory

# Return 0 when everything went ok
exit 0

