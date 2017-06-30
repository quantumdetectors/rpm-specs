Name:           epics-areadetector
Version:        1.9.1
%define         subversion dfsg1-1
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/areadetector
Summary:        EPICS Areadetector Module
License:        GPL
Source:         https://github.com/epicsdeb/areadetector/archive/debian/%{version}+%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  epics-base-devel
BuildRequires:  epics-asyn-devel
BuildRequires:  epics-calc-devel
BuildRequires:  epics-busy-devel
BuildRequires:  epics-sscan-devel
BuildRequires:  epics-autosave-devel
BuildRequires:  netcdf-devel
BuildRequires:  GraphicsMagick-devel
BuildRequires:  libtiff-devel
BuildRequires:  CBFlib-devel
Requires:       epics-base
Requires:       epics-asyn
Requires:       epics-calc
Requires:       epics-busy
Requires:       epics-sscan
Requires:       epics-autosave
Requires:       netcdf
Requires:       GraphicsMagick
Requires:       GraphicsMagick-c++
Requires:       libtiff
Requires:       CBFlib
Requires:       libpng12
AutoReqProv:    no


%description
EPICS Controls System - Areadetector Package
Ported from https://github.com/epicsdeb/areadetector


%package devel
Summary: EPICS Areadetector development files
Provides: %{name}-devel
Requires: %{name} == %{version}

%description devel
This package contains necessary header files and static libraries for the EPICS Areadetector module.


%prep
%setup -q -n areadetector-debian-%{version}-%{subversion}
git apply debian/patches/0001-fix-RELEASE.patch
git apply debian/patches/0002-Use-system-cbf-library.patch
git apply debian/patches/0003-cbf-API-differences.patch
git apply debian/patches/0004-Use-TOP.patch
git apply debian/patches/0005-Adjust-build.patch
git apply debian/patches/0016-Do-not-build-Andor-drivers.patch
sed -i -e "s|PROD_LIBS               += calc busy sscan autosave mca|PROD_LIBS               += calc seq pv busy sscan autosave|" ADApp/commonDriverMakefile
%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

install -d %{epics_base}/bin/%{epics_host_arch}
install -d %{epics_base}/lib/%{epics_host_arch}
install -d %{epics_base}/op
install -d %{epics_base}/as/req
install -d %{epics_base}/common/ADApp

install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_bindir}/

mv dbd %{epics_base}/
mv db %{epics_base}/
mv include %{epics_base}/

cp -r ADApp/op/* %{epics_base}/op/
cp -r ADApp/Db/*.req %{epics_base}/as/req
cp -r ADApp/commonDriverMakefile %{epics_base}/common/ADApp/

install bin/%{epics_host_arch}/* %{epics_base}/bin/%{epics_host_arch}/
install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/

chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.a
chmod 755 %{epics_base}/bin/%{epics_host_arch}/*


export GLOBIGNORE="*.pl"
chrpath --delete %{epics_base}/bin/%{epics_host_arch}/*
unset GLOBIGNORE

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
* Mon Jun 26 2017 Stu<stu@quantumdetectors.com>
- Missing dependency
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
- Split into devel package
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
