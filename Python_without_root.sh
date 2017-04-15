#!/bin/bash
mkdir ~/src
mkdir ~/.localpython
cd ~/src
#wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tar.xz
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tar.xz
#tar xvfJ Python-3.5.0.tar.xz
tar xvfJ Python-2.7.10.tar.xz
#cd Python-3.5.0
cd Python-2.7.10
​
make clean
./configure --prefix=/home/UA/jschroder/.localpython
make
make install
​
#2) Install virtualenv
cd ~/src
wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.2.tar.gz --no-check-certificate
tar -zxvf virtualenv-13.1.2.tar.gz
cd virtualenv-13.1.2/
~/.localpython/bin/python setup.py install
​
#3) Create a virtualenv using your local python
cd ~
~/.localpython/bin/virtualenv venv2 --python=/home/UA/jschroder/.localpython/bin/python2.7
​
#4) Activate the environment
​
source venv2/bin/activate
