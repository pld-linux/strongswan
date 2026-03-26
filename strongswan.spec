%bcond_without	python3
%bcond_without	perl
%bcond_with	tests
Summary:	IPsec-based VPN Solution for Linux
Name:		strongswan
Version:	6.0.5
Release:	3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
# Source0-md5:	7049111627010dc02293970c82e43d28
Source1:	tmpfiles-%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-vici-socket-path.patch
URL:		http://www.strongswan.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	gettext-devel
BuildRequires:	gmp-devel >= 4.1.5
BuildRequires:	iptables-devel
BuildRequires:	json-c-devel
BuildRequires:	libcap-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	sqlite-devel
BuildRequires:	systemd-devel
BuildRequires:	tpm2-tss-devel
%if %{with python3}
BuildRequires:	python3-build
BuildRequires:	python3-daemon
BuildRequires:	python3-devel
BuildRequires:	python3-pytest
BuildRequires:	python3-setuptools
%endif
%if %{with perl}
BuildRequires:	perl-devel
%endif
BuildRequires:	NetworkManager-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	rc-scripts >= 0.4.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
strongSwan is an OpenSource IPsec solution for the Linux operating
system.

%package libipsec
Summary:	Strongswan's libipsec backend

%description libipsec
The kernel-libipsec plugin provides an IPsec backend that works
entirely in userland, using TUN devices and its own IPsec
implementation libipsec.

%package charon-nm
Summary:	NetworkManager plugin for Strongswan
Requires:	dbus

%description charon-nm
NetworkManager plugin integrates a subset of Strongswan capabilities
to NetworkManager.

%package sqlite
Summary:	SQLite support for strongSwan
Requires:	strongswan = %{version}-%{release}

%description sqlite
The sqlite plugin adds an SQLite database backend to strongSwan.

%package tnc-imcvs
Summary:	Trusted network connect (TNC)'s IMC/IMV functionality
Requires:	strongswan = %{version}-%{release}
Requires:	strongswan-sqlite = %{version}-%{release}

%description tnc-imcvs
This package provides Trusted Network Connect's (TNC) architecture
support. It includes support for TNC client and server (IF-TNCCS), IMC
and IMV message exchange (IF-M), interface between IMC/IMV and TNC
client/server (IF-IMC and IF-IMV). It also includes PTS based IMC/IMV
for TPM based remote attestation, SWID IMC/IMV, and OS IMC/IMV. It's
IMC/IMV dynamic libraries modules can be used by any third party TNC
Client/Server implementation possessing a standard IF-IMC/IMV
interface. In addition, it implements PT-TLS to support TNC over TLS.

%package -n python3-vici
Summary:	Strongswan Versatile IKE Configuration Interface python bindings
BuildArch:	noarch

%description -n python3-vici
VICI is an attempt to improve the situation for system integrators by
providing a stable IPC interface, allowing external tools to query,
configure and control the IKE daemon.

The Versatile IKE Configuration Interface (VICI) python bindings
provides module for Strongswan runtime configuration from python
applications.

%package -n perl-vici
Summary:	Strongswan Versatile IKE Configuration Interface perl bindings
BuildArch:	noarch

%description -n perl-vici
VICI is an attempt to improve the situation for system integrators by
providing a stable IPC interface, allowing external tools to query,
configure and control the IKE daemon.

