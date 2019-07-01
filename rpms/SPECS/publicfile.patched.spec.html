%define destdir %buildroot
%global myhome /usr/local/%name
Buildroot: %_tmppath/%name-%version-root
License: Check with djb
Group: System Environment/Daemons
Name: publicfile
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Provides: publicfile
Release: 112memphis
Requires: ucspi-tcp daemontools > 0.53
Source: http://cr.yp.to/%name/%name-%version.tar.gz
Summary: publicfile supplies files to the public through HTTP and FTP
URL: http://cr.yp.to/%name.html
Version: 0.52

%description
   publicfile supplies files to the public through HTTP and FTP.

   Security features:
     * Before accepting any commands, publicfile chroot()s to the public
       file area and sheds root privileges.
     * publicfile doesn't let users log in. Intruders can't use
       publicfile to check your usernames and passwords.
     * publicfile refuses to supply files that are unreadable to owner,
       unreadable to group, or unreadable to world.
     * publicfile never attempts to modify the public file area. It
       refuses all HTTP and FTP modification commands.
     * publicfile never runs any other programs. It does not support HTTP
       CGI or FTP SITE EXEC.
     * publicfile avoids bug-prone libraries such as stdio.
     * The publicfile FTP server uses local ports above 1024 for PORT
       connections.
     * The publicfile FTP server prohibits remote ports below 1024 for
       PORT.
     * The publicfile FTP server prohibits PORT relaying.
     * The publicfile FTP server includes automatic PASV IP protection.

   HTTP features:
     * publicfile supports virtual hosts through the Host field.
     * publicfile supports virtual hosts through absolute URLs.
     * publicfile supports HTTP/1.1 persistent connections.
     * publicfile supports HTTP/1.1 chunked responses.
     * publicfile supports user-controlled content types.
     * publicfile supports exact-prefix If-Modified-Since.

   FTP features:
     * publicfile has built-in LIST and NLST commands. You don't have to
       bother setting up bin/ls, shared libraries, et al. inside the
       public file area.
     * publicfile provides EPLF LIST responses, including options "i",
       "s", and "m".
     * publicfile supports restarted transfers.
     * publicfile supports pipelining.

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

This rpm applies the following patch:

0: errno; to correct an incompatibility in errno declaration

Since this rpm applies this patch to the sources, you cannot distribute it
publicly.
" >> README_rpm

%install
rm -rf %destdir

mkdir -p %destdir%myhome 
# The next steps make sure that instcheck and install
# will do their job in %destdir%myhome and not
# in %myhome

echo %destdir%myhome > conf-home
make install instcheck
./install
./instcheck


%clean
rm -rf %destdir 

%files
%defattr(-,  root, root)
%doc CHANGES    README*	TODO		
%myhome




