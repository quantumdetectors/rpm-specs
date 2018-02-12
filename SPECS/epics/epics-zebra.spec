Name:           epics-zebra
Version:        1
%define         subversion 13
Release:        1%{?dist}
Url:            https://github.com/quantumdetectors/zebra-epics
Summary:        EPICS Zebra Module
License:        GPL
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:	git
BuildRequires:  epics-base-devel
BuildRequires:  epics-asyn-devel
BuildRequires:  epics-busy-devel
BuildRequires:  epics-motor-devel
Requires:       epics-base
Requires:       epics-asyn
Requires:       epics-busy
Requires:       epics-motor
AutoReqProv:    no


%description
EPICS Controls System - Zebra


%package devel
Summary: EPICS Zebra development files
Provides: %{name}-devel
Requires: %{name} == %{version}
Requires: epics-base-devel
Requires: epics-asyn-devel
Requires: epics-busy-devel
Requires: epics-motor-devel

%description devel
This package contains necessary header files and static libraries for the EPICS Zebra module.


%prep
%setup -T -c -n %{name}-%{version}-%{subversion}
git clone %{url}.git .
git checkout qd-prod-pkg
%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
export EPICS_HOST_ARCH=%{epics_host_arch}
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

install -d %{epics_base}/bin/%{epics_host_arch}
install -d %{epics_base}/lib/%{epics_host_arch}

install -d %{epics_base}/iocBoot

install -d %{epics_base}/op/edl
install -d %{epics_base}/op/adl

install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_bindir}/

mv dbd %{epics_base}/
mv db %{epics_base}/

install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/

install zebraApp/opi/edl/*.edl %{epics_base}/op/edl/
# install zebraApp/opi/adl/*.adl %{epics_base}/op/adl/

mv iocs %{epics_base}/iocBoot/zebra
mv startStandalone.sh %{epics_base}/iocBoot/zebra/
mv zebraGui %{epics_base}/iocBoot/zebra/

chmod 755 %{epics_base}/iocBoot/zebra/*/bin/%{epics_host_arch}/*

chmod 644 %{epics_base}/iocBoot/zebra/*/dbd/*
chmod 644 %{epics_base}/iocBoot/zebra/*/db/*

chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.a
chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.so

chrpath --delete %{epics_base}/lib/%{epics_host_arch}/*.so

export GLOBIGNORE="*.sh:*-gui:*.boot:*envPaths"
chrpath --delete %{epics_base}/iocBoot/zebra/*/bin/%{epics_host_arch}/*
unset GLOBIGNORE

cd %{epics_base}/lib/%{epics_host_arch}
ln -sr * ../../../../..%{_libdir}/

cd %{epics_base}/bin/%{epics_host_arch}
ln -sr * ../../../../..%{_bindir}/

cd %{epics_base}/iocBoot/zebra/test/bin/%{epics_host_arch}
ln -sr sttest-gui ../../../../../../../..%{_bindir}/zebra-edm.sh
ln -sr sttest.sh ../../../../../../../..%{_bindir}/zebra-ioc.sh

cd %{epics_base}/iocBoot/zebra
ln -sr startStandalone.sh ../../../../..%{_bindir}/zebra-standalone.sh

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{__libdir}/*
%{_libdir}/*
%{_bindir}/*
%exclude %{__libdir}/epics/lib/%{epics_host_arch}/*.a
%exclude %{_libdir}/*.a


%files devel
%{__libdir}/epics/lib/%{epics_host_arch}/*.a
%{_libdir}/*.a


%changelog
* Fri Feb 09 2018 Stu<stu@quantumdetectors.com>
– Initial rpm build
