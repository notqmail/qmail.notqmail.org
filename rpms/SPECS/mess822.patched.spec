%define destdir %buildroot
%global myhome /usr/local
Buildroot: %_tmppath/%name-%version-root
License: Check with djb@cr.yp.to
Group: Utilities/System
Name: mess822
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Release: 112memphis
Requires: qmail leapsecs
Source0: ftp://cr.yp.to/software/%name-%version.tar.gz
Summary: mess822 is a library for parsing Internet mail messages. 
URL: http://cr.yp.to/%name.html
Version: 0.58 

%description
mess822 is a library for parsing Internet mail messages. The mess822
package contains several applications that work with qmail:

   * ofmipd rewrites messages from dumb clients. It supports a database
     of recognized senders and From lines, using cdb for fast lookups.

   * new-inject is an experimental new version of qmail-inject. It
     includes a flexible user-controlled hostname rewriting mechanism.

   * iftocc can be used in .qmail files. It checks whether a known
     address is listed in To or Cc.

   * 822header, 822field, 822date, and 822received extract various
     pieces of information from a mail message.

   * 822print converts a message into an easier-to-read format.

mess822 supports the full complexity of RFC 822 address lists, including
address groups, source routes, spaces around dots, etc. It also supports
common RFC 822 extensions: backslashes in atoms, dots in phrases,
addresses without host names, etc. It extracts each address as an
easy-to-use string, with a separate string for the accompanying comment.

mess822 converts RFC 822 dates into libtai's struct caltime format. It
supports numeric time zones, the standard old-fashioned time zones, and
many nonstandard time zones.

mess822 is fast. For example, extracting 10000 addresses from a 160KB To
field takes less than a second on a Pentium-100.

%prep
%setup -q
%patch -p1

%build

echo %myhome > conf-home
make prog
sleep 1

# Fix hier.c so that nothing gets installed
# in man/cat?.
awk '!/cat|leapsecs.dat/ { sub("/etc","%destdir/etc"); print}' hier.c > hier.c.tmp
mv hier.c.tmp hier.c

COMPILER="Compiler: $(gcc -v 2>&1 | tail -1)"
HARDWARE="Hardware: $(uname -m)"
LIBRARY="Library: $(rpm -q glibc)"
OSVERSION="OSversion: $(uname -sr)"
PACKAGER="Packager: %packager"
REDHATRELEASE="RedHat release: $(cat /etc/redhat-release)"
RPMVERSION="rpm version: $(rpm -q rpm)"

echo "The %name rpm was created in the following environment:
" > README_rpm

echo "$COMPILER
$HARDWARE
$LIBRARY
$OSVERSION
$PACKAGER
$REDHATRELEASE
$RPMVERSION

The packager above has made a good-faith attempt to ensure
that the package behaves correctly.

This rpm applies the following patch:

0: errno; to correct an incompatibility in errno declaration

Since this rpm applies this patch to the sources, you cannot distribute it
publicly.
" >> README_rpm

%install
/bin/rm -rf %destdir

mkdir -p %destdir%myhome 
# The next steps make sure that instcheck and install
# will do their job in %destdir%myhome and not
# in %myhome

echo %destdir%myhome > conf-home

make install instcheck
./install
./instcheck

%clean
/bin/rm -rf %destdir


%files
%defattr(-,root,root)
%doc BLURB CHANGES INSTALL README 
%doc THANKS TODO VERSION 
%myhome/bin/*
%myhome/man/*/*
%myhome/include/*
%myhome/lib/*
