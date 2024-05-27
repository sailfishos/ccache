Name:         ccache
Summary:      C/C++ compiler cache
Version:      4.9.1
Release:      1
License:      GPLv3+
URL:          https://github.com/sailfishos/ccache
Source:       %{name}-%{version}.tar.xz
Provides:     distcc:/usr/bin/ccache
BuildRequires: cmake
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(zlib)

%description
ccache is a compiler cache.  It speeds up recompilation of C/C++ code
by caching previous compiles and detecting when the same compile is
being done again.  The main focus is to handle the GNU C/C++ compiler
(GCC), but it may also work with compilers that mimic GCC good enough.

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
%cmake \
 -DENABLE_DOCUMENTATION=OFF \
 -DOFFLINE=1 \
 -DREDIS_STORAGE_BACKEND=OFF
%cmake_build

%install
%cmake_install

%files
%license GPL-3.0.txt
%{_bindir}/ccache
