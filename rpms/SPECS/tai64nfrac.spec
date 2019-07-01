%define destdir %buildroot
%global myhome /usr/local
BuildRoot: %_builddir/%{name}-%{version}-buildroot
Group: Utilities/System
License: Free
Name: tai64nfrac
Packager: mw@csi.hu
Release: 112memphis
Source0: %{name}-%{version}.tar.gz
Summary: Convert external TAI64N timestamps to fractional seconds since epoch.
URL: http://www.qmail.org
Version: 0.01

%description

%prep
%setup -q

%build
make DESTDIR=%destdir MYHOME=%myhome 

%install
rm -rf %destdir


make DESTDIR=%destdir MYHOME=%myhome install command_link

%clean
rm -rf %destdir

%files
%defattr(-,root,root,-)
%doc README
%myhome/bin/%name
/command/%name

%changelog
* Sun Jun  1 2003 Mate Wierdl <mw@csi.hu> 
- Initial build.


