#! /bin/rpm
%define destdir %buildroot
# you should not change command_dir
%global command_dir /package/admin/%name-%version/command
%global varserviceroot /var/service 
Buildarch: noarch
Buildroot: %_tmppath/%name-%version-root
Copyright: GPL
Group: Utilities/System
Name: runlevelconf
Packager: mw@csi.hu
Release: 112memphis
Requires: functions >= 3 daemontools >= 0.76 tree
Source: ftp://moni.msci.memphis.edu/pub/run/%name-%version.tar.gz
Summary: Maintains a dependency tree for startup order of services
Version: 0.08

%description
Tools to maintain a dependency tree for start/stop order of services.
The main tools are:

-- rlc-add builds the start/stop dependency tree for a runlevel

-- rlc-doit, based on the dependency tree, creates a start/stop
   sequence.

-- rlc-go, if given a list of currently running services, creates an
   appropriately ordered list of services to start and stop.

%prep

%setup

%install
export PATH=/command:$PATH
rm -rf %destdir

echo %destdir 		> config/DESTDIR
make ibase

mkdir -p %destdir/etc/profile.d
echo "appath PATH /command"  > %destdir/etc/profile.d/%name.sh
echo 'setenv PATH ${PATH}:/command' > %destdir/etc/profile.d/%name.csh
chmod +x %destdir/etc/profile.d/*
%clean
rm -rf %destdir

%files
%defattr(-,root,root)
%config /etc/profile.d/*
%dir /var/service
%dir /var/service/runlevelconf
%doc ChangeLog DISTRIBUTE INSTALL* MANUAL ME README
%doc THANKS TODO
%varserviceroot/runlevelconf/*
/command/*
%command_dir