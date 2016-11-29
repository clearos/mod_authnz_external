Summary: An Apache module used for authentication
Name: mod_authnz_external
Version: 3.3.2
Release: 3%{?dist}
License: ASL 1.0
Group: System Environment/Libraries
URL: http://code.google.com/p/mod-auth-external/
Source: http://mod-auth-external.googlecode.com/files/%{name}-%{version}.tar.gz
Source1: 10-authnz-external-webconfig.conf
Requires: pwauth, httpd-mmn = %(cat %{_includedir}/httpd/.mmn 2> /dev/null || echo missing)
BuildRequires: httpd-devel

%description
Mod_Auth_External can be used to quickly construct secure, reliable
authentication systems.  It can also be mis-used to quickly open gaping
holes in your security.  Read the documentation, and use with extreme
caution.

%global modulesdir %{_libdir}/httpd/modules
%global confdir %{_sysconfdir}/httpd/conf

%package webconfig
Summary: A Webconfig Apache module used for authentication
Group: System Environment/Libraries
Requires: pwauth-webconfig, webconfig-httpd-mmn = %(cat %{_includedir}/webconfig-httpd/.mmn 2> /dev/null || echo missing)
BuildRequires: webconfig-httpd-devel

%description webconfig
Mod_Auth_External for webconfig

%prep
%setup -q

%build
/usr/clearos/sandbox/usr/bin/apxs -c -I . %{name}.c
mkdir webconfig
mv mod_authnz_external.o mod_authnz_external.lo mod_authnz_external.slo mod_authnz_external.la webconfig/
mv .libs webconfig/

apxs -c -I . %{name}.c


%install
mkdir -p %{buildroot}%{modulesdir} %{buildroot}%{confdir}.d
apxs -i -S LIBEXECDIR=%{buildroot}%{modulesdir} -n %{name} %{name}.la
install -p -m 644 -t %{buildroot}%{confdir}.d/ authnz_external.conf

# in case we're on a 64-bit machine, otherwise a no-op
sed -i \
	-e 's@/usr/lib/@%{_libdir}/@' \
	%{buildroot}%{confdir}.d/authnz_external.conf

mkdir -p %{buildroot}/usr/clearos/sandbox%{modulesdir} %{buildroot}/usr/clearos/sandbox%{confdir}.d
apxs -i -S LIBEXECDIR=%{buildroot}/usr/clearos/sandbox%{modulesdir} -n %{name} webconfig/%{name}.la
install -d %{buildroot}/usr/clearos/sandbox%{confdir}.modules.d
install -m0644 %{SOURCE1} %{buildroot}/usr/clearos/sandbox%{confdir}.modules.d/10-authnz-external.conf

%files webconfig
/usr/clearos/sandbox%{modulesdir}/%{name}.so
/usr/clearos/sandbox%{confdir}.modules.d/10-authnz-external.conf

%files
%{modulesdir}/%{name}.so
%config(noreplace) %lang(en) %{confdir}.d/authnz_external.conf
%doc AUTHENTICATORS CHANGES README TODO UPGRADE
