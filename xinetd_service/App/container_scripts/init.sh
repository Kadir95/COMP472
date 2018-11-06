echo "unicornfts    ${PORT}/tcp" >> /etc/services
echo "unicornfts    ${PORT}/udp" >> /etc/services
/etc/init.d/xinetd restart
ln -s /usr/bin/python3 /bin/python
ln -s /usr/bin/python3 /usr/bin/python
python /App/idle.py