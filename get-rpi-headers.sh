#! /bin/sh

KTREE="3.10.y"
KVERSION=`uname -r`

cd /usr/src
wget  https://github.com/raspberrypi/linux/tarball/rpi-$KTREE
tar xzf rpi-$KTREE

mv raspberrypi-linux-* linux-headers-$KVERSION
cd linux-headers-$KVERSION
zcat /proc/config.gz > .config
make oldconfig
make modules_prepare