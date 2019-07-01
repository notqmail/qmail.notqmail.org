%{expand: %%{global} _i_am_%{_target_os} %%{nil}}
# If OS is Linux
%{?_i_am_linux: %global ezroot /usr}
%{?_i_am_linux: %global ezcgi /var/www/cgi-bin}
%{?_i_am_linux: %global  rcdir /etc/ezmlm}
# If OS is not Linux
%{!?_i_am_linux: %global ezroot /usr/local}
%{!?_i_am_linux: %global ezcgi /usr/local/apache/cgi-bin}
%{!?_i_am_linux: %global rcdir /usr/local/etc/ezmlm}
# endif OS
%define dbase mysql
%define destdir %buildroot
Buildprereq: rpm >= 3.0.2
Buildroot: %_tmppath/%name-%version-root
License: GPL
Group: Utilities/System
Name: ezmlm-idx
Packager: mw@csi.hu
Prereq: rpm >= 3.0.2
Release: 112memphis
Source0: ftp://cr.yp.to/software/ezmlm-0.53.tar.gz
Source1: http://ezmlm.org/archive/0.421/%name-0.421.tar.gz
Source3: ezmlm-idx.spec-kit.tar.gz
Summary: Qmail Easy Mailing List Manager + IDX patches.
URL: http://www.ezmlm.org
Version: 0.53.421

%description 
None.  See subpackages.

%package %{dbase}
Summary: Qmail Easy Mailing List Manager + IDX patches with %{dbase} database support.
Group: Utilities/System 
Obsoletes: ezmlm-idx
Provides: EZMLM
Conflicts: ezmlm ezmlm-idx-std ezmlm-idx-pgsql

%description %{dbase}
ezmlm lets users set up their own mailing lists within qmail's address
hierarchy. A user, Joe, types

   ezmlm-make ~/SOS ~/.qmail-sos joe-sos isp.net

and instantly has a functioning mailing list, joe-sos@isp.net, with all
relevant information stored in a new ~/SOS directory.

ezmlm sets up joe-sos-subscribe and joe-sos-unsubscribe for automatic
processing of subscription and unsubscription requests. Any message to
joe-sos-subscribe will work; Joe doesn't have to explain any tricky
command formats. ezmlm will send back instructions if a subscriber sends
a message to joe-sos-request or joe-sos-help.

ezmlm automatically archives new messages. Messages are labelled with
sequence numbers; a subscriber can fetch message 123 by sending mail to
joe-sos-get.123. The archive format supports fast message retrieval even
when there are thousands of messages.

ezmlm takes advantage of qmail's VERPs to reliably determine the
recipient address and message number for every incoming bounce message.
It waits ten days and then sends the subscriber a list of message
numbers that bounced. If that warning bounces, ezmlm sends a probe; if
the probe bounces, ezmlm automatically removes the subscriber from the
mailing list.


