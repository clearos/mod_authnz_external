Summary: An Apache module used for authentication
Name: mod_authnz_external
Version: 3.3.2
Release: 3%{?dist}
License: ASL 1.0
Group: System Environment/Libraries
URL: http://code.google.com/p/mod-auth-external/
Source: http://mod-auth-external.googlecode.com/files/%{name}-%{version}.tar.gz
Requires: pwauth, httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel

%description
Mod_Auth_External can be used to quickly construct secure, reliable
authentication systems.  It can also be mis-used to quickly open gaping
holes in your security.  Read the documentation, and use with extreme
caution.

%global modulesdir %{_libdir}/httpd/modules
%global confdir %{_sysconfdir}/httpd/conf


%prep
%setup -q

%build
apxs -c -I . %{name}.c


%install
mkdir -p %{buildroot}%{modulesdir} %{buildroot}%{confdir}.d
apxs -i -S LIBEXECDIR=%{buildroot}%{modulesdir} -n %{name} %{name}.la
install -p -m 644 -t %{buildroot}%{confdir}.d/ authnz_external.conf

# in case we're on a 64-bit machine, otherwise a no-op
sed -i \
	-e 's@/usr/lib/@%{_libdir}/@' \
	%{buildroot}%{confdir}.d/authnz_external.conf


%files
%{modulesdir}/%{name}.so
%config(noreplace) %lang(en) %{confdir}.d/authnz_external.conf
%doc AUTHENTICATORS CHANGES README TODO UPGRADE
