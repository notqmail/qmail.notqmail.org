%define destdir %buildroot
%global myhome /usr/local/clockspeed
Buildroot: %_tmppath/%name-%version-root
License: Check with djb@cr.yp.to
Group: Utilities/System
Name: clockspeed
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Release: 112memphis
Requires: leapsecs
Source0: http://cr.yp.to/%name/%name-%version.tar.gz
Summary: Tools to make sure the system clock is accurate
URL: http://cr.yp.to/%name.html
Version: 0.62

%description
clockspeed uses a hardware tick counter to compensate for a persistently
fast or slow system clock. Given a few time measurements from a reliable
source, it computes and then eliminates the clock skew.

sntpclock checks another system's NTP clock, and prints the results in a
format suitable for input to clockspeed. sntpclock is the simplest
available NTP/SNTP client.

taiclock and taiclockd form an even simpler alternative to SNTP. They
are suitable for precise time synchronization over a local area network,
without the hassles and potential security problems of an NTP server.

This version of clockspeed can use the Pentium RDTSC tick counter or the
Solaris gethrtime() nanosecond counter.


%prep 
%setup -q
%patch -p1

%build
echo %myhome > conf-home
make
sleep 1

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

This rpm applies a patch to the sources to fix an
incompatibility in errno declaration.  
" >> README_rpm

%install
rm -rf %destdir

# The next steps make sure that instcheck and install
# will do their job in %destdir%myhome and not 
# in %myhome

mkdir -p %destdir%myhome 
echo %destdir%myhome > conf-home
awk '!/cat|leapsecs.dat/ { sub("\"/\"","\"%destdir\""); print}' hier.c > hier.c.tmp
mv hier.c.tmp hier.c
make install instcheck
./install
./instcheck


%clean
rm -rf  %destdir


%files
%defattr(-,root,root)
%doc BLURB CHANGES INSTALL README* 
%doc THANKS TODO VERSION 
%myhome

