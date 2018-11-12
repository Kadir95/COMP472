# Xinetd Data Mover (unicornfts)
## Start to work
Host machine must have docker. Server side of the data mover (unicornfts) is run on docker container and it exposes <code>8181</code> port to host.
### Setup
Run those command on your shell. <code>./build.sh</code> will ask root password

    $git clone https://github.com/Kadir95/COMP472.git
    $cd COMP472/xinetd_service/ </br>
    $./build.sh

<code>./build.sh</code> will take time. It'll create docker container and run it.
### Running the client script
Client scirpt is in <code>/path/to/repo/COMP472/xinetd_service/client/unicornfts.py</code>.

	$./client/unicornfts.py
	Usage: ./client/unicornfts.py <operation>
	Operations : put, get, del, list

#### list
list argument print your directory with <code>ls -l</code>.
If you run the list functionality first time, the server will create a directory which is named with your username.

	$ ./client/unicornfts.py list
	New directory is created (<username>)
	$ ./client/unicornfts.py list
	There is no stored file

#### get
get functionality downloads file from server to client. It take 1 argument which is file name.

	$ ./client/unicornfts.py list
	total 6504
	-rw-r--r-- 1 root root 6659919 Nov 12 04:51 test.data
	$ ./client/unicornfts.py get test.data
	File is transferred successfully

#### del
del functionality delete remote data if the client machine has a copy of the data. It takes 1 argument which is a file name

	$ ./client/unicornfts.py list
	total 6504
	-rw-r--r-- 1 root root 6659919 Nov 12 04:51 test.data
	$ ./client/unicornfts.py del test.data
	File test.data is deleted
	$ ./client/unicornfts.py list
	There is no stored file

#### put
put functionality upload a data. It takes 1 argument which is file name.
put checks the local file and the uploaded file according to MD5. If they match, uploading progress is ended successfully. Otherwise the progress will delete

	$ ./client/unicornfts.py list
	There is no stored file
	$ ./client/unicornfts.py put test.data
	File is transferred successfully
	$ ./client/unicornfts.py list
	total 6504
	-rw-r--r-- 1 root root 6659919 Nov 12 05:04 test.data

