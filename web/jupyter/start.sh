#!/bin/bash

/usr/sbin/sshd

exec su - hawk -c "jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''"
