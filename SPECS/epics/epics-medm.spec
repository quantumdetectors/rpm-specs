Name:           epics-medm
Version:        3
%define         subversion 1_12
Release:        1%{?dist}
Url:            https://ics-web.sns.ornl.gov/edm
Summary:        Extensible Display Manager
License:        GPL
Source:         MEDM%{version}_%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{subversion}-root
BuildRequires:  git
BuildRequires:  epics-base-devel
BuildRequires:  epics-extensions
Requires:       epics-base
Requires:       epics-extensions
AutoReqProv:    no


%description
EPICS Controls System - MEDM


%package devel
Summary: EPICS MEDM development files
Provides: %{name}-devel
Requires: %{name} == %{version}
Requires: epics-base-devel
Requires: epics-extensions

%description devel
This package contains necessary header files and static libraries for EPICS MEDM


%prep
%setup -q -n medm-MEDM%{version}_%{subversion}
ln -s /usr/lib/epics/extensions/configure .

sed -i -e "s|TOP = ../..|TOP =.|" Makefile
sed -i -e "s|TOP = ../../..|TOP = ./..|" printUtils/Makefile
sed -i -e "s|TOP = ../../..|TOP = ./..|" xc/Makefile
sed -i -e "s|TOP = ../../..|TOP = ./..|" medm/Makefile

sed -i -e "s|USR_LIBS_DEFAULT = Xm Xt Xmu X11 Xext|#USR_LIBS_DEFAULT = Xt Xm Xmu X11 Xext|" medm/Makefile
sed -i -e "s|USR_LIBS_Linux = Xm Xt Xp Xmu X11 Xext|USR_SYS_LIBS_Linux = Xm Xt Xp Xmu X11 Xext|" medm/Makefile

%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
export EPICS_HOST_ARCH=%{epics_host_arch}
export EPICS_BASE=/usr/lib/epics
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_libdir}/


cp bin/%{epics_host_arch}/medm %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_bindir}/medm

cp lib/%{epics_host_arch}/* %{buildroot}%{_libdir}/
chmod 644 %{buildroot}%{_libdir}/*.a

chrpath --delete %{buildroot}%{_bindir}/medm


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/*.a


%files devel
%{_libdir}/*.a


%changelog
* Thu Jan 10 2018 Stu<stu@quantumdetectors.com>
- Add devel package dependencies
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
- Split into devel package
* Tue Jun 06 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
