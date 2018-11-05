FROM ubuntu:16.04
RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends tcpd xinetd python nano lsof && \
    apt-get clean
ADD App/ /App/
# Add unicorn fts service config
ADD xinetd.conifg/unicornfts /etc/xinetd.d/
CMD xinetd -dontfork
EXPOSE 8181
ENTRYPOINT echo "unicornfts    8181/tcp" >> /etc/services && \
    /etc/init.d/xinetd restart && \
    python /App/idle.py