%define destdir %buildroot
%global myhome /usr/local
Buildroot: %_tmppath/%name-%version-root
License: Check with djb
Group: Utilities/System
Name: djbdns
Obsoletes: dnscache
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Release: 004patch
Requires: ucspi-tcp >= 0.88 daemontools >= 0.70
Source0: ftp://cr.yp.to/djbdns/%name-%version.tar.gz
Summary: A bind replacement
URL: http://cr.yp.to/dnscache.html
Version: 1.05

%description 
   dnscache maintains a limited-size cache of DNS information, 1 megabyte
   by default. When the cache fills up, dnscache smoothly discards old
   cache entries. 

   You can easily configure dnscache to send queries for a particular
   domain to a particular set of servers, such as ``split DNS'' internal
   servers behind a firewall. All you have to do is put the server IP
   addresses into a file named after the domain.

   The djbdns package includes three servers that publish local host
   information: tinydns, walldns, and rbldns. Every aspect of
   configuration was rethought from the perspective of an overworked
   administrator who has better things to do than play with DNS.

   tinydns handles basic DNS service. The tinydns-data file format
   combines the flexibility of zone files with the convenience of modern
   zone-building tools. Host information is stored in one file. PTR
   records are handled automatically. Changes can be scheduled in
   advance, with TTLs handled automatically.

   tinydns has several load-balancing features. It automatically
   selects a random set of 8 servers from a cluster of any size. It
   allows easy removal of dead servers by external monitoring
   tools. It also supports client differentiation, checking the
   client's IP address and choosing one of several clusters
   accordingly.  walldns is a reverse DNS wall. It lets firewalled
   sites access name-checking servers without revealing true host
   information.

   rbldns publishes lists of IP addresses, such as RBL or DUL, through
   DNS. This could be done with a general-purpose server, but rbldns uses
   much less memory and much less disk space.

   Databases for tinydns, pickdns, and rbldns are compiled into cdb
   format. The servers start up instantly, even if the database is a
   gigabyte or more. While a new database is being compiled, the servers
   continue to answer queries from the old database. There is no gap in
   DNS service when the new database is finished. The old database is
   left in place if anything goes wrong.


%prep
%setup -q

%patch -p1

%build

echo %myhome > conf-home
 
make

# make may notice only 1 sec changes
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

Since this rpm applies a patch to the sources (to fix an
incompatibility in errno declaration), you cannot distribute it
publicly.  
" >> README_rpm


%install
rm -rf %destdir

# The next steps make sure that instcheck and install
# will do their job in %destdir%myhome and not 
# in %myhome

mkdir -p %destdir%myhome %destdir/etc
echo %destdir%myhome > conf-home
sed 's}/}%destdir}' hier.c > hier.c.tmp
mv hier.c.tmp hier.c
make install instcheck
./install
./instcheck


%clean
rm -rf  %destdir  

%changelog
* Tue Oct 25 2005 Mate Wierdl <mw@csi.hu> - 1.05-004patch
- Changed Copyright to License;
- inserted sleep to help make; fixed compilation bug reported by Eric Calder


* Mon Oct 20 2003 Mate Wierdl <mw@csi.hu> 1.05-003patch
- Bugfix: change tmppath to _tmppath; thx James A. Kennemore, Jr.

%files
%defattr(-,root,root)
%doc CHANGES    README*
%doc TODO	VERSION
/etc/*			
%myhome/bin/*


