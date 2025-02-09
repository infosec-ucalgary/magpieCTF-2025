#!/bin/bash
/usr/sbin/sshd
exec su - rhash -c "cd /home/rhash/notebooks && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''"
