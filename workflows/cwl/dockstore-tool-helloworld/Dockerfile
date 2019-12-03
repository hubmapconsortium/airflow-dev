#############################################################
# Dockerfile to build container for Synapse Python client
#############################################################

# Base Image
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER James Eddy <james.a.eddy@gmail.com>

# set version here to minimize need for edits below
ENV VERSION=1.0.2

# set up packages
USER root

COPY bin/hello_world /usr/local/bin/
RUN chmod a+x /usr/local/bin/hello_world

CMD ["/bin/bash"]
