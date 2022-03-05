%define major 5.3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s
%define alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

# (tpg) enable PGO build
%ifnarch riscv64
%bcond_without pgo
%else
%bcond_with pgo
%endif

Summary:	Powerful, light-weight programming language
Name:		lua
Version:	5.3.6
Release:	1
License:	MIT
Group:		Development/Other
Url:		http://www.lua.org/
Source0:	http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:	lua.pc
Patch0:		lua-5.3.1-dynlib.patch
Patch1:		lua-5.2.0-modules_path.patch
Patch2:		lua52-compat-old-versions.patch
Patch3:		0001-Add-scimark-as-PGO-profiling-workload.patch
Patch4:		0001-Add-option-for-pgo-profiling-test-with-scimark.patch
Provides:	lua%{major} = %{EVRD}
BuildRequires:	pkgconfig(readline)
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
[ -f %{_bindir}/lua%{major} ] || /usr/sbin/update-alternatives --remove lua %{_bindir}/lua%{major}

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
%autosetup -p1

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

%if %{with pgo}
CFLAGS_PGO="%{optflags} -fprofile-instr-generate"
CXXFLAGS_PGO="%{optflags} -fprofile-instr-generate"
FFLAGS_PGO="$CFLAGS_PGO"
FCFLAGS_PGO="$CFLAGS_PGO"
LDFLAGS_PGO="%{ldflags} -fprofile-instr-generate"
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
%make_build CC=%{__cc} linux CFLAGS="${CFLAGS_PGO} -fPIC -DLUA_USE_LINUX" MYLDFLAGS="${LDFLAGS_PGO}"
make test_pgo CC=%{__cc} linux CFLAGS="${CFLAGS_PGO} -fPIC -DLUA_USE_LINUX" MYLDFLAGS="${LDFLAGS_PGO}"
unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d
rm -f *.profile.d
make clean
export CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)"
export CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)"
export LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)"
%endif
%make_build CC=%{__cc} linux CFLAGS="${CFLAGS} -fPIC -DLUA_USE_LINUX" MYLDFLAGS="${LDFLAGS}"

%install
%make_install INSTALL_TOP=%{buildroot}%{_prefix} INSTALL_LIB=%{buildroot}%{_libdir} INSTALL_MAN=%{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_libdir}/lua/%{major}/
install -d %{buildroot}%{_datadir}/lua/%{major}/

install -m 755 src/liblua.so.%{major}* %{buildroot}%{_libdir}
ln -s liblua.so.%{major} %{buildroot}%{_libdir}/liblua.so

install -d -m 755 %{buildroot}%{_libdir}/pkgconfig/
install -m 644 etc/lua.pc %{buildroot}%{_libdir}/pkgconfig/

# for update-alternatives
mv %{buildroot}%{_bindir}/lua %{buildroot}%{_bindir}/lua%{major}
mv %{buildroot}%{_bindir}/luac %{buildroot}%{_bindir}/luac%{major}
