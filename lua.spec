%define	major	5.1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%define	static	%mklibname %{name} -d -s
%define	alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

Summary:	Powerful, light-weight programming language
Name:		lua
Version:	5.1.5
Release:	1
License:	MIT
URL:		http://www.lua.org/
Group:		Development/Other
Source0:	http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Patch0:		lua-5.1-dynlib.patch
Patch1:		lua-5.1-pkgconfig_libdir.patch
Patch2:		lua-5.1-modules_path.patch
Provides:	lua%{major}
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
Provides:	/usr/bin/lua

%description
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

%package -n	%{libname}
Summary:	Powerful, light-weight programming language
Group:		Development/Other

%description -n	%{libname}
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

%package -n	%{devname}
Summary:	Headers and development files for Lua
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Provides:	lua-devel = %{version}-%{release}
Provides:	lua%{major}-devel = %{version}-%{release}
Obsoletes: 	%{_lib}lua5-devel < %{version}
Obsoletes:	%{_lib}lua4-devel
Obsoletes:	%{libname}-devel

%description -n	%{devname}
This package contains the headers and development files for Lua.

%package -n	%{static}
Summary:	Static development files for Lua
Group:		Development/Other
Provides:	lua-devel-static = %{version}-%{release}
Provides:	lua-static-devel = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}
Obsoletes:	%{libname}-static-devel
Obsoletes:	%{libname}-devel-static

%description -n	%{static}
This package contains the static development files for Lua.

%prep
%setup -q
%patch0 -p1 -b .dynlib
%patch1 -p1 -b .pkgconfig
%patch2 -p1 -b .modules

sed -i -e "s|/usr/local|%{_prefix}|g" Makefile
sed -i -e "s|/lib|/%{_lib}|g" Makefile
sed -i -e "s|/usr/local|%{_prefix}|g" src/luaconf.h
sed -i -e "s|/lib|/%{_lib}|g" src/luaconf.h
sed -i -e "s|/man/man1|/share/man/man1|g" Makefile
sed -i -e "s|\$(V)|%{major}|g" src/Makefile

%build
%make linux CFLAGS="%{optflags} -fPIC -DLUA_USE_LINUX"
sed -i -e "s#/usr/local#%{_prefix}#" etc/lua.pc
sed -i -e 's/-lreadline -lncurses //g' etc/lua.pc

%install
%makeinstall_std INSTALL_TOP=%{buildroot}%{_prefix} INSTALL_LIB=%{buildroot}%{_libdir} INSTALL_MAN=%{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_libdir}/lua/%{major}/
install -d %{buildroot}%{_datadir}/lua/%{major}/
install -m 644 test/*.lua %{buildroot}%{_datadir}/lua/%{major}/

install -m 755 src/liblua.so.%{major}* %{buildroot}%{_libdir}
ln -s liblua.so.%{major} %{buildroot}%{_libdir}/liblua.so

install -d -m 755 %{buildroot}%{_libdir}/pkgconfig/
install -m 644 etc/lua.pc %{buildroot}%{_libdir}/pkgconfig/

# for update-alternatives
mv %{buildroot}%{_bindir}/lua %{buildroot}%{_bindir}/lua%{major}
mv %{buildroot}%{_bindir}/luac %{buildroot}%{_bindir}/luac%{major}

%post
/usr/sbin/update-alternatives --install %{_bindir}/lua lua %{_bindir}/lua%{major} %{alt_priority} --slave %{_bindir}/luac luac %{_bindir}/luac%{major}

%postun
[[ -f %{_bindir}/lua%{major} ]] || /usr/sbin/update-alternatives --remove lua %{_bindir}/lua%{major}

%files
%doc doc/*.html doc/*.gif
%doc COPYRIGHT HISTORY INSTALL README
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/lua
%{_datadir}/lua/%{major}/*.lua

%files -n %{libname}
%{_libdir}/liblua.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/liblua.so

%files -n %{static}
%{_libdir}/*.a
