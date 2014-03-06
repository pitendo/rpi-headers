#! /bin/sh

KTREE="3.10.y"
KVERSION=`uname -r`

cd /usr/src

echo "### Downloading kernel source ###"
wget  https://github.com/raspberrypi/linux/tarball/rpi-$KTREE

echo "### Uncompressing kernel source ###"
tar xzf rpi-$KTREE



mv raspberrypi-linux-* linux-headers-$KVERSION
rm -fr rpi-$KTREE

echo "### Preparing linux headers ###"
cd linux-headers-$KVERSION
zcat /proc/config.gz > .config
make oldconfig
make modules_prepare

echo "### Downloading Module.symvers ###"
wget https://github.com/raspberrypi/firmware/raw/master/extra/Module.symvers

echo "### Linking to kernel source ###"
KERNEL_SRC=`pwd`
cd /lib/modules/$KVERSION
ln -s ${KERNEL_SRC} build
