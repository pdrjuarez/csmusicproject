#!/bin/bash

sudo su
yum update -y
pip install --upgrade --no-cache-dir awscli
pip install --upgrade --no-cache-dir boto
pip install --upgrade --no-cache-dir boto3
yum install -y gcc
yum install -y gcc-c++
yum install -y gcc-gfortran
yum groupinstall "Development Tools"
yum install -y python-devel libpng-devel freetype-devel
yum install -y libxml12 libxml12-devel libxslt libxslt-devel
yum install -y python-setuptools
pip install --upgrade --no-cache-dir boto3
pip install --upgrade --no-cache-dir wheel
pip install --upgrade --no-cache-dir cython
pip install --upgrade --no-cache-dir pycparser
pip install --upgrade --no-cache-dir toolz
pip install --upgrade --no-cache-dir pytz
wget ftp://ftp.hdfgroup.org/HDF5/current/src/hdf5-1.8.17.tar.gz
tar -xvzf hdf5-1.8.17.tar.gz
rm -f hdf5-1.8.17.tar.gz
cd hdf5-1.8.17
./configure --prefix=/usr/local/hdf5
make
make check
make install
make check-install
export HDF5_DIR=/usr/local/hdf5
export LD_LIBRARY_PATH=/usr/local/hdf5/lib
cd /home/ec2-user
/bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=3072
/sbin/mkswap /var/swap.1
/sbin/swapon /var/swap.1
pip install --upgrade --no-cache-dir boto3
pip install --upgrade --no-cache-dir requests
pip install --upgrade --no-cache-dir pyYAML
pip install --upgrade --no-cache-dir numpy
pip install --upgrade --no-cache-dir rdflib
pip install --upgrade --no-cache-dir h5py
pip install --upgrade --no-cache-dir tables
pip install --upgrade --no-cache-dir numexpr
pip install --upgrade --no-cache-dir cytoolz
pip install --upgrade --no-cache-dir matplotlib
pip install --upgrade --no-cache-dir ipython
pip install --upgrade --no-cache-dir pandas
pip install --upgrade --no-cache-dir sympy
pip install --upgrade --no-cache-dir nose
yum install -y numpy-f2py
yum install -y atlas atlas-devel
yum install -y blas blas-devel
yum install -y lapack lapack-devel
pip install --upgrade --no-cache-dir scipy
pip install --upgrade --no-cache-dir wikipedia
swapoff /var/swap.1
rm /var/swap.1

cd
git clone https://github.com/tbertinmahieux/MSongsDB


export HDF5_DIR=/usr/local/hdf5
export LD_LIBRARY_PATH=/usr/local/hdf5/lib
cd /home/ec2-user




