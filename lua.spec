%define major   5.1
%define libname %mklibname lua %{major}
%define alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

Name:		lua
Version:	5.1.2
Release:	%mkrel 1
License:	MIT
Summary:	Lua is a powerful, light-weight programming language
URL:		http://www.lua.org/
Group:		Development/Other
Source0:	http://www.lua.org/ftp/%{name}-%{version}.tar.bz2
Patch0:		lua-5.1-dynlib.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	lua%{major}
# why obsoleting lua5.1 ?
# Obsoletes:	lua5.1
BuildRequires:	libreadline-devel
BuildRequires:	ncurses-devel

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


%package -n %{libname}
Summary:	Lua is a powerful, light-weight programming language
Group:		Development/Other
Obsoletes:	%mklibname %{name} 5

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

This package contains the headers and development files for lua.


%package -n %{libname}-devel
Summary:	Lua is a powerful, light-weight programming language
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	liblua-devel = %{version}-%{release}
Provides:	liblua%{major}-devel = %{version}-%{release}
Provides:	lua-devel = %{version}-%{release}
Provides:	lua%{major}-devel = %{version}-%{release}
Obsoletes: 	%{_lib}lua5-devel < %{version}
Obsoletes:	%{_lib}lua4-devel

%description -n %{libname}-devel
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

This package contains the headers and development files for lua.


%package -n	%{libname}-devel-static
Summary:	Lua is a powerful, light-weight programming language
Group:		Development/Other
Provides:	lua-devel-static = %{version}-%{release}
# Previous package was a -devel only
Requires:	%{libname}-devel = %{version}-%{release}

%description -n	%{libname}-devel-static
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

This package contains the headers and development files for lua.

%prep
%setup -q
%patch0 -p0 -b .dynlib

%build
%make linux CFLAGS="%{optflags} -fPIC -DLUA_USE_LINUX"
sed -i -e "s�/usr/local�%_prefix�" etc/lua.pc

%install
rm -rf %buildroot

%makeinstall_std INSTALL_TOP=%{buildroot}%{_prefix} INSTALL_LIB=%{buildroot}%{_libdir} INSTALL_MAN=%{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_libdir}/lua/%{major}/
install -d %{buildroot}%{_datadir}/lua/%{major}/
install -m 644 test/*.lua %{buildroot}%{_datadir}/lua/%{major}/

install -m 755 src/liblua.so* %{buildroot}%{_libdir}

install -d -m 755 %{buildroot}%{_libdir}/pkgconfig/
install -m 644 etc/lua.pc %{buildroot}%{_libdir}/pkgconfig/

# for update-alternatives
mv %{buildroot}%{_bindir}/lua %{buildroot}%{_bindir}/lua%{major}
mv %{buildroot}%{_bindir}/luac %{buildroot}%{_bindir}/luac%{major}

%clean
rm -rf %{buildroot}

%post
/usr/sbin/update-alternatives --install %{_bindir}/lua lua %{_bindir}/lua%{major} %{alt_priority} --slave %{_bindir}/luac luac %{_bindir}/luac%{major}

%post -n %{libname} -p /sbin/ldconfig

%postun
[[ -f %{_bindir}/lua%{major} ]] || /usr/sbin/update-alternatives --remove lua %{_bindir}/lua%{major}

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/liblua.so.%{major}*

%files -n %{libname}-devel
%defattr (-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/liblua.so

%files -n %{libname}-devel-static
%defattr (-,root,root)
%{_libdir}/*.a

%files
%defattr (-,root,root)
%doc doc/*.html doc/*.gif
%doc COPYRIGHT HISTORY INSTALL README
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/lua
%{_datadir}/lua/%{major}/*.lua
