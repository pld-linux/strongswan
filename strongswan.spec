#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	-
Summary(pl.UTF-8):	-
Name:		strongswan
Version:	4.5.0
Release:	0.1
License:	- (enter GPL/GPL v2/GPL v3/LGPL/BSD/BSD-like/other license name here)
Group:		Applications
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
# Source0-md5:	cfbd6efef87830a2e7cc4175bde7ac84
#Source1:	-
# Source1-md5:	-
#Patch0:		%{name}-DESTDIR.patch
URL:		http://www.strongswan.org/
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%endif
#BuildRequires:	-
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Provides:	group(foo)
#Provides:	user(foo)
#Obsoletes:	-
#Conflicts:	-
#BuildArch:	noarch
#ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%define         skip_post_check_so	libcharon.so.0.0.0 libhydra.so.0.0.0

%description

%description -l pl.UTF-8

%package subpackage
Summary:	-
Summary(pl.UTF-8):	-
Group:		-

%description subpackage

%description subpackage -l pl.UTF-8

%package libs
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries

%description libs

%description libs -l pl.UTF-8

%package devel
Summary:	Header files for ... library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ...
Group:		Development/Libraries
# if base package contains shared library for which these headers are
#Requires:	%{name} = %{version}-%{release}
# if -libs package contains shared library for which these headers are
#Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for ... library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ....

%package static
Summary:	Static ... library
Summary(pl.UTF-8):	Statyczna biblioteka ...
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ... library.

%description static -l pl.UTF-8
Statyczna biblioteka ....

%prep
%setup -q
#%setup -q -c -T
#%setup -q -n %{name}
#%setup -q -n %{name}-%{version}.orig -a 1
#%patch0 -p1

# undos the source
#find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

# remove CVS control files
#find -name CVS -print0 | xargs -0 rm -rf

# you'll need this if you cp -a complete dir in source
# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__intltoolize}
#%%{__gettextize}
#%%{__libtoolize}
#{__aclocal}
%{__autoconf}
#%%{__autoheader}
%{__automake}
# if not running libtool or automake, but config.sub is too old:
#cp -f /usr/share/automake/config.sub .
%configure \
	--enable-cisco-quirks
%{__make}

#%{__make} \
#	CFLAGS="%{rpmcflags}" \
#	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
%if %{with initscript}
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
%endif
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
#groupadd -g xxx %{name}
#useradd -u xxx -d /var/lib/%{name} -g %{name} -c "XXX User" %{name}

%post

%preun

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%if %{with ldconfig}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%if %{with initscript}
%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README TODO
%{_sysconfdir}/ipsec.conf
%{_sysconfdir}/strongswan.conf
%attr(755,root,root) %{_libdir}/ipsec
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/*.so.0
%attr(755,root,root) %{_sbindir}/ipsec
%{_mandir}/man[358]/*


%if 0
# if _sysconfdir != /etc:
#%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%endif

# initscript and its config
%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif

#%{_examplesdir}/%{name}-%{version}

%if %{with subpackage}
%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%endif
