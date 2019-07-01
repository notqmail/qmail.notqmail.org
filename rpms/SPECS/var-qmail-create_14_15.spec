# Customize
# Intended name of binary package. 
# For now, the name of the package will be `qmail' so 
# rpm can upgrade older qmail rpms properly; the `Obsoletes' tag is 
# just not doing what we need.  The name below refers to the prefix name for 
# everything else in the binary package but the name. The actual name of the 
# package is determined in the `VNAME=qmail' assignment below.
%define vname var-qmail_14_15
%define vsrcname var-qmail
# qmail's home directory
%define qmailhome /var/qmail
# If you redistribute the created binary qmail package, 
# you must change this
%define vpackager mw@csi.hu
# If you change anything in this package, change this
Packager: mw@csi.hu
Release: 112patch_14_15
# end customize: change below at your own risk
%define destdir %buildroot
%define distdir %vname-%version
%define vdestdir /tmp/%vname-root
%define vqmailhome %vdestdir%qmailhome
# Change below, at your own (high) risk
Buildroot: /tmp/%name-root
License: Check with djb@cr.yp.to
ExclusiveOS: Linux
Group: Utilities/System
Name: var-qmail-create
# errno, fixes errno declaration 
Patch14:qmail-%version.errno.patch
# qmail_local, fixes and_or typo in qmail-local.c 
Patch15:qmail-%version.qmail_local.patch
Requires: rpm >= 3
Source0: ftp://cr.yp.to/software/qmail-%version.tar.gz
Source1: %name-%vsrcname.spec
Source2: %name-add-account
Source3: %name-add-group
Source4: %name-Makefile
Source5: %name-README_rpm
Source6: %name.mem_replace.sh
Summary: Creates binary package for qmail
URL: http://www.qmail.org/
Version: 1.03

%description
This package creates a binary package for qmail.

%prep
%setup -q -n qmail-%version






%patch14 -p1
%patch15 -p1
%build

# create auto_uids.c so that the qmail users
# do not have to be added
cat > auto_uids.c <<EOF
int auto_uida = 1;
int auto_uidd = 1;
int auto_uidl = 1;
int auto_uido = 1;
int auto_uidp = 1;
int auto_uidq = 1;
int auto_uidr = 1;
int auto_uids = 1;
int auto_gidq = 1;
int auto_gidn = 1;
EOF

# Fix Makefile so that auto_uids.c 
# does not get created
sed '/auto_uids.c: /,/^$/ s/^/# /' Makefile > Makefile.tmp
mv Makefile.tmp Makefile

# make does not notice short time intervals
sleep 1
# Fix hier.c so that nothing gets installed
# in man/cat?.
grep -v "man/cat*" hier.c > hier.c.tmp 
mv hier.c.tmp hier.c

echo %qmailhome > conf-qmail
make -o auto_uids.c auto_uids.o
make -o auto_uids.c
make man

# get a list of files to be put in the distribution
grep "c(" hier.c | awk -F, '{ print $3 }'| sed 's/\"//g' > distr_files

mkdir %distdir
cp $(cat distr_files) %distdir

# these are needed for installation
mv config config-fast dnsfq dnsip dnsptr hostname \
idedit instcheck ipmeprint %distdir

# Now find out the byte positions of auto_uid* and auto_gid* in 
# instcheck qmail-lspawn qmail-queue qmail-rspawn qmail-showctl 
# qmail-start.  install will be treated separately.
# We just need to find out the byte position of auto_uida.  

# for make
sleep 1
PROGS="instcheck qmail-lspawn qmail-queue qmail-rspawn qmail-showctl qmail-start"
# change uids
awk -F"=" '/int/ { $2=($2 + 1); print $1"= "$2";" }' auto_uids.c \
    > auto_uids.c.tmp
mv auto_uids.c.tmp auto_uids.c

make 

# find byteposition of auto_uida
for prog in $PROGS; do
    cmp -l $prog %distdir/$prog |
    awk 'NR==1 { print $1 }' > $prog.auto_uida
done

# Now deal with install:
# In the distribution, we  need an install 
# that thinks ~qmail=%vqmailhome
sleep 1
echo %vqmailhome >  conf-qmail
make install
mv install %distdir

sleep 1
# change uids
awk -F"=" '/int/ { $2=($2 + 1); print $1"= "$2";" }' auto_uids.c \
    > auto_uids.c.tmp
mv auto_uids.c.tmp auto_uids.c
make install

# find byteposition of auto_uida
cmp -l install  %distdir/install |
    awk 'NR==1 { print $1 }' > install.auto_uida


# generate arguments for idedit
bytepos() {
    i=1
    byte=$[ $1 - 1 ]
    while [ $i -le 40 ]; do
        echo -n "$byte "
        byte=$[ byte + 1]
    i=$[ i + 1 ]
    done   
}

ALLPROGS="install $PROGS"
for prog in $ALLPROGS; do
    bytepos $(cat $prog.auto_uida) > $prog.idedit_args
done

