FROM ubuntu:16.04
ENV PORT    8181
RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends tcpd xinetd python3 nano lsof && \
    apt-get clean
ADD App/ /App/
# Add unicorn fts service config
ADD xinetd.conifg/unicornfts /etc/xinetd.d/
CMD xinetd -dontfork
EXPOSE ${PORT}
ENTRYPOINT ./App/container_scripts/init.sh