Name:           epics-calc
Version:        3.6.1
%define         subversion 2
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/asyn
Summary:        EPICS Calc Module
License:        GPL
Source:         https://github.com/epicsdeb/calc/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base-devel
BuildRequires:  epics-seq-devel
BuildRequires:  epics-sscan-devel
Requires:       epics-base
Requires:       epics-seq
Requires:       epics-sscan
AutoReqProv:    no


%description
EPICS Controls System - Calc Package
Ported from https://github.com/epicsdeb/calc


%package devel
Summary: EPICS Calc development files
Requires: epics-calc
Provides: epics-calc-devel
Requires: epics-base-devel
Requires: epics-seq-devel
Requires: epics-sscan-devel

%description devel
This package contains necessary header files and static libraries for the EPICS Calc module.


%prep
%setup -q -n calc-debian-%{version}-%{subversion}
git apply debian/patches/0001-update-configure-RELEASE.patch
%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

install -d %{epics_base}/lib/%{epics_host_arch}

install -d %{buildroot}%{_libdir}/

mv dbd %{epics_base}/
mv include %{epics_base}/

install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/

chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.a
chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.so

chrpath --delete %{epics_base}/lib/%{epics_host_arch}/*.so

cd %{epics_base}/lib/%{epics_host_arch}
ln -sr * ../../../../..%{_libdir}/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{__libdir}/*
%{_libdir}/*
%exclude %{__libdir}/epics/include/*
%exclude %{__libdir}/epics/lib/%{epics_host_arch}/*.a
%exclude %{_libdir}/*.a


%files devel
%{__libdir}/epics/include/*
%{__libdir}/epics/lib/%{epics_host_arch}/*.a
%{_libdir}/*.a


%changelog
* Thu Jan 10 2018 Stu<stu@quantumdetectors.com>
- Add devel package dependencies
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
- Split into devel package
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
