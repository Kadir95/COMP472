FROM ubuntu:16.04
RUN apt-get update
RUN DEBIAN_FRONTED=noninteractive apt-get install -y --no-install-recommends apt-utils && \
    apt-get -y dist-upgrade && \
    apt-get -y install tcpd xinetd && \
    apt-get clean && \
ADD idle.py /App/idle.py
RUN python /App/idle.py