Name:           epics-seq
Version:        2.2.3
%define         subversion 4
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/seq
Summary:        EPICS Seq Module
License:        GPL
Source:         https://github.com/epicsdeb/seq/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  re2c
BuildRequires:  epics-base
Requires:       epics-base
AutoReqProv:    no

%description
EPICS Controls System - Seq Module
Ported from https://github.com/epicsdeb/seq


%prep
%setup -q -n seq-debian-%{version}-%{subversion}
git apply debian/patches/0001-Set-EPICS_BASE-correctly.patch
%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)
# export EPICS_HOST_ARCH=%{epics_host_arch}


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

mv dbd %{epics_base}/
mv db %{epics_base}/
mv include %{epics_base}/

install -d %{epics_base}/configure/rules.d
mv configure/RULES_BUILD %{epics_base}/configure/rules.d/seqsnc.make


install bin/%{epics_host_arch}/* %{epics_base}/bin/%{epics_host_arch}/
install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/

chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.a
chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.so
chmod 755 %{epics_base}/bin/%{epics_host_arch}/*

chrpath --delete %{epics_base}/lib/%{epics_host_arch}/*.so

export GLOBIGNORE="*.pl"
chrpath --delete %{epics_base}/bin/%{epics_host_arch}/*
unset GLOBIGNORE

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
%{_bindir}/*


%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
