BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Group: system/utilities
License: djb
Name: leapsecs
Release: 112memphis
Source0: leapsecs.dat
Summary: leapsecs.dat needed by mess822 and clockspeed
Version: 1

%description 

Installs /etc/leapsecs.dat needed by the mess822 and clockspeed
packages


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
cp %_sourcedir/leapsecs.dat $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0644,root,root) /etc/leapsecs.dat


%changelog
* Wed Oct 22 2003 mw <mw@csi.hu> 
- Initial build.


