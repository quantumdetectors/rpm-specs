Name:           tango
Version:        9.2.5a
Release:        1%{?dist}
Url:            http://tango-controls.org
Summary:        Tango Controls System
License:        GPL
Source:         https://downloads.sourceforge.net/project/tango-cs/tango-%{version}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-root
Requires:       zeromq
Requires:       omniORB
Requires:       mariadb-server
Requires:       mysql-devel
Requires:       jre
BuildRequires:  zeromq-devel
BuildRequires:  omniORB-devel
BuildRequires:  mysql-devel

%description
Tango Controls System


%package devel
Summary: Tango Controls System development files
Provides: tango-devel

%description devel
This package contains necessary header files for Tango development.


%global _python_bytecompile_errors_terminate_build 0
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{_prefix} --with-mysqlclient-lib=/usr/lib64/mysql --libdir=%{_libdir} --with-mysql-admin=%{_mysql_user} --with-mysql-admin-passwd=%{_mysql_password}
%{__make}

%install
%{__make} DESTDIR=$RPM_BUILD_ROOT install

chmod 755 %{buildroot}%{_datadir}/tango/db/create_db.sh

chrpath --delete %{buildroot}%{_libdir}/*.so
chrpath --delete %{buildroot}%{_bindir}/tango_admin
chrpath --delete %{buildroot}%{_bindir}/Starter
chrpath --delete %{buildroot}%{_bindir}/TangoTest
chrpath --delete %{buildroot}%{_bindir}/DataBaseds
chrpath --delete %{buildroot}%{_bindir}/TangoAccessControl

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post
cd %{_datadir}/tango/db
./create_db.sh
tango start

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*

%changelog
* Thu Jun 09 2017 Stu<stu@quantumdetectors.com>
– Create db, split into devel package, pass credentials to rpmbuild, remove rpaths
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
