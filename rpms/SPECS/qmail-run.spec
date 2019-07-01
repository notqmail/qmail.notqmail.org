#! /bin/rpm
%define destdir %buildroot
%define dqmailhome %destdir%qmailhome
%define qdaemons qmail qmail-pop3d qmail-qmqpd qmail-qmtpd qmail-smtpd rblsmtpd
%define qmailhome /var/qmail
Buildarch: noarch
Buildprereq: qmail 
Buildroot: %_tmppath/%name-%version-root
Conflicts: sendmail exim smail
Copyright: Free
ExclusiveOS: Linux
Group: Utilities/System
Name: qmail-run
Packager: mw@csi.hu
Prereq: qmail dt-run 
Provides: qmail-run
Release: 112memphis
Requires:  dt-run 
Source: %name-%version.tar.gz
Summary: run files to run qmail under svscan
Version: 11.07

%description
This package 

--provides init and run scripts to start the qmail daemons at startup
and to manage them by svscan controlled supervises.  

--provides shell init files to set the usual environment variables
associated with mailing (MAIL and MAILDROP).

--sets up the same system aliases as the RH sendmail package.

--sets up links in /usr/sbin and /usr/lib to the sendmail
emulation of qmail.

%prep
%setup

%install
rm -rf %destdir

echo %destdir > config/DESTDIR
make iqmail

# make links to qmail's sendmail in standard places
# link in /usr/lib is needed for Emacs
for i in sbin lib; do
    mkdir -p %destdir/usr/$i
    ln -sf ../..%qmailhome/bin/sendmail %destdir/usr/$i/sendmail
done

# Preserve the default aliases from RedHat's sendmail.
mkdir -p %dqmailhome/alias
(
    cd %dqmailhome/alias
    for i in postmaster mailer-daemon bin daemon games ingres nobody \
    system toor uucp manager dumper operator decode; do
	echo '&root' > .qmail-$i
    done
    touch .qmail-root
    chmod 644 .qmail*
)


# Install the shell init files to set MAIL and MAILDROP for MUAs 
# pine will be dealt with later
mkdir -p %destdir/etc/profile.d
cp %name.sh %name.csh %destdir/etc/profile.d
chmod +x %destdir/etc/profile.d/*

%post
# take care of pine---but only if we are not upgrading
if [ $1 = "1" ]; then
    if [ -f /usr/lib/pine.conf ]; then
       echo "Modifying /usr/lib/pine.conf"
       echo "The old  pine.conf file is saved as "
       echo "/usr/lib/pine.conf.PREQMAIL."
       TMPFILE=`mktemp -q /tmp/pine.conf.XXXXXX`
	if [ $? -ne 0 ]; then
	    echo "$0: Can't create temp file, exiting..."
	    exit 1
	fi
	trap "rm $TMPFILE* 2>/dev/null" 0
       cp -a /usr/lib/pine.conf /usr/lib/pine.conf.PREQMAIL
       sed -e '/^inbox-path/d' \
           -e '/^sendmail-path/d' \
           /usr/lib/pine.conf   > $TMPFILE.noq
       echo 'inbox-path=$MAIL' > $TMPFILE.q
       echo 'sendmail-path=/usr/sbin/sendmail  -oem -oi -t' >> $TMPFILE.q
       cat $TMPFILE.noq  $TMPFILE.q >  $TMPFILE
       mv $TMPFILE /usr/lib/pine.conf
       rm -f  $TMPFILE*  
       echo You may also want to set user-domain to the qmqpserver
    fi

    if [ -f /etc/pine.conf ]; then
       echo "Modifying /etc/pine.conf"
       echo "The old  pine.conf file is saved as "
       echo "/etc/pine.conf.PREQMAIL."
       TMPFILE=`mktemp -q /tmp/pine.conf.XXXXXX`
	if [ $? -ne 0 ]; then
	    echo "$0: Can't create temp file, exiting..."
	    exit 1
	fi
	trap "rm $TMPFILE* 2>/dev/null" 0       
       cp -a /etc/pine.conf /etc/pine.conf.PREQMAIL
       sed -e '/^inbox-path/d' \
           -e '/^sendmail-path/d' \
           /etc/pine.conf   > $TMPFILE.noq
       echo 'inbox-path=$MAIL' > $TMPFILE.q
       echo 'sendmail-path=/usr/sbin/sendmail  -oem -oi -t' >> $TMPFILE.q
       cat $TMPFILE.noq  $TMPFILE.q >  $TMPFILE
       mv $TMPFILE /etc/pine.conf
       rm -f  $TMPFILE*  
       echo You may also want to set user-domain to the qmqpserver
    fi

    echo "Now you need to run, as a minimum,"
    echo
    echo "/command/add-service.sh qmail qmail-smtpd"
    echo
    echo "to set up the *.init commands and links in /service."
	        
    
fi

%preun
# remove sysV style init if the package is removed for good
if [ $1 = 0 ]; then
    for i in %qdaemons; do
	if [ -f /command/$i.init ]; then
	    /command/remove-service.sh $i
	fi
    done
fi

%clean
rm -rf %destdir

%files 
%defattr(-,root,root)
%config(noreplace) %attr(-,alias,qmail) %qmailhome/alias/.qmail-*
%config /var/service/qmail/defaultdelivery/*
%config /var/service/*/run
%config /var/service/*/log/run
%config /etc/profile.d/*
%dir /var/service/qmail/defaultdelivery
%dir /var/service/*
%dir  /var/service/*/log
%dir %attr(-,qmaill,nofiles) /var/service/*/log/main
/usr/lib/sendmail
/usr/sbin/sendmail

