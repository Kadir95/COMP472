echo "unicornfts    ${PORT}/tcp" >> /etc/services
echo "unicornfts    ${PORT}/udp" >> /etc/services
ln -s /usr/bin/python3 /bin/python
ln -s /usr/bin/python3 /usr/bin/python
/etc/init.d/xinetd restart
python /App/idle.py