The Versatile IKE Configuration Interface (VICI) perl bindings
provides module for Strongswan runtime configuration from perl
applications.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--with-ipsec-script=strongswan \
	--sysconfdir=%{_sysconfdir}/strongswan \
	--with-ipsecdir=%{_libexecdir}/strongswan \
	--bindir=%{_libexecdir}/strongswan \
	--with-ipseclibdir=%{_libdir}/strongswan \
	--with-piddir=%{_rundir}/strongswan \
	--with-nm-ca-dir=%{_sysconfdir}/strongswan/ipsec.d/cacerts/ \
	--enable-bypass-lan \
	--enable-tss-tss2 \
	--enable-nm \
	--enable-systemd \
	--enable-openssl \
	--enable-unity \
	--enable-ctr \
	--enable-ccm \
	--enable-gcm \
	--enable-chapoly \
	--enable-md4 \
	--enable-ml \
	--enable-gcrypt \
	--enable-xauth-eap \
	--enable-xauth-pam \
	--enable-xauth-noauth \
	--enable-eap-identity \
	--enable-eap-md5 \
	--enable-eap-gtc \
	--enable-eap-tls \
	--enable-eap-ttls \
	--enable-eap-peap \
	--enable-eap-mschapv2 \
	--enable-eap-tnc \
	--enable-eap-sim \
	--enable-eap-sim-file \
	--enable-eap-aka \
	--enable-eap-aka-3gpp \
	--enable-eap-aka-3gpp2 \
	--enable-eap-dynamic \
	--enable-eap-radius \
	--enable-ext-auth \
	--enable-ipseckey \
	--enable-pkcs11 \
	--enable-tpm \
	--enable-farp \
	--enable-dhcp \
	--enable-ha \
	--enable-led \
	--enable-sql \
	--enable-sqlite \
	--enable-tnc-ifmap \
	--enable-tnc-pdp \
	--enable-tnc-imc \
	--enable-tnc-imv \
	--enable-tnccs-20 \
	--enable-tnccs-11 \
	--enable-tnccs-dynamic \
	--enable-imc-test \
	--enable-imv-test \
	--enable-imc-scanner \
	--enable-imv-scanner  \
	--enable-imc-attestation \
	--enable-imv-attestation \
	--enable-imv-os \
	--enable-imc-os \
	--enable-imc-swima \
	--enable-imv-swima \
	--enable-imc-hcd \
	--enable-imv-hcd \
	--enable-curl \
	--enable-cmd \
	--enable-acert \
	--enable-vici \
	--enable-swanctl \
	--enable-duplicheck \
	--enable-selinux \
	--enable-stroke \
%ifarch x86_64 %{ix86}
	--enable-aesni \
%endif
%if %{with perl}
	--enable-perl-cpan \
%endif
%if %{with tests}
	--enable-test-vectors \
%endif
	--enable-kernel-libipsec \
	--with-capabilities=libcap \
	CPPFLAGS="-DSTARTER_ALLOW_NON_ROOT"

# disable certain plugins in the daemon configuration by default
for p in bypass-lan; do
	echo -e "\ncharon.plugins.${p}.load := no" >> conf/plugins/${p}.opt
done

# ensure manual page is regenerated with local configuration
rm src/ipsec/_ipsec.8

%{__make}

%if %{with python3}
cd src/libcharon/plugins/vici/python
sed -e 's,@EGG_VERSION@,%{version},' setup.py.in > setup.py
%py3_build
cd ../../../../..
%endif

%if %{with perl}
olddir=$(pwd)
cd src/libcharon/plugins/vici/perl/Vici-Session
%{__perl} Makefile.PL \
		INSTALLDIRS=vendor
%{__make}
cd $olddir
%endif

%if %{with tests}
export TESTS_VERBOSITY=1
# protect against hanging tests
timeout 600 %{__make} check

%if %{with python3}
cd src/libcharon/plugins/vici/python
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest test
cd ../../../../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python3}
cd src/libcharon/plugins/vici/python
%py3_install
cd ../../../../..
%endif

%if %{with perl}
%{__make} -C src/libcharon/plugins/vici/perl/Vici-Session install \
	DESTDIR=$RPM_BUILD_ROOT
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Vici/Session/.packlist
%endif

