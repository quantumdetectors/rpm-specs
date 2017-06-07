Name:           epics-autosave
Version:        5.7.1
%define         subversion 2
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/autosave
Summary:        EPICS Autosave Module
License:        GPL
Source:         https://github.com/epicsdeb/autosave/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base
Requires:       epics-base
AutoReqProv:    no


%description
EPICS Controls System - Autosave Package
Ported from https://github.com/epicsdeb/autosave


%prep
%setup -q -n autosave-debian-%{version}-%{subversion}
git apply debian/patches/0001-RELEASE.patch
git apply debian/patches/0003-install-db-and-req-files.patch
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

mv dbd %{epics_base}/
mv db %{epics_base}/
mv include %{epics_base}/

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

# cd %{epics_base}/bin/%{epics_host_arch}
# ln -sr * ../../../../..%{_bindir}/


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
