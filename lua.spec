%define major 5.3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s
%define alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

Summary:	Powerful, light-weight programming language
Name:		lua
Version:	5.3.5
Release:	2
License:	MIT
Group:		Development/Other
Url:		http://www.lua.org/
Source0:	http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:	lua.pc
Patch0:		lua-5.3.1-dynlib.patch
Patch1:		lua-5.2.0-modules_path.patch
Patch2:		lua52-compat-old-versions.patch
Provides:	lua%{major} = %{EVRD}
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncursesw)
Requires(post,postun):	chkconfig

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

%files
%doc doc/*{.html,.css,.gif,.png}
%doc README
%{_bindir}/*
%{_mandir}/man1/*

%post
/usr/sbin/update-alternatives --install %{_bindir}/lua lua %{_bindir}/lua%{major} %{alt_priority} --slave %{_bindir}/luac luac %{_bindir}/luac%{major}

%postun
[[ -f %{_bindir}/lua%{major} ]] || /usr/sbin/update-alternatives --remove lua %{_bindir}/lua%{major}

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Powerful, light-weight programming language
Group:		Development/Other

%description -n %{libname}
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

%files -n %{libname}
%{_libdir}/liblua.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers and development files for Lua
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Requires:	%{name} = %{EVRD}
Provides:	liblua%{major}-devel = %{EVRD}
Provides:	lua-devel = %{EVRD}
Provides:	lua%{major}-devel = %{EVRD}

%description -n %{devname}
This package contains the headers and development files for Lua.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/liblua.so

#----------------------------------------------------------------------------

%package -n %{staticname}
Summary:	Static development files for Lua
Group:		Development/Other
Provides:	lua-devel-static = %{EVRD}
Provides:	lua-static-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
This package contains the static development files for Lua.

%files -n %{staticname}
%{_libdir}/*.a

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches
mkdir -p etc
cp %{SOURCE1} ./etc/
sed -i -e 's/@MAJOR_VERSION@/%{major}/g' ./etc/lua.pc
sed -i -e 's/@FULL_VERSION@/%{version}/g' ./etc/lua.pc

sed -i -e "s|/usr/local|%{_prefix}|g" Makefile
sed -i -e "s|/lib|/%{_lib}|g" Makefile
sed -i -e "s|/usr/local|%{_prefix}|g" src/luaconf.h
sed -i -e "s|/lib|/%{_lib}|g" src/luaconf.h
sed -i -e "s|/man/man1|/share/man/man1|g" Makefile
sed -i -e "s|\$(V)|%{major}|g" src/Makefile
sed -i -e "s|gcc|%{__cc}|g" src/Makefile

%build
%setup_compile_flags
sed -i 's/-lncurses/-lncursesw/g' */Makefile*
%make CC=%{__cc} linux CFLAGS="%{optflags} -fPIC -DLUA_USE_LINUX" MYLDFLAGS="%{ldflags}"

%install
%makeinstall_std INSTALL_TOP=%{buildroot}%{_prefix} INSTALL_LIB=%{buildroot}%{_libdir} INSTALL_MAN=%{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_libdir}/lua/%{major}/
install -d %{buildroot}%{_datadir}/lua/%{major}/

install -m 755 src/liblua.so.%{major}* %{buildroot}%{_libdir}
ln -s liblua.so.%{major} %{buildroot}%{_libdir}/liblua.so

install -d -m 755 %{buildroot}%{_libdir}/pkgconfig/
install -m 644 etc/lua.pc %{buildroot}%{_libdir}/pkgconfig/

# for update-alternatives
mv %{buildroot}%{_bindir}/lua %{buildroot}%{_bindir}/lua%{major}
mv %{buildroot}%{_bindir}/luac %{buildroot}%{_bindir}/luac%{major}

