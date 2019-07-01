%define destdir %buildroot
%global myhome /
Buildroot: %_tmppath/%name-%version-root
License: Check with djb@cr.yp.to
Group: Utilities/System
Name: checkpassword
Packager: mw@csi.hu
Patch: %name-%version.errno.patch
Provides: CHECKPASSWORD 
Release: 112memphis
Source: ftp://cr.yp.to/checkpwd//%name-%version.tar.gz 
Summary: Password checking software
URL: http://cr.yp.to/checkpwd.html
Version: 0.90

%description 
checkpassword provides a simple, uniform password-checking interface
to all root applications. It is suitable for use by applications such as
login, ftpd, and pop3d.

There are checkpassword-compatible tools that support alternate password
databases, secret login names, long passwords, subaccounts, one-time
passwords, detailed accounting, and many other features. Applications
that use the checkpassword interface will work with all of these tools.
Several tools have been specifically designed to support POP toasters.


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

Since this rpm applies a patch to the sources (to fix an
incompatibility in errno declaration), you cannot distribute it
publicly.  
" >> README_rpm

%install
rm -rf %destdir

# The next steps make sure that instcheck and install
# will do their job in %destdir%myhome and not 
# in %myhome

mkdir -p %destdir%myhome/bin
echo %destdir%myhome > conf-home
make install instcheck
./install
./instcheck


%clean
rm -rf  %destdir

%files
%defattr(-,root,root)
%doc CHANGES    README*
%doc TODO       VERSION
%myhome/bin/*

