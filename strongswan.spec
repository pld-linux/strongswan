# TODO:
#	- init script
#	- kill skip_post_check_so
#	- enable more configure options
Summary:	IPsec-based VPN Solution for Linux
Name:		strongswan
Version:	4.5.2
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
# Source0-md5:	ac33b8f849a274127f84df0838cae953
URL:		http://www.strongswan.org/
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%endif
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel >= 4.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%define         skip_post_check_so	libcharon.so.0.0.0 libhydra.so.0.0.0

%description
strongSwan is an OpenSource IPsec solution for the Linux operating
system.

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

%build
%{__autoconf}
%{__automake}
%configure \
	--enable-cisco-quirks
%{__make}

#%{__make} \
#	CFLAGS="%{rpmcflags}" \
#	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
%if %{with initscript}
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

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
