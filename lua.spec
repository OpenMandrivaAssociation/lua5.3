%define major 5.1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s
%define alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

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

%package -n %{develname}
Summary:	Headers and development files for Lua
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Provides:	liblua%{major}-devel = %{version}-%{release}
Provides:	lua-devel = %{version}-%{release}
Provides:	lua%{major}-devel = %{version}-%{release}
Obsoletes: 	%{_lib}lua5-devel < %{version}

%description -n %{develname}
This package contains the headers and development files for Lua.

%package -n	%{staticname}
Summary:	Static development files for Lua
Group:		Development/Other
Provides:	lua-devel-static = %{version}-%{release}
Provides:	lua-static-devel = %{version}-%{release}
Requires:	%{develname} = %{version}-%{release}

%description -n	%{staticname}
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
%make linux CFLAGS="%{optflags} -fPIC -DLUA_USE_LINUX" CC="%__cc" LD="%__ld"
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

%files -n %{develname}
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/liblua.so

%files -n %{staticname}
%{_libdir}/*.a


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 5.1.4-10mdv2011.0
+ Revision: 666103
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.4-9mdv2011.0
+ Revision: 606426
- rebuild

* Mon Mar 15 2010 RÃ©my Clouard <shikamaru@mandriva.org> 5.1.4-8mdv2010.1
+ Revision: 520626
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 5.1.4-7mdv2010.0
+ Revision: 426015
- rebuild

* Wed Feb 25 2009 Thierry Vignaud <tv@mandriva.org> 5.1.4-6mdv2009.1
+ Revision: 344654
- rebuild for new libreadline in order to unbreak cooker

* Sat Jan 24 2009 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 5.1.4-5mdv2009.1
+ Revision: 333184
- previous patch was broken, remove libdir completely since library resides in
  standard location and doesn't need to get passed to linker anyways..

* Mon Dec 29 2008 JÃ©rÃ´me Soyer <saispo@mandriva.org> 5.1.4-4mdv2009.1
+ Revision: 320762
- Bump Release
- Add patch for fixing 64bit issue

  + Per Ã˜yvind Karlsen <peroyvind@mandriva.org>
    - remove -L{libdir} from lua.pc so that -L/usr/lib won't be passed to ldflags
      (very annoying on x86_64 which will give a lot of warnings about skipping
      32 bit libraries under /ur/lib..)

* Fri Sep 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 5.1.4-2mdv2009.0
+ Revision: 285916
- ensure devel package requires main package

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 5.1.4-1mdv2009.0
+ Revision: 283044
- New version
- drop P1 (merged upstream)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 5.1.3-5mdv2009.0
+ Revision: 265034
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jun 05 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.1.3-4mdv2009.0
+ Revision: 215155
- Patch1: add upstream patch

* Thu Jun 05 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.1.3-3mdv2009.0
+ Revision: 215152
- rebuild for new gcc-4.3

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 5.1.3-2mdv2008.1
+ Revision: 170970
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Mon Feb 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.1.3-1mdv2008.1
+ Revision: 165019
- fix summaries and descriptions
- fix lua.pc
- new version

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 5.1.2-6mdv2008.1
+ Revision: 152880
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Aug 05 2007 Anssi Hannula <anssi@mandriva.org> 5.1.2-4mdv2008.0
+ Revision: 59119
- make liblua.so a proper devel symlink instead of a copy

* Mon Jul 16 2007 Funda Wang <fwang@mandriva.org> 5.1.2-3mdv2008.0
+ Revision: 52568
- Obsoletes old static devel name

* Wed Jun 20 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 5.1.2-2mdv2008.0
+ Revision: 41814
- new devel library policy
- spec file clean

* Sat May 19 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 5.1.2-1mdv2008.0
+ Revision: 28430
- new version
- drop P1
- make use of %%{major}
- spec file clean


* Tue Mar 06 2007 Olivier Thauvin <nanardon@mandriva.org> 5.1.1-9mdv2007.0
+ Revision: 133768
- obsoletes liblua5 to avoid files conflicts

* Mon Nov 13 2006 Pascal Terjan <pterjan@mandriva.org> 5.1.1-8mdv2007.0
+ Revision: 83555
- ship lua.pc

* Fri Aug 25 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 5.1.1-7mdv2007.0
+ Revision: 57833
- Increase release
- Fix group

  + GaÃ«tan Lehmann <glehmann@mandriva.org>
    - add alternative for lua and luac
    - small spec cleanup

* Sun Aug 20 2006 Olivier Thauvin <nanardon@mandriva.org> 5.1.1-5mdv2007.0
+ Revision: 56856
- replace major from 5 to 5.1 for lua5.0 cohabitation

* Sat Aug 19 2006 Thierry Vignaud <tvignaud@mandriva.com> 5.1.1-4mdv2007.0
+ Revision: 56793
- fix build on x86_64

* Fri Aug 18 2006 Olivier Thauvin <nanardon@mandriva.org> 5.1.1-3mdv2007.0
+ Revision: 56554
- reprovide liblua and its -devel
- add patch to enable .so building

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - fix buildrequires

* Sun Aug 13 2006 Olivier Thauvin <nanardon@mandriva.org> 5.1.1-2mdv2007.0
+ Revision: 55708
- release package
- provide also liblua-devel
- handle the name change -devel to -devel-static

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - fix buildrequires

* Fri Aug 11 2006 Helio Chissini de Castro <helio@mandriva.com> 5.1.1-1mdv2007.0
+ Revision: 55509
- New upstream version 5.1.1
- Lua now is just static, as decided by developers. This package will solve the
  conflicts with old lua on main and new wrong package on contrib
- import lua-5.0.2-9mdk

* Fri Oct 07 2005 Götz Waschk <waschk@mandriva.org> 5.0.2-9mdk
- fix packaging bugs 16461 and 19006

* Mon Oct 03 2005 Pascal Terjan <pterjan@mandriva.org> 5.0.2-8mdk
- add SONAME to the libs so that other package don't want -devel (P3)

* Sat Jul 09 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0.2-7mdk
- fix provides for x86_64

* Wed Apr 13 2005 Olivier Thauvin <nanardon@mandrake.org> 5.0.2-6mdk
- avoid postun exit 1 (thanks Eskild Hustvedt && Daniel Le Berre)

* Tue Apr 12 2005 Olivier Thauvin <nanardon@mandrake.org> 5.0.2-5mdk
- add -fPIC on x86_64
- fix lib location

* Sat Mar 12 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.2-4mdk
- fix update-alternatives (#14460)

* Thu Mar 10 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 5.0.2-3mdk
- fix ownership of files (fixes #14458)
- fix libuse- cosmetics
- compile with optimizations

* Mon Aug 30 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0.2-2mdk
- fix .so links

* Wed May 05 2004 Lenny Cartier <lenny@mandrakesoft.com> 5.0.2-1mdk
- from Andre Nathan <andre@digirati.com.br>