ezmlm is easy for users to control. Joe can edit ~/SOS/text/* to change
any of the administrative messages sent to subscribers. He can remove
~/SOS/public and ~/SOS/archived to disable automatic subscription and
archiving. He can put his own address into ~/SOS/editor to set up a
moderated mailing list. He can edit ~/SOS/{headeradd,headerremove} to
control outgoing headers. ezmlm has several utilities to manually
inspect and manage mailing lists.

ezmlm uses Delivered-To to stop forwarding loops, Mailing-List to
protect other mailing lists against false subscription requests, and
real cryptographic cookies to protect normal users against false
subscription requests. ezmlm can also be used for a sublist,
redistributing messages from another list.

ezmlm is reliable, even in the face of system crashes. It writes each
new subscription and each new message safely to disk before it reports
success to qmail.

ezmlm doesn't mind huge mailing lists. Lists don't even have to fit into
memory. ezmlm hashes the subscription list into a set of independent
files so that it can handle subscription requests quickly. ezmlm uses
qmail for blazingly fast parallel SMTP deliveries.

The IDX patches add: Indexing, (Remote) Moderation, digest, make
patches, multi-language, MIME, global interface, %{dbase} database support.

%description %{dbase} -l pl
Menad<BF>er pocztowych list dyskusyjnych, ca<B3>kowicie spolszczony, mo<BF>liwo
<B6><F6> zdalnego moderowania, MIME.

%package cgi
Prefix: %ezcgi
Summary: www archiver for %name
Group: Utilities/System 
Requires:  EZMLM

%description cgi
www archiver for %name.
 

%prep 
%setup -q -T -b 0 -n ezmlm-0.53
%setup -q -D -T -a 1 -n ezmlm-0.53
mv -f ezmlm-idx-0.421/* .

patch -s < idx.patch

%build 
RC=%{rcdir}/ezmlmrc

sed -e "s}^#define TXT_ETC_EZMLMRC \"/etc/ezmlmrc\"}#define TXT_ETC_EZMLMRC \"$RC\"}" \
idx.h > idx.h.tmp
mv idx.h.tmp idx.h

echo %{ezroot}/bin > conf-bin
echo %{ezroot}/man > conf-man

if [ "%{dbase}" = "mysql" ]; then
    echo "cc -s -lz" > conf-ld    
fi


# Check for gcc version with optimizer bug

GCC_VERSION="$(cc -v 2>& 1 | tail -1 |awk '{print $3}')"

if [ "$GCC_VERSION" = "2.95" ] || [ "$GCC_VERSION" = "2.95.1" ]; then
   echo cc > conf-cc 
fi

make %{dbase}
make it install

# format man pages only if on nonlinux.
%ifos Linux
%else
make man
%endif

%install
/bin/rm -rf %destdir
RC=%{rcdir}/ezmlmrc

mkdir -p %destdir/%{ezroot}/{bin,man}
mkdir -p %destdir/%{rcdir}
mkdir -p %destdir/%ezcgi 

# Do not create cat subdirs on Linux
%ifos Linux
sed '/cat/d' MAN > MAN.tmp
mv MAN.tmp MAN
%endif 

./install %destdir/%{ezroot}/bin < BIN
./install %destdir/%{ezroot}/man < MAN

cp ezmlm-cgi %destdir/%ezcgi

# create file list for man pages
find %destdir/%{ezroot}/man -type f \
| sed -e "s}%destdir}}" -e "s}$}*}" > man-list

cp ezmlm-cgi.1 %destdir/%{ezroot}/man/man1
chmod 644 %destdir/%{ezroot}/man/man1/ezmlm-cgi.1

cp %destdir/%{ezroot}/bin/ezmlmrc %destdir/$RC
cp %destdir/%{ezroot}/bin/ezmlmrc  %destdir/$RC.dist

# Create INSTALL file for how to set up ezcgi
cat <<EOF > INSTALL.cgi
The script ezmlm-cgi is installed as  %ezcgi/ezmlm-cgi with 
permissions 0444.  In order to use it, you need to make it
SUID root.  So do

chmod 4755 %ezcgi/ezmlm-cgi

Please see INSTALL.idx 16-22) and the man page ezmlm-cgi.1 for more
details on setting up and using ezmlm-cgi.

EOF

%post %{dbase}
echo To create an ezmlmrc file for a language other than US English
echo go to this package\'s doc directory, and type 
echo "    make iso"
echo 'where "iso" is the ISO language designation.' 
echo For currently supported languages, see the INSTALL.idx
echo file, section 7.

%post cgi
cat <<EOF

The script ezmlm-cgi is installed as  %ezcgi/ezmlm-cgi with 
permissions 0444.  In order to use it, you need to make it
SUID root.  So do

chmod 4755 %ezcgi/ezmlm-cgi

Please see INSTALL.idx 16-22) in this package's doc directory
and the man page ezmlm-cgi.1 for more details on
setting up and using ezmlm-cgi.

EOF

%clean
/bin/rm -rf %destdir

%files %{dbase} -f man-list
%defattr(-, root, root)
%config %{rcdir}/ezmlm*
%doc BLURB CHANGES* FAQ.idx INSTALL INSTALL.idx  README*
%doc THANKS TODO UPGRADE.idx 
%doc DOWNGRADE.idx ezmlmrc ezmlmrc.[a-zA-Z]* 
%doc Makefile lang makelang makelang.sh warn-auto.sh
%dir %{ezroot}
%dir %{ezroot}/*
%{ezroot}/bin/*

%files cgi
%defattr(-, root, root)
%doc INSTALL.idx INSTALL.cgi ezcgirc ezcgi.css
%attr(0444,root,root) %ezcgi/*
%{ezroot}/man/man1/ezmlm-cgi.1.gz
