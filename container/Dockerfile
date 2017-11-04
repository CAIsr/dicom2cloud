FROM kaczmarj/minc:1.9.15_centos7

USER 0

# We need perl to run all the scripts
RUN yum install -y perl

# This file is missing for some reason.  Copied from minc-widgets/b7dbf3c
COPY mincanon /opt/minc/bin/mincanon

USER neuro

