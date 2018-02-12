Name:           epics-motor
Version:        6.9
%define         subversion 1
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/motor
Summary:        EPICS Motor Module
License:        GPL
Source:         https://github.com/epicsdeb/motor/archive/master.zip
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base-devel
BuildRequires:  epics-asyn-devel
BuildRequires:  epics-busy-devel
BuildRequires:  epics-seq-devel
Requires:       epics-base
Requires:       epics-asyn
Requires:       epics-busy
Requires:       epics-seq
AutoReqProv:    no


%description
EPICS Controls System - Busy Package
Ported from https://github.com/epicsdeb/busy


%package devel
Summary: EPICS Busy development files
Provides: %{name}-devel
Requires: %{name} == %{version}
Requires: epics-base-devel
Requires: epics-asyn-devel
Requires: epics-busy-devel
Requires: epics-seq-devel

%description devel
This package contains necessary header files and static libraries for the EPICS Motor module.


%prep
%setup -q -n motor-master
git apply debian/patches/0001-RELEASE.patch
git apply debian/patches/0002-disable-build-of-hytec-controller.patch
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

# install -d %{epics_base}/op/edl
install -d %{epics_base}/op/adl

install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/

# install motorApp/op/edl/*.edl %{epics_base}/op/edl/
install motorApp/op/adl/*.adl %{epics_base}/op/adl/

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
* Fri Feb 09 2018 Stu<stu@quantumdetectors.com>
– Initial rpm build
