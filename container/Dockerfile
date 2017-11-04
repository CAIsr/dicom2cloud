FROM kaczmarj/minc:1.9.15_centos7

USER 0

# We need perl to run all the scripts
RUN yum install -y perl

# This file is missing for some reason.  Copied from minc-widgets/b7dbf3c
COPY mincanon /opt/minc/bin/mincanon

# Copying in beast libraries used for defacing
ADD http://packages.bic.mni.mcgill.ca/tgz/beast-library-1.1.tar.gz /opt/minc/share
COPY beast_atlas_icbm152_2009 /opt/minc/share

USER neuro

