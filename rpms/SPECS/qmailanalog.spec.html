%define destdir %buildroot
%global myhome /usr/local/qmailanalog
Buildroot: %_builddir/%{name}-%version-root
License: Check with djb
Group: Utilities/System
Name: qmailanalog
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Release: 112memphis
Requires: qmail >= 1.01 functions > 1
Source: ftp://cr.yp.to/software/%name-%version.tar.gz
Summary: Analysis tools for qmail
URL: http://cr.yp.to/%name.html
Version: 0.70

%description
qmailanalog is a collection of tools to help you analyze qmail-send's
activity record. It supplies statistics to answer a wide variety of
questions:

   * overall: how many messages? recipients? attempts? etc.

   * ddist: how soon were 50 percent of the messages delivered?
            90 percent? 95 percent? 99 percent?

   * rxdelay: what's the best order of recipients for mailing lists?

   * recipients, rhosts: who's getting mail? bytes? messages? attempts?

   * successes, failures, deferrals: why? how often? how much delay?

   * senders, suids: messages? bytes? load? recipients? attempts? delay?

qmailanalog also includes several tools to focus attention on particular
senders, recipients, or messages.

%prep
%setup -q
%patch -p1

%build
make man prog
sleep 1
# add %myhome/qmailanalog/bin to PATH via shellinit files
echo 'setenv  PATH "${PATH}:%myhome/bin"' > qmailanalog.csh
echo 'appath PATH %myhome/bin' > qmailanalog.sh

%install

/bin/rm -rf %destdir

mkdir -p %destdir%myhome
echo %destdir%myhome > conf-home

grep -v cat1 hier.c > hier.c.tmp
mv hier.c.tmp hier.c

make install instcheck
./install
./instcheck

#install shell init files
mkdir -p %destdir/etc/profile.d
cp qmailanalog.sh %destdir/etc/profile.d
cp qmailanalog.csh %destdir/etc/profile.d
chmod a+x %destdir/etc/profile.d/*

%clean
/bin/rm -rf %destdir

%files
%config /etc/profile.d/*
%doc ACCOUNTING BLURB CHANGES INSTALL MATCHUP README THANKS TODO
%doc VERSION
%myhome