newname() {
    basename $1|sed 's}%name-}}'  
}
for i  in %SOURCE2 %SOURCE3 %SOURCE4 %SOURCE5; do
    cp $i %distdir/$(newname $i)
done

chmod +x %distdir/add-*

# Fix Makefile and README_rpm for the distr
(
cd %distdir

echo "
VQMAILHOME=%vqmailhome
HOSTNAME=hostname -f
" | %SOURCE6 Makefile > Makefile.tmp
mv Makefile.tmp Makefile

COMPILER="Compiler: $(gcc -v 2> gcc.v; cat gcc.v | tail -1; rm -f gcc.v)"
HARDWARE="Hardware: $(uname -m)"
LIBRARY="Library: $(rpm -q glibc)"
OSVERSION="OSversion: $(uname -sr)"
PACKAGER="Packager: %vpackager"
REDHATRELEASE="RedHat release: $(cat /etc/redhat-release)"
RPMVERSION="rpm version: $(rpm -q rpm)"

echo "This qmail rpm was created in the following environment:

$COMPILER
$HARDWARE
$LIBRARY
$OSVERSION
$PACKAGER
$REDHATRELEASE
$RPMVERSION

This is a patched version of qmail; you cannot distribute it.
The patches used are

14 errno, fixes errno declaration
15 qmail_local, fixes and_or typo in qmail-local.c

Where I did not indicate the author, the patch is from www.qmail.org,
and that is where you should go to read about what the patches do.
" > README_rpm
) 

# Fix %vname.spec
echo '
DISTDIR=%distdir
QMAILHOME=%qmailhome
VRELEASE=%release
VDESTDIR=%vdestdir
VERSION=%version
VNAME=qmail
VPACKAGER=%vpackager
VQMAILHOME=%vqmailhome
' |  %SOURCE6 %SOURCE1 > %vname.spec

# Enter arguments to idedit in Makefile
for prog in $ALLPROGS; do
    sed "s/$prog XXX/$prog $(cat $prog.idedit_args)/" %distdir/Makefile \
    > %distdir/Makefile.tmp
    mv %distdir/Makefile.tmp %distdir/Makefile 
done

# These will go in the RH doc dir
mkdir %distdir/doc
cp BLURB* CHANGES README SECURITY THANKS THOUGHTS TODO %distdir/doc
cp %distdir/README_rpm %distdir/doc

tar zcvf %distdir.tar.gz %distdir

%install
rm -rf %destdir

# Maybe rpm will be able to expand _sourcedir and _specdir
# on the install system; for now, we can only do this.
# In the post section we'll copy all to the right place.
mkdir -p %destdir{%_sourcedir,%_specdir}
cp %vname.spec %destdir%_specdir
cp %distdir.tar.gz %destdir%_sourcedir

echo "
This rpm creates a patched version of qmail; you cannot distribute it or 
the resulting %vname package.

The patches used are

14 errno, fixes errno declaration
15 qmail_local, fixes and_or typo in qmail-local.c

Where I did not indicate the author, the patch is from www.qmail.org,
and that is where you should go to read about what the patches do. 
" > %name.README

%clean
rm -rf %destdir

%post
# create a spec file, and then run rpm on the
# install system to find out _specdir and _sourcedir
### next rpm will simplify this a great deal

TMPFILE=$(mktemp -q /tmp/1.spec.XXXXXX)
if [ $? -ne 0 ]; then
    echo "$0: Can't create temp file, exiting..."
    exit 1
fi

cat > $TMPFILE <<EOF
Name: 1
Summary: 1
Version: 1
Release: 1
Group: 1
License: 1

%%%description
1

%%%post

ISPECDIR %%_specdir
ISOURCEDIR %%_sourcedir
EOF

ISPECDIR=$(rpm -q --specfile --scripts $TMPFILE |
    grep ISPECDIR| awk '{ print $2 }')
ISOURCEDIR=$(rpm -q --specfile --scripts $TMPFILE |
    grep ISOURCEDIR| awk '{ print $2 }')

if [ "$ISPECDIR" != "%_specdir" ]; then
    cp %_specdir/%vname.spec $ISPECDIR
fi

if [ "$ISOURCEDIR" != "%_sourcedir" ]; then
    cp %_sourcedir/%distdir.tar.gz $ISOURCEDIR
fi

echo The spec file you want to use is %vname.spec

%files
%doc %name.README
%_specdir/*
%_sourcedir/*


%changelog
* Tue Oct 25 2005 Mate Wierdl <mw@csi.hu> - 1.03-112patch_14_15
- Changed Copyright to License, added some sleeps for make

* Thu Jan  9 2003 Mate Wierdl <mw@csi.hu>
- Added errno and qmail_local patches

* Tue Jun 11 2002 Mate Wierdl <mw@csi.hu>
- Added pop3d_stat patch

* Thu Jun  6 2002 Mate Wierdl <mw@csi.hu>
- Added ext-todo, syncdir, qmtpc, condredirect patches

* Thu May  2 2002 Mate Wierdl <mw@csi.hu>
-- Added queuevar patch

* Mon Jul 26 1999 Mate Wierdl <mw@moni.msci.memphis.edu>
-- First version 



