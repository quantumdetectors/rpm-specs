Name:           epics-extensions
Version:        20130514.5
Release:        1%{?dist}
Url:            https://github.com/epics-extensions/extensions
Summary:        EPICS Controls System Extensions
License:        GPL
Source:         https://github.com/epicsdeb/epics-extensions/archive/debian/%{version}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:		epics-base


%description
EPICS Controls System - Extensions
Ported from https://github.com/epicsdeb/epics-extensions

%prep
%setup -q -n epics-extensions-debian-%{version}

%install

%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

echo 'MOTIF_LIB := /usr/lib64' >> configure/os/CONFIG_SITE.linux-x86.linux-x86
echo 'X11_LIB := /usr/lib64' >> configure/os/CONFIG_SITE.linux-x86.linux-x86

mkdir -p %{epics_base}/extensions
cp -r configure %{epics_base}/extensions

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{__libdir}/*

%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
