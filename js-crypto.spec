Summary:	JavaScript implementations of standard and secure cryptographic algorithms
Name:		js-crypto
Version:	2.3.0
Release:	1
License:	New BSD License
Group:		Applications/WWW
Source0:	https://crypto-js.googlecode.com/files/Crypto-JS%20v%{version}.zip
# Source0-md5:	c2d35c3611fbb156103590b50eba9d70
URL:		https://code.google.com/p/crypto-js/
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Crypto-JS is a growing collection of standard and secure cryptographic
algorithms implemented in JavaScript using best practices and
patterns. They are fast, and they have a consistent and simple
interface.

%prep
%setup -qc
%undos -f js

# Apache1/Apache2 config
cat > apache.conf <<'EOF'
Alias /js/crypto/ %{_appdir}/
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# Lighttpd config
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/js/crypto/" => "%{_appdir}/",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a . $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*/
