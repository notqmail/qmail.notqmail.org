# put the fqdn of the qmqpserver here
%define qmqpserver ''
%define destdir %buildroot
# homedir of mini-qmail
%global mini_qmail_home /var/mini-qmail
Buildroot: %{_tmppath}/%{name}-%{version}
Conflicts: sendmail exim smail qmail postfix
License: Check with djb@koobera.math.uic.edu
ExclusiveOS: Linux
Group: Utilities/System
Name: mini-qmail
Packager: mw@csi.hu
Patch0: qmail-%{version}.errno.patch
Patch1: %name-%{version}.patch
Provides: MTA 
Release: 112memphis
Requires: functions > 1 
Source0: ftp://cr.yp.to/software/qmail-%{version}.tar.gz
Source1: %name.README_rpm
Summary: Qmail Mail Transfer Agent
URL: http://www.qmail.org/
Version: 1.03

%description 

Qmail is a small, fast, secure replacement for the SENDMAIL package,
which is the program that actually receives, routes, and delivers
electronic mail.  This mini-qmail package is a qmail nullclient the
only role of which is to forward mail to a smarthost.

%prep
if [ "`id | cut -d'(' -f1`" != 'uid=0' ]; then
	echo Need to build this package as root
	exit 2
fi

%setup -q -n qmail-%{version}

%patch -p1
%patch1 -p1

%build
echo "gcc ${RPM_OPT_FLAGS}" | sed s}"-O2"}"-O"} > conf-cc
echo %mini_qmail_home > conf-qmail

# Fix hier.c so that nothing gets installed
# in man/cat?.
grep -v "man/cat*" hier.c > hier.c.tmp 
mv hier.c.tmp hier.c

make mini-it
make man

%install
rm -rf %destdir

# create ~qmail
mkdir -p %destdir%mini_qmail_home/bin
chmod 755 %destdir%mini_qmail_home

# these are needed after installation 
cp config-idhost config-idhost-fast config-qmqpserver dnsfq dnsip \
dnsptr hostname instcheck ipmeprint %destdir%mini_qmail_home/bin

# Needed to work around a make bug 
sleep 2

# Now recompile install and instcheck to install in
# %destdir%mini_qmail_home

echo %destdir%mini_qmail_home > conf-qmail

make install
make instcheck

# install
./install 

# check 
./instcheck

# link for qmail-queue
ln -sf  ../../..%mini_qmail_home/bin/qmail-qmqpc %destdir%mini_qmail_home/bin/qmail-queue

# link in /usr/lib is needed for Emacs
for i in sbin lib; do
    mkdir -p %destdir/usr/$i
    ln -sf ../..%mini_qmail_home/bin/sendmail %destdir/usr/$i/sendmail
done


# The next files will be "filled" after installation
# They need to be created so that rpm knows about them
(cd %destdir%mini_qmail_home/control;
for i in defaultdomain  me plusdomain idhost qmqpservers; do
    touch $i
    chmod 644 $i
done
)

cp %SOURCE1 README_rpm

%post
# set up files in %mini_qmail_home/control only if we are not upgrading
if [ $1 = "1" ]; then
   ( cd %mini_qmail_home/bin
     ./config-idhost
     if [ "`expr '%{qmqpserver}' = ''`" = 1 ]; then
	echo You set the qmqpserver(s) by running the command
	echo 
	echo '( cd %mini_qmail_home/bin; ./config-qmqpserver FQDN_of_qmqpserver )'
	echo
    	echo See README_rpm in the doc directory of this package for details. 
     else
	echo Since the name of the qmqpserver has been given to this rpm,
	echo I try to run config-qmqpserver for you now.  If you see
	echo any errors, you need to run the command yourself.  See
	echo README_rpm in the doc directory of this package for details.
	./config-qmqpserver %qmqpserver
	
     fi
   )
fi

# check the installation
(cd %mini_qmail_home/bin; ./instcheck)


# take care of pine---but only if we are not upgrading
if [ $1 = "1" ]; then
   if [ -f /etc/pine.conf ]; then
       echo "Modifying /etc/pine.conf"
       echo "The old  pine.conf file is saved as "
       echo "/etc/pine.conf.BEFORE_QMAIL."
       cp -a /etc/pine.conf /etc/pine.conf.BEFORE_QMAIL
       sed -e '/^inbox-path/d' \
	   -e '/^sendmail-path/d' \
	   /etc/pine.conf   > /tmp/pine.conf.noq
       echo 'inbox-path=$MAIL' > /tmp/pine.conf.q
       echo 'sendmail-path=/usr/sbin/sendmail  -oem -oi -t' >> /tmp/pine.conf.q
       cat /tmp/pine.conf.noq  /tmp/pine.conf.q >  /tmp/pine.conf
       mv /tmp/pine.conf /etc/pine.conf
       rm -f  /tmp/pine.conf*  
       echo You also want to set the user-domain to the qmqpserver
       echo in control/defaulthost
    fi
fi

%postun

# If mini-qmail is removed:
if [ $1 = 0 ]; then
    if [ -f /etc/pine.conf ]; then
	echo "Removing inbox-path, sendmail-path from pine.conf..."
	echo "The old  pine.conf file is saved as "
	echo "/etc/pine.conf.QMAIL."
	cp -a /etc/pine.conf /etc/pine.conf.QMAIL    
	sed -e '/^inbox-path/d' \
	    -e '/^sendmail-path/d' \
	    /etc/pine.conf   > /tmp/pine.conf.noq
	mv  /tmp/pine.conf.noq /etc/pine.conf
	rm -f  /tmp/pine.conf*	
    fi
fi 


%clean
rm -rf %destdir    

%changelog

* Wed Nov 19 2003 Mate Wierdl <mw@csi.hu> 1.03-5
- Updated and added errno patch

%files
%defattr(-,root,root)
%dir %mini_qmail_home
%dir %mini_qmail_home/control
%config %mini_qmail_home/control/*
%doc BLURB* CHANGES FAQ INSTALL* INTERNALS PIC*
%doc README README_rpm REMOVE.* SECURITY SENDMAIL SYSDEPS TARGETS 
%doc TEST.* THANKS THOUGHTS TODO UPGRADE VERSION
%mini_qmail_home/bin
%mini_qmail_home/doc
%mini_qmail_home/man
/usr/lib/sendmail
/usr/sbin/sendmail


