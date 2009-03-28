# TODO:
#   - there is also support for apache1 in scgi-1.2.tar.gz
#   - there is cgi2scgi.c (CGI script that forwards requests to a SCGI server)
#     which may be compiled and instaled in cgi-bin
#   - python-scgi not tested; apache-mod_scgi works for me
#
# Conditional build:
%bcond_without	apache		# don't build the apache module
#
%define		apxs	/usr/sbin/apxs
Summary:	SCGI - a replacement for the Common Gateway Interface (CGI)
Summary(pl.UTF-8):	SCGI - zastępnik dla Common Gateway Interface (CGI)
Name:		scgi
Version:	1.13
Release:	2
Epoch:		0
License:	CNRI Open Source License/MIT
Group:		Networking/Daemons
Source0:	http://python.ca/scgi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	5cc79e59130ae9efc20388cc8ce906ba
Source1:	apache-mod_%{name}.conf
URL:		http://www.mems-exchange.org/software/scgi/
%if %{with apache}
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
%endif
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

%description -l pl.UTF-8
Protokół SCGI może być używany zamiast protokołu Common Gateway
Interface (CGI). Jest standardem komunikacji miedzy aplikacją a
serwerem HTTP. Jest podobny do FastCGI ale zaprojektowany tak, by być
prostszym do zaimplementowania.

%package -n apache-mod_scgi
Summary:	SCGI - a replacement for the Common Gateway Interface (CGI)
Summary(pl.UTF-8):	SCGI - zastępnik dla Common Gateway Interface (CGI)
Group:		Networking/Daemons
Requires:	apache(modules-api) = %apache_modules_api
%pyrequires_eq  python-modules

%description -n apache-mod_scgi
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

In this package you can find an Apache module named mod_scgi that
implements the client side of the protocol.

%description -n apache-mod_scgi -l pl.UTF-8
Protokół SCGI może być używany zamiast protokołu Common Gateway
Interface (CGI). Jest standardem komunikacji miedzy aplikacją a
serwerem HTTP. Jest podobny do FastCGI ale zaprojektowany tak, by być
prostszym do zaimplementowania.

W tym pakiecie można znaleźć moduł dla serwera Apache nazwany
mod_scgi, który implementuje klienta protokołu SCGI.

%package -n python-scgi
Summary:	A Python package that implements the server side of the SCGI protocol
Summary(pl.UTF-8):	Moduł Pythona implementujący serwer protokołu SCGI
Group:		Libraries/Python
%pyrequires_eq	python-modules

%description -n python-scgi
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

In this package you can find a Python package named scgi that
implements the server side of the protocol.

%description -n python-scgi -l pl.UTF-8
Protokół SCGI może być używany zamiast protokołu Common Gateway
Interface (CGI). Jest standardem komunikacji miedzy aplikacją a
serwerem HTTP. Jest podobny do FastCGI ale zaprojektowany tak, by być
prostszym do zaimplementowania.

W tym pakiecie można znaleźć moduł Pythona implementujący serwer
protokołu SCGI.

%prep
%setup -q

%build
%if %{with apache}
cd apache2
%{apxs} -c mod_scgi.c
cd ..
%endif
env CFLAGS="%{rpmcflags}" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%if %{with apache}
install -d $RPM_BUILD_ROOT%{_libdir}/apache
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d

install apache2/.libs/mod_scgi.so $RPM_BUILD_ROOT%{_libdir}/apache
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/60_mod_scgi.conf
%endif

%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -n apache-mod_scgi
%service httpd restart

%preun -n apache-mod_scgi
if [ "$1" = "0" ]; then
	%service httpd restart
fi

%if %{with apache}
%files -n apache-mod_scgi
%defattr(644,root,root,755)
%doc CHANGES.txt apache2/README.txt LICENSE.txt doc/LICENSE_110.txt
%attr(755,root,root) %{_libdir}/apache/mod_%{name}.so
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/conf.d/*.conf
%endif

%files -n python-%{name}
%defattr(644,root,root,755)
%doc LICENSE.txt doc/LICENSE_110.txt
%dir %{py_sitedir}/scgi
%attr(755,root,root) %{py_sitedir}/scgi/passfd.so
%{py_sitedir}/scgi/*.py[co]
%{py_sitedir}/scgi-*.egg-info
