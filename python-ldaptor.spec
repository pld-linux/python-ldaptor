#
# Conditional build:
%bcond_without	doc		# build the documentation
#
%define		githash		29a06fa
Summary:	Python LDAP client library
Name:		python-ldaptor
Version:	0.0.44
Release:	0.git%{githash}.2
License:	LGPLv2
Group:		Libraries/Python
Source0:	https://codeload.github.com/antong/ldaptor/tar.gz/%{githash}?/python-ldaptor-%{version}.%{githash}.tar.gz
# Source0-md5:	eace8cf1dc3f7061051b019444d57ca6
Source1:	global.cfg
Patch0:		%{name}-remove-webui.patch
Patch1:		%{name}-doc-paths.patch
Patch2:		deprecated-exception.patch
Patch3:		module-typo.patch
Patch4:		sasl.patch
Patch5:		starttls-fix.patch
Patch6:		unicode.patch
Patch7:		abandon.patch
URL:		https://github.com/antong/ldaptor
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with doc}
BuildRequires:	dia
BuildRequires:	docbook-slides
BuildRequires:	docbook-style-xsl
BuildRequires:	epydoc
BuildRequires:	libxslt
BuildRequires:	python-docutils
BuildRequires:	source-highlight
%endif
Requires:	Zope-Interface
Requires:	python-Crypto
Requires:	python-TwistedCore
Requires:	python-TwistedCore-ssl
Requires:	python-TwistedMail
Requires:	python-TwistedNames
Requires:	python-modules
Requires:	python-pyOpenSSL
Requires:	python-pyparsing
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ldaptor is LDAP library written in pure Python. The library implements
LDAP client logic, separately-accessible LDAP and BER protocol message
generation and parsing, ASCII format LDAP filter generation and
parsing, LDIF format data generation, and Samba password changing
logic.

%package doc
Summary:	Documentation for python-ldaptor package
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description doc
The package contains documentation for python-ldaptor package.

%package tools
Summary:	Ldaptor command line utilities
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description tools
The package contains command line utilities build upon python-ldaptor
library.

%prep
%setup -q -n ldaptor-%{githash}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# remove deprecated web interface
%{__rm} -r ldaptor/{apps,weave.*,test/{web,test_webui.*}}

%{__sed} -i -e 's|/usr/share/xml|/usr/share/sgml|g' doc/Makefile doc/slides-driver.xsl

%build
%py_build

%if %{with doc}
%{__make} -C doc
epydoc -o doc/api --name Ldaptor ldaptor --exclude 'ldaptor\.test\.' --simple-term
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ldaptor

%py_install \
	--root $RPM_BUILD_ROOT

# library system-wide configuration and schema
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ldaptor
install -p ldaptor.schema $RPM_BUILD_ROOT%{_sysconfdir}/ldaptor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO README.md
%dir %{_sysconfdir}/ldaptor
%config(noreplace) %{_sysconfdir}/ldaptor/global.cfg
%{_sysconfdir}/ldaptor/ldaptor.schema
%{py_sitescriptdir}/ldaptor-0.0.0-py2.7.egg-info
%{py_sitescriptdir}/ldaptor

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/addressbook-slides
%doc doc/api
%doc doc/examples
%doc doc/ldap-intro
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldaptor-*
