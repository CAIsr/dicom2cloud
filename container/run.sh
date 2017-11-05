#!/bin/bash
#
# run.sh - This is the main pipeline script for the clinic2cloud.
#    This script calls the other scripts that actually do the heavy lifting.
#
# Copyright 2017 Clinc2Clound Team
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

echo "Doing some heavy lifting..."
# TODO: Actually do heavy lifting

cd /home/neuro
mkdir mnc
dcm2mnc -clobber /home/neuro/* ./mnc
mv ./mnc/*.mnc ./temp.mnc
deface_minipipe.pl temp.mnc --beastlib /opt/minc/share/beast-library-1.1/ --model-dir /opt/minc/share/icbm152_model_09c/ --model mni_icbm152_t1_tal_nlin_sym_09c output.mnc
mincanon output.mnc

# Return 0 when everything went ok
exit 0

