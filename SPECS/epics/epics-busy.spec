Name:           epics-busy
Version:        1.6.1
%define         subversion 1
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/busy
Summary:        EPICS Busy Module
License:        GPL
Source:         https://github.com/epicsdeb/busy/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base
BuildRequires:  epics-asyn
Requires:       epics-base
Requires:       epics-asyn
AutoReqProv:    no


%description
EPICS Controls System - Busy Package
Ported from https://github.com/epicsdeb/busy


%prep
%setup -q -n busy-debian-%{version}-%{subversion}
git apply debian/patches/0001-RELEASE.patch
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


%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
