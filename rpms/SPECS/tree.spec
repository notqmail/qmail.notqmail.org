Summary: A utility which displays a tree view of the contents of directories.
Name: tree
Version: 1.5.0
Release: 1
Group: Applications/File
License: GPL
Url: http://mama.indstate.edu/users/ice/tree/
Source: ftp://mama.indstate.edu/linux/tree/tree-1.5.0.tgz
Patch1: tree-1.2-carrot.patch
Patch2: tree-1.2-colour.patch
Patch3: tree-1.2-no-strip.patch
Prefix: /usr
BuildRoot: /var/tmp/tree-root

%description
The tree utility recursively displays the contents of directories in a
tree-like format.  Tree is basically a UNIX port of the DOS tree
utility.

%prep
%setup -q
%patch1 -p1 -b .carrot
%patch2 -p1 -b .colour
%patch3 -p1 -b .no-strip

%build
rm -f tree
make CFLAGS="$RPM_OPT_FLAGS" CPPFLAGS=$(getconf LFS_CFLAGS)

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT/usrman/man1

make	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	install

chmod -x $RPM_BUILD_ROOT%{_mandir}/man1/tree.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/tree
%{_mandir}/man1/tree.1*
%doc README

%changelog
* Mon Sep 13 2004 Tim Waugh <twaugh@redhat.com> 1.5.0-1
- 1.5.0 (bug #131854).
- No longer need utf8 or gcc34 patches.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Tim Waugh <twaugh@redhat.com> 1.4b3-2
- Fixed compilation with GCC 3.4.

* Wed Aug 13 2003 Tim Waugh <twaugh@redhat.com> 1.4b3-1
- Upgraded (bug #88525).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov  8 2002 Tim Waugh <twaugh@redhat.com> 1.2-21
- Assume -N except if -q is given (bug #77517).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 23 2002 Tim Waugh <twaugh@redhat.com> 1.2-18
- Don't explicitly strip binaries (bug #62569).
- Fix malloc/realloc problems (bug #56858).

* Fri Mar 22 2002 Tim Waugh <twaugh@redhat.com> 1.2-17
- Large file support (bug #61456).

* Wed Feb 27 2002 Tim Waugh <twaugh@redhat.com> 1.2-16
- Rebuild in new environment.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Oct  5 2001 Tim Waugh <twaugh@redhat.com> 1.2-14
- Fix size format (bug #54298).
- Don't use colours by default (bug #25389).

* Mon Jul 30 2001 Tim Waugh <twaugh@redhat.com> 1.2-13
- Change Copyright: to License:.
- Don't dump core if LS_COLORS is too big (bug #50016).

* Wed May 30 2001 Tim Waugh <twaugh@redhat.com> 1.2-12
- Sync description with specspo.

* Tue Oct 10 2000 Tim Waugh <twaugh@redhat.com> 1.2-11
- Don't blabber about carrots in the man page (bug #18823)
- Use RPM_OPT_FLAGS while building

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- remove executable bit from man page (Bug #9035)
- deal with rpm compressing man pages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built package for 6.0

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 29 1998 Cristian Gafton <gafton@redhat.com>
- installing in /usr/bin

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- updated version
- fixed src url

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
