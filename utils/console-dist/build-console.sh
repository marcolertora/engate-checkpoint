#!/bin/sh

SFSIMAGE=$1
SFSROOT=/tmp/fsfimage

COMP="-comp xz -Xbcj x86"
OPTIONS="$COMP -no-progress -noappend -all-root"

if [ $# -ne 1 ]; then
    echo "usage: $0 output.sfs"
    exit 1
fi

echo "Creating image in: $SFSROOT"
rm -rf $SFSROOT

install -D -m 644 tools/console/inittab $SFSROOT/etc/inittab
install -D -m 755 tools/console/console.xinitrc $SFSROOT/opt/checkpoint/console.xinitrc
install -D -m 644 tools/console/preferences $SFSROOT/root/.icewm/preferences

install -D -m 644 console.ini.sample $SFSROOT/opt/checkpoint/console.ini
install -D -m 644 console_it.qm $SFSROOT/opt/checkpoint/console_it.qm
install -D -m 755 console.py $SFSROOT/opt/checkpoint/console.py
install -D -m 644 ui/__init__.py $SFSROOT/opt/checkpoint/ui/__init__.py
install -D -m 644 ui/console_rc.py $SFSROOT/opt/checkpoint/ui/console_rc.py
install -D -m 644 ui/console.py $SFSROOT/opt/checkpoint/ui/console.py

install -D -m 644 tools/console/ssh/ssh_host_dsa_key.pub $SFSROOT/etc/ssh/ssh_host_dsa_key.pub
install -D -m 600 tools/console/ssh/ssh_host_dsa_key $SFSROOT/etc/ssh/ssh_host_dsa_key
install -D -m 644 tools/console/ssh/ssh_host_rsa_key.pub $SFSROOT/etc/ssh/ssh_host_rsa_key.pub
install -D -m 600 tools/console/ssh/ssh_host_rsa_key $SFSROOT/etc/ssh/ssh_host_rsa_key
install -D -m 644 tools/console/ssh/authorized_keys $SFSROOT/root/.ssh/authorized_keys
install -D -m 755 tools/console/runvnc $SFSROOT/usr/local/bin/runvnc


echo "Creating $SFSIMAGE"
mksquashfs $SFSROOT $SFSIMAGE $OPTIONS
unsquashfs -l $SFSIMAGE
rm -rf $SFSROOT
