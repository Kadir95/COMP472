FROM ubuntu:16.04
RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends tcpd xinetd python nano lsof netstat && \
    apt-get clean
ADD App/ /App/
ADD idle.py /App/idle/idle.py
ADD xinetd.conifg/unicornfts /etc/xinetd.d/ 
CMD echo "unicornfts    8181/tcp" >> /etc/services
CMD xinetd -stayalive
CMD /etc/init.d/xinetd restart
CMD python /App/idle/idle.py