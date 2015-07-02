Summary:	IPsec-based VPN Solution for Linux
Name:		strongswan
Version:	5.3.2
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
# Source0-md5:	fab014be1477ef4ebf9a765e10f8802c
URL:		http://www.strongswan.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel >= 4.1.5
BuildRequires:  libcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
strongSwan is an OpenSource IPsec solution for the Linux operating
system.

%prep
%setup -q

%build
%{__autoconf}
%{__automake}
%configure \
        --with-capabilities=libcap \
        --disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{_sysconfdir}/ipsec.secrets

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%dir %{_sysconfdir}/ipsec.d
%dir %{_sysconfdir}/ipsec.d/crls
%dir %{_sysconfdir}/ipsec.d/reqs
%dir %{_sysconfdir}/ipsec.d/certs
%dir %{_sysconfdir}/ipsec.d/acerts
%dir %{_sysconfdir}/ipsec.d/aacerts
%dir %{_sysconfdir}/ipsec.d/cacerts
%dir %{_sysconfdir}/ipsec.d/ocspcerts
%dir %attr(700,root,root) %{_sysconfdir}/ipsec.d/private
%dir %{_sysconfdir}/strongswan.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/strongswan.d/*.conf
%dir %{_sysconfdir}/strongswan.d/charon
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/strongswan.d/charon/*.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.secrets
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/strongswan.conf
%{systemdunitdir}/%{name}.service
%attr(755,root,root) %{_bindir}/pki
%dir %{_libdir}/ipsec
%attr(755,root,root) %{_libdir}/ipsec/_copyright
%attr(755,root,root) %{_libdir}/ipsec/_updown
%attr(755,root,root) %{_libdir}/ipsec/charon
%attr(755,root,root) %{_libdir}/ipsec/scepclient
%attr(755,root,root) %{_libdir}/ipsec/starter
%attr(755,root,root) %{_libdir}/ipsec/stroke
%attr(755,root,root) %{_libdir}/ipsec/*.so*
%dir %{_libdir}/ipsec/plugins
%attr(755,root,root) %{_libdir}/ipsec/plugins/libstrongswan-*.so
%attr(755,root,root) %{_sbindir}/ipsec
%{_datadir}/%{name}
%{_mandir}/man[158]/*

