#
# TODO:
#   - there is also support for apache1 in scgi-1.2.tar.gz
#   - there is cgi2scgi.c (CGI script that forwards requests to a SCGI server)
#     which may be compiled and instaled in cgi-bin
#   - python-scgi not tested; apache-mod_scgi works for me
#
#

%define		pname	scgi
%define		apxs	/usr/sbin/apxs

Summary:	SCGI is a replacement for the Common Gateway Interface (CGI)
Summary(pl):	SCGI jest zast�pnikiem dla Common Gateway Interface (CGI)
Name:		apache-mod_scgi
Version:	1.2
Release:	1
Epoch:		0
License:	CNRI OPEN SOURCE LICENSE
Group:		Networking/Daemons
Source0:	http://www.mems-exchange.org/software/scgi/%{pname}-%{version}.tar.gz
Source1:	%{name}.conf
# Source0-md5:	577f6db7ab95e602378293756d368112
Patch0:		%{pname}-apache2.patch
URL:		http://www.mems-exchange.org/software/scgi/
BuildRequires:	python-devel >= 1:2.3
%pyrequires_eq  python-modules
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

In this package you can find an Apache module named mod_scgi that
implements the client side of the protocol.

%description -l pl
Protok� SCGI mo�e by� u�ywany zamiast protoko�u Common Gateway
Interface (CGI). Jest standardem komunikacji miedzy aplikacj� a
serwerem HTTP. Jest podobny do FastCGI ale zaprojektowany tak, by by�
prostszym do zaimplementowania

W tym pakiecie mo�na znale�� modu� dla serwera Apache nazwany
mod_scgi, kt�ry implementuje klienta protoko�u SCGI.


%package -n python-scgi
Summary:	A Python package that implements the server side of the SCGI protocol
Summary(pl):	Modu� Pythona implementuj�cy serwer protoko�u SCGI
Group:		Libraries/Python

%description -n python-scgi
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

In this package you can find a Python package named scgi that
implements the server side of the protocol.

%description -n python-scgi -l pl
Protok� SCGI mo�e by� u�ywany zamiast protoko�u Common Gateway
Interface (CGI). Jest standardem komunikacji miedzy aplikacj� a
serwerem HTTP. Jest podobny do FastCGI ale zaprojektowany tak, by by�
prostszym do zaimplementowania

W tym pakiecie mo�na znale�� modu� Pythona implementuj�cy serwer
protoko�u SCGI.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%build

cd apache2
%{apxs} -c mod_scgi.c
cd ..

env CFLAGS="%{rpmcflags}" python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
# create directories
install -d $RPM_BUILD_ROOT/%{_libdir}/apache
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf
install apache2/.libs/mod_scgi.so $RPM_BUILD_ROOT/%{_libdir}/apache
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/60_mod_scgi.conf

python -- setup.py install \
        --root=$RPM_BUILD_ROOT \
        --optimize=2

find $RPM_BUILD_ROOT%{py_sitedir} -name \*.py | xargs rm -f
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}/%{pname}
find $RPM_BUILD_ROOT%{py_sitedir} -name \*.py[co] -exec mv \{\} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{pname} \;


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES apache2/README LICENSE.txt
%attr(755,root,root) %{_libdir}/apache/mod_%{pname}.so
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*.conf

%files -n python-%{pname}
%doc LICENSE.txt
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{pname}
%{py_sitedir}/%{pname}
