FROM ubuntu:16.04
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get -y install --no-install-recommends tcpd xinetd && \
    apt-get clean && \
RUN useradd -u 8888 -m pwn
COPY App /App