Name:           epics-spectraplugins
Version:        1
%define         subversion 6
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/spectraplugins
Summary:        EPICS spectraplugins Module
License:        GPL
Source:         spectraPlugins-%{version}-%{subversion}.zip
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base-devel
BuildRequires:  epics-seq-devel
BuildRequires:  epics-areadetector-devel
Requires:       epics-base
Requires:       epics-seq
Requires:       epics-areadetector
AutoReqProv:    no


%description
EPICS Controls System - spectraplugins Package
Ported from https://github.com/epicsdeb/spectraplugins


%package devel
Summary: EPICS Spectraplugins development files
Provides: %{name}-devel
Requires: %{name} == %{version}
Requires: epics-base-devel
Requires: epics-seq-devel
Requires: epics-areadetector-devel

%description devel
This package contains necessary header files and static libraries for the EPICS Spectraplugins module.


%prep
%setup -q -n spectraPlugins-%{version}-%{subversion}
sed -i -e "s|SUPPORT=/home/xspress3/software/epics/R3.14.12.3/support|#SUPPORT=/home/xspress3/software/epics/R3.14.12.3/support|" configure/RELEASE
sed -i -e "s|ASYN=\$(SUPPORT)/asyn4-21|ASYN=\$(EPICS_BASE)|" configure/RELEASE
sed -i -e "s|AREA_DETECTOR=\$(SUPPORT)/areaDetectorR1-9-1|AREA_DETECTOR=\$(EPICS_BASE)|" configure/RELEASE
sed -i -e "s|EPICS_BASE=/home/xspress3/software/epics/R3.14.12.3/base|EPICS_BASE=/usr/lib/epics|" configure/RELEASE
rm -rf spectraPluginsApp/protocol
make clean

%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

install -d %{epics_base}/lib/%{epics_host_arch}

install -d %{buildroot}%{_libdir}/
install -d %{epics_base}/op/edl
install -d %{epics_base}/op/adl

mv dbd %{epics_base}/
mv db %{epics_base}/

cp -r spectraPluginsApp/opi/edl/*.edl %{epics_base}/op/edl/
cp -r spectraPluginsApp/opi/adl/*.adl %{epics_base}/op/adl/

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
%exclude %{__libdir}/epics/lib/%{epics_host_arch}/*.a
%exclude %{_libdir}/*.a


%files devel
%{__libdir}/epics/lib/%{epics_host_arch}/*.a
%{_libdir}/*.a


%changelog
* Thu Jan 10 2018 Stu<stu@quantumdetectors.com>
- Add devel package dependencies
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
- Split into devel package
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
