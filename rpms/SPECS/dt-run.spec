#! /bin/rpm
%define destdir %buildroot
# you should not change admin_dir
%global admin_dir /package/admin
%global command_dir %admin_dir/%name-%version/command
%global ucspi_tcp_bin /usr/local/bin
%global varserviceroot /var/service
Buildarch: noarch
Buildroot: %_tmppath/%name-%version-root
Copyright: GPL
Group: Utilities/System
Name: dt-run
Conflicts: tcpserver-initscripts
Packager: mw@csi.hu
Prereq: shadow-utils
Release: 112memphis
Requires: functions >= 3 daemontools >= 0.76 ucspi-tcp >= 0.88 runlevelconf >= 0.07 
Source: ftp://moni.csi.hu/pub/run/%name-%version.tar.gz
Summary: Tools to help run daemons under svscan
Version: 11.07

%description 

Tools to help run daemons under svscan.  The package includes
dt-runlevel.init which emulates runlevel changes under svscan.  In
fact, the package sets up a sysV like environment which is independent
from the one provided by the traditional rc scripts.  Services are
started/stopped not by sequence numbers, but according to a "real"
start/stop dependence tree of services.

%prep

%setup -q

%install
rm -rf %destdir

echo %destdir		> config/DESTDIR
echo %ucspi_tcp_bin	> config/UCSPI_TCP_BIN
make ibase


echo 1,000,000 > %destdir/%varserviceroot/multilog/filesize
echo 10 > %destdir/%varserviceroot/multilog/fileno

mkdir -p %destdir/etc/profile.d
echo "appath PATH /command"  \
    > %destdir/etc/profile.d/%name.sh
echo 'setenv PATH ${PATH}:/command' \
    > %destdir/etc/profile.d/%name.csh
chmod +x %destdir/etc/profile.d/*

%post
export PATH=/command:$PATH:/usr/sbin:/sbin

function user_add() {
    for i in $@; do
        if id -u $i > /dev/null 2>&1; then
            true
        else
            useradd -r $i
        fi
    done
}

user_add dtlog

## update nis database
if /sbin/pidof ypserv >/dev/null 2>&1; then
    (cd /var/yp; make)
fi

if [ $1 = 1 ]; then
    echo "See INSTALL_rpm for what to put in /etc/inittab"
fi

if [ $1 = 0 ]; then
    echo "Please remove the dt-runlevel.init and dt-svscan.init entries"
    echo "from /etc/inittab."
fi

# compatibility with older versions
for i in $(/bin/ls /service); do
    if [ -f /usr/local/sbin/$i.init ]; then
	rm /usr/local/sbin/$i.init
	(
	cd /command
	ln -s ..%varserviceroot/dt-run/dt-service.init $i.init
	)
    fi
done

%preun
if [ $1 = 0 ]; then
    export PATH=/command:/usr/sbin:/sbin:$PATH

    for i in $(awk -F: '!/^#/ { print $1 }' %varserviceroot/dt-run/dt-list); do
	if [ -f /command/$i.init ]; then
	    /command/remove-service.sh $i
	fi
    done    
    
    for i in $(/bin/ls /service); do
	$i.init stop
    done	

    %varserviceroot/dt-runlevel.init stop
    %varserviceroot/dt-svscan.init stop

fi

%clean
rm -rf %destdir

%files
%defattr(-,root,root)
%config %varserviceroot/svscan/run
%config /etc/profile.d/*
%config(noreplace) %varserviceroot/multilog/*
%dir /service
%dir %varserviceroot/dt-run
%dir %varserviceroot/multilog
%dir %varserviceroot/svscan
%doc  ChangeLog DISTRIBUTE INSTALL* MANUAL ME README
%doc THANKS TODO
%varserviceroot/dt-run/*
/command/*
%admin_dir/*
