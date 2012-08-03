#
# spec file for package ccache (Version 2.4)
#
# Copyright (c) 2005 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild

Name:         ccache
Summary:      Compiler Cache
Version:      2.4
Release:      17.51
Group:        Development/Languages/C and C++
License:      GPL
Autoreqprov:  on
URL:          http://ccache.samba.org/
Source:       http://samba.org/ftp/ccache/ccache-%{version}.tar.gz
Patch0:       basedir.patch
Patch1:       umask.patch
Patch2:       maxsize.patch
Provides:     distcc:/usr/bin/ccache
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Ccache is a compiler cache. It acts as a caching pre-processor to C/C++
compilers, using the -E compiler switch and a hash to detect when a
compilation can be satisfied from cache. This often results in a
speedup for common compilations.

Note that this ccache package is meant to use only with the openSUSE build
service.  For general use, the package that comes with the distro is probably
what you really want.


Authors:
--------
    Andrew Tridgell

%prep
%setup

%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}
make

# SHARING A CACHE
# 
# A group of developers can increase the cache hit rate by
# sharing a cache directory. The hard links however cause unwanted side
# effects, as all links to a cached file share the file's modification
# timestamp. This results in false dependencies to be triggered by
# timestamp-based build systems whenever another user links to an
# existing file. Typically, users will see that their libraries and
# binaries are relinked without reason. To share a cache without side
# effects, the following conditions need to be met:   
# 
#     * Use the same CCACHE_DIR environment variable setting
#     * Set the CCACHE_NOLINK environment variable
#     * Make sure everyone sets the CCACHE_UMASK environment variable to
#       002, this ensures that cached files are accessible to everyone
#       in the group. 
#     * Make sure that all users have write permission in the entire
#       cache directory (and that you trust all users of the shared
#       cache). 
#     * Make sure that the setgid bit is set on all directories in the
#       cache. This tells the filesystem to inherit group ownership for
#       new directories. The command "chmod g+s `find $CCACHE_DIR -type
#       d`" might be useful for this.  

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
ln -s /usr/bin/ccache $RPM_BUILD_ROOT/usr/local/bin/gcc
ln -s /usr/bin/ccache $RPM_BUILD_ROOT/usr/local/bin/g++
ln -s /usr/bin/ccache $RPM_BUILD_ROOT/usr/local/bin/cc
ln -s /usr/bin/ccache $RPM_BUILD_ROOT/usr/local/bin/c++
mkdir -p $RPM_BUILD_ROOT/.ccache
chmod a+s `find $RPM_BUILD_ROOT/.ccache -type d`

%files
%defattr(-,root,root)
%doc COPYING README web/*.html
%doc %{_mandir}/man1/ccache.1*
%{_bindir}/ccache
/usr/local/bin/gcc
/usr/local/bin/g++
/usr/local/bin/cc
/usr/local/bin/c++
%defattr(1777,root,root)
%dir /.ccache

%clean
rm -rf $RPM_BUILD_ROOT

