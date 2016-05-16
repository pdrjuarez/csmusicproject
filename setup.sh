#!/bin/bash

wget ftp://ftp.hdfgroup.org/HDF5/current/src/hdf5-1.8.17.tar.gz
tar -xvzf hdf5-1.8.16.tar.gz
rm hdf5-1.8.16.tar.gz
cd hdf5-1.8.16
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
pip install --upgrade --no-cache-dir numpy
pip install --upgrade --no-cache-dir h5py
pip install --upgrade --no-cache-dir matplotlib
pip install --upgrade --no-cache-dir ipython
pip install --upgrade --no-cache-dir tables
yum install -y numpy-f2py
yum install -y atlas atlas-devel
yum install -y blas blas-devel
yum install -y lapack lapack-devel
swapoff /var/swap.1
rm /var/swap.1
cd
git clone https://github.com/tbertinmahieux/MSongsDB