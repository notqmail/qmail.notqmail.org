#! /bin/rpm
%define destdir %buildroot
%define daemons fingerd wuftpd proftpd rlogind rshd rsync telnetd
Buildarch: noarch
Buildroot: %_tmppath/%name-%version-root
Copyright: Free
ExclusiveOS: Linux
Group: Utilities/System
Name: other-run
Packager: mw@csi.hu
Prereq: dt-run 
Provides: other-run
Release: 112memphis
Requires:  dt-run 
Source0: %name-%version.tar.gz
Summary: run files for some common daemons
Version: 11.07

%description
This package

--provides init and run scripts so that the services
    %daemons
can run under svscan controlled supervises.  

%prep
%setup

%install
rm -rf %destdir


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

echo %destdir > config/DESTDIR
make iother

%preun
# remove sysV style init if the package is removed for good
if [ $1 = 0 ]; then
    for i in %daemons; do
	if [ -f /command/$i.init ]; then
	    /command/remove-service.sh $i
	fi
    done
    
fi

%clean
rm -rf %destdir

%files
%defattr(-,root,root)
%config /var/service/*/run
%config /var/service/*/log/run
%dir /var/service/*
%dir /var/service/*/log
%dir %attr(-,dtlog,dtlog) /var/service/*/log/main
