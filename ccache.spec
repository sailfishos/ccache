Name:         ccache
Summary:      Compiler Cache
Version:      3.1.9
Release:      17.51
Group:        Development/Languages/C and C++
License:      GPL3
URL:          http://ccache.samba.org/
Source:       http://samba.org/ftp/ccache/ccache-%{version}.tar.gz
Patch0:       maxsize.patch
Provides:     distcc:/usr/bin/ccache
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
BuildRequires: zlib-devel

%description
Ccache is a compiler cache. It acts as a caching pre-processor to C/C++
compilers, using the -E compiler switch and a hash to detect when a
compilation can be satisfied from cache. This often results in a
speedup for common compilations.

%prep
%setup
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/.ccache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS.txt GPL-3.0.txt INSTALL.txt LICENSE.txt MANUAL.txt NEWS.txt README.txt
%doc %{_mandir}/man1/ccache.1*
%{_bindir}/ccache