# prefix man pages
for i in $RPM_BUILD_ROOT%{_mandir}/*/*; do
    if echo "$i" | grep -vq '/strongswan[^\/]*$'; then
        mv "$i" "`echo "$i" | sed -re 's|/([^/]+)$|/strongswan_\1|'`"
    fi
done

install -d $RPM_BUILD_ROOT%{_rundir}/strongswan
install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/strongswan.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/strongswan-starter.conf

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm $RPM_BUILD_ROOT%{_libdir}/%{name}/*.so
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.la
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/imcvs/*.la

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ipsec.secrets
echo '# EAP-SIM triplets: IMSI,RAND,SRES,Kc' > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ipsec.d/triplets.dat

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "strongSwan IPsec"
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/strongswan
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/ipsec.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/ipsec.secrets
%dir %{_sysconfdir}/%{name}/ipsec.d
%dir %{_sysconfdir}/%{name}/ipsec.d/aacerts
%dir %{_sysconfdir}/%{name}/ipsec.d/acerts
%dir %{_sysconfdir}/%{name}/ipsec.d/cacerts
%dir %{_sysconfdir}/%{name}/ipsec.d/certs
%dir %{_sysconfdir}/%{name}/ipsec.d/crls
%dir %{_sysconfdir}/%{name}/ipsec.d/ocspcerts
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/ipsec.d/private
%dir %{_sysconfdir}/%{name}/ipsec.d/reqs
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/ipsec.d/triplets.dat
%dir %{_sysconfdir}/%{name}/%{name}.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.d/*.conf
%exclude %{_sysconfdir}/%{name}/%{name}.d/charon-nm.conf
%dir %{_sysconfdir}/%{name}/%{name}.d/charon
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.d/charon/*.conf
%dir %{_sysconfdir}/%{name}/%{name}.d/charon-cmd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.d/charon-cmd/*.conf
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/swanctl
%dir %{_sysconfdir}/%{name}/swanctl/conf.d
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/swanctl/ecdsa
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/swanctl/pkcs12
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/swanctl/pkcs8
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/swanctl/private
%dir %{_sysconfdir}/%{name}/swanctl/pubkey
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/swanctl/rsa
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/swanctl/swanctl.conf
%dir %{_sysconfdir}/%{name}/swanctl/x509
%dir %{_sysconfdir}/%{name}/swanctl/x509aa
%dir %{_sysconfdir}/%{name}/swanctl/x509ac
%dir %{_sysconfdir}/%{name}/swanctl/x509ca
%dir %{_sysconfdir}/%{name}/swanctl/x509crl
%dir %{_sysconfdir}/%{name}/swanctl/x509ocsp
%dir %{_libdir}/strongswan
%exclude %{_libdir}/strongswan/imcvs
%dir %{_libdir}/strongswan/plugins
%dir %{_libexecdir}/strongswan
%{systemdunitdir}/strongswan.service
%{systemdunitdir}/strongswan-starter.service
%attr(755,root,root) %{_sbindir}/charon-cmd
%attr(755,root,root) %{_sbindir}/charon-systemd
%attr(755,root,root) %{_sbindir}/strongswan
%attr(755,root,root) %{_sbindir}/swanctl
%{_libdir}/strongswan/*.so.*
%{_libdir}/strongswan/plugins/*.so
%exclude %{_libdir}/strongswan/libimcv.so.*
%exclude %{_libdir}/strongswan/libtnccs.so.*
%exclude %{_libdir}/strongswan/libipsec.so.*
%exclude %{_libdir}/strongswan/plugins/libstrongswan-sqlite.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-*tnc*.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-kernel-libipsec.so
%attr(755,root,root) %{_libexecdir}/strongswan/*
%exclude %{_libexecdir}/strongswan/attest
%exclude %{_libexecdir}/strongswan/pt-tls-client
%exclude %{_libexecdir}/strongswan/charon-nm
%exclude %dir %{_datadir}/strongswan/swidtag
%{_mandir}/man?/*.*
%{_datadir}/strongswan/templates/config
%{_datadir}/strongswan/templates/database
%dir %attr(700,root,root) %{_rundir}/strongswan
%{systemdtmpfilesdir}/strongswan.conf
%{systemdtmpfilesdir}/strongswan-starter.conf

%files sqlite
%defattr(644,root,root,755)
%{_libdir}/strongswan/plugins/libstrongswan-sqlite.so

%files tnc-imcvs
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/sw-collector
%attr(755,root,root) %{_sbindir}/sec-updater
%dir %{_libdir}/strongswan/imcvs
%{_libdir}/strongswan/imcvs/*.so
%{_libdir}/strongswan/libimcv.so.*
%{_libdir}/strongswan/libtnccs.so.*
%{_libdir}/strongswan/plugins/libstrongswan-*tnc*.so
%attr(755,root,root) %{_libexecdir}/strongswan/attest
%attr(755,root,root) %{_libexecdir}/strongswan/pt-tls-client
%dir %{_datadir}/strongswan/swidtag
%{_datadir}/strongswan/swidtag/*.swidtag

%files libipsec
%defattr(644,root,root,755)
%{_libdir}/strongswan/libipsec.so.*
%{_libdir}/strongswan/plugins/libstrongswan-kernel-libipsec.so

%files charon-nm
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}/%{name}.d/charon-nm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.d/charon-nm.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.d/charon-nm/*.conf
%{_datadir}/dbus-1/system.d/nm-strongswan-service.conf
%attr(755,root,root) %{_libexecdir}/strongswan/charon-nm

%if %{with python3}
%files -n python3-vici
%defattr(644,root,root,755)
%doc src/libcharon/plugins/vici/python/README.rst
%{py3_sitescriptdir}/vici
%{py3_sitescriptdir}/vici-%{version}*.egg-info
%endif

%if %{with perl}
%files -n perl-vici
%defattr(644,root,root,755)
%{perl_vendorlib}/Vici
%endif
