FROM ubuntu:16.04
RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends tcpd xinetd python && \
    apt-get clean
ADD idle.py /App/idle.py
CMD python /App/idle.py