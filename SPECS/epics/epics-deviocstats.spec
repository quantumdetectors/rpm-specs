Name:           epics-deviocstats
Version:        3.1.9
%define         subversion 5
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/deviocstats
Summary:        EPICS deviocstats Module
License:        GPL
Source:         https://github.com/epicsdeb/deviocstats/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base
Requires:       epics-base
AutoReqProv:    no


%description
EPICS Controls System - deviocstats Package
Ported from https://github.com/epicsdeb/deviocstats


%prep
%setup -q -n deviocstats-debian-%{version}-%{subversion}
%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

install -d %{epics_base}/bin/%{epics_host_arch}
install -d %{epics_base}/lib/%{epics_host_arch}

install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_bindir}/
install -d %{epics_base}/op/edl

mv dbd %{epics_base}/
mv db %{epics_base}/
mv include %{epics_base}/
mv iocAdmin/srcDisplay/*.edl %{epics_base}/op/edl/
mv debian/ioc_stats_settings.req %{epics_base}/db/

install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/

chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.a
chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.so

cd %{epics_base}/lib/%{epics_host_arch}
ln -sr * ../../../../..%{_libdir}/

cd %{epics_base}/bin/%{epics_host_arch}
ln -sr * ../../../../..%{_bindir}/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{__libdir}/*
%{_libdir}/*
# %{_bindir}/*


%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
