# Clinic2Cloud Docker container.
# November 2017, Copyright Clinic2Cloud team, licence: BSD 2-Clause

FROM kaczmarj/minc:1.9.15_centos7

# Change to the root user for updating the image
USER 0

# We need perl to run all the scripts
RUN yum install -y perl

# This file is missing for some reason.  Copied from minc-widgets/b7dbf3c
COPY mincanon /opt/minc/bin/mincanon

# Change back to a less privilaged user for execution
USER neuro

# Copy the script for our processing pipeline
COPY run.sh /home/neuro/run.sh

# Create a default command for processing the files
CMD ["/bin/bash", "/home/neuro/run.sh"]

