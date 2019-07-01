%define destdir %buildroot
%global myhome /usr/local
Buildroot: %_tmppath/%name-%version-root
License: Check with djb
Group: Utilities/System
Name: ucspi-tcp
Obsoletes: rblsmtpd
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Patch1: %name-%version.nobase.patch
Patch2: %name-%version.a_record.patch
Provides: tcp-superserver
Release: 112memphis
Source0: http://cr.yp.to/%name/%name-%version.tar.gz
Summary: partial replacement for inetd+tcpd
URL: http://cr.yp.to/%name.html
Version: 0.88

%description 
tcpserver and tcpclient are easy-to-use command-line tools for building
TCP client-server applications.

tcpserver waits for incoming connections and, for each connection, runs
a program of your choice. Your program receives environment variables
showing the local and remote host names, IP addresses, and port numbers.

tcpserver offers a concurrency limit to protect you from running out of
processes and memory. When you are handling 40 (by default) simultaneous
connections, tcpserver smoothly defers acceptance of new connections.

tcpserver also provides TCP access control features, similar to
tcp-wrappers/tcpd\'s hosts.allow but much faster. Its access control
rules are compiled into a hashed format with cdb, so it can easily deal
with thousands of different hosts.

This package includes a recordio tool that monitors all the input and
output of a server.

tcpclient makes a TCP connection and runs a program of your choice. It
sets up the same environment variables as tcpserver.

This package includes several sample clients built on top of tcpclient:
who@, date@, finger@, http@, tcpcat, and mconnect.

tcpserver and tcpclient conform to UCSPI, the UNIX Client-Server Program
Interface, using the TCP protocol. UCSPI tools are available for several
different networks.


%prep
%setup -q
%patch -p1
%patch1 -p1
%patch2 -p1

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

This rpm applies the following patches:

0: errno; to correct an incompatibility in errno declaration
1: nobase; the default rbl base is not avaialble noncommercially anymore
2: a_record; many rbl databases provide now A records instead of txt
  
Since this rpm applies patches to the sources, you cannot distribute it
publicly.  
" >> README_rpm

%install
rm -rf %destdir

# The next steps make sure that instcheck and install
# will do their job in %destdir%myhome and not 
# in %myhome


mkdir -p %destdir%myhome
echo %destdir%myhome > conf-home
make install instcheck
./install
./instcheck


%clean
rm -rf  %destdir  

%files
%defattr(-,root,root)
%doc TODO	VERSION
%doc CHANGES    README*			
%myhome/bin/*
