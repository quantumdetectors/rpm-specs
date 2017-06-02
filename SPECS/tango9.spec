Name:           tango
Version:        9.2.5a
Release:        1%{?dist}
Url:            http://tango-controls.org
Summary:        Tango Controls System
License:        GPL
Source:         tango-9.2.5a.tar.gz
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

%global _python_bytecompile_errors_terminate_build 0
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{_prefix} --with-mysqlclient-lib=/usr/lib64/mysql --libdir=%{_libdir}
%{__make}

%install
export QA_RPATHS=$[ 0x0001 ]
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
#%{_prefix}/lib/*
%{_libdir}/*
%{_datadir}/*
%{_includedir}/*

%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
