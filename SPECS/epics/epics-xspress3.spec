Name:           epics-xspress3
Version:        1
%define         subversion 13
Release:        7%{?dist}
Url:            https://github.com/quantumdetectors/xspress3-epics
Summary:        EPICS Xspress 3 Module
License:        GPL
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:	git
BuildRequires:  epics-base-devel
BuildRequires:  epics-areadetector-devel
BuildRequires:  epics-asyn-devel
BuildRequires:  epics-calc-devel
BuildRequires:  epics-busy-devel
BuildRequires:  epics-deviocstats-devel
BuildRequires:  epics-spectraplugins-devel
Requires:       epics-base
Requires:       epics-areadetector
Requires:       epics-asyn
Requires:       epics-calc
Requires:       epics-busy
Requires:       epics-deviocstats
Requires:       epics-spectraplugins
AutoReqProv:    no


%description
EPICS Controls System - Xspress 3


%package devel
Summary: EPICS Xspress3 development files
Provides: %{name}-devel
Requires: %{name} == %{version}
Requires: epics-base-devel
Requires: epics-areadetector-devel
Requires: epics-asyn-devel
Requires: epics-calc-devel
Requires: epics-busy-devel
Requires: epics-deviocstats-devel
Requires: epics-spectraplugins-devel

%description devel
This package contains necessary header files and static libraries for the EPICS Xspress3 module.


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
install -m 777 -d %{buildroot}%{_sysconfdir}/epics/xspress3/settings

install -d %{buildroot}%{_sysconfdir}/profile.d
install etc/profile.d/epics.sh %{buildroot}%{_sysconfdir}/profile.d/

mv dbd %{epics_base}/
mv db %{epics_base}/
mv include %{epics_base}/

#install bin/%{epics_host_arch}/* %{epics_base}/bin/%{epics_host_arch}/
install lib/%{epics_host_arch}/* %{epics_base}/lib/%{epics_host_arch}/
install data/*.edl %{epics_base}/op/edl/
install data/*.adl %{epics_base}/op/adl/

mv iocs %{epics_base}/iocBoot/xspress3
rm -rf %{epics_base}/iocBoot/xspress3/*/iocBoot
rm -rf %{epics_base}/iocBoot/xspress3/*/configure
rm -rf %{epics_base}/iocBoot/xspress3/*/data/*
rm -rf %{epics_base}/iocBoot/xspress3/*/Makefile
rm -rf %{epics_base}/iocBoot/xspress3/*/test

for ioc in %{epics_base}/iocBoot/xspress3/example*/; do 
    cp ${ioc}/example*/data/*.xml ${ioc}data/
done

rm -rf %{epics_base}/iocBoot/xspress3/*/example*


sed -r -i -e 's|cd "%{_builddir}/%{name}-%{version}-%{subversion}/iocs/(example[0-9]+Channel(Mini)?)"|cd "/usr/lib/epics/iocBoot/xspress3/\1"|' %{epics_base}/iocBoot/xspress3/*/bin/%{epics_host_arch}/*.boot
sed -r -i -e 's|dbpf\("XSPRESS3-EXAMPLE:CONFIG_PATH", "%{_builddir}/%{name}-%{version}-%{subversion}/xspress3_settings/([0-9]+channel)"\)|dbpf\("XSPRESS3-EXAMPLE:CONFIG_PATH", "/etc/epics/xspress3/settings/\1"\)|' %{epics_base}/iocBoot/xspress3/*/bin/%{epics_host_arch}/*.boot
sed -r -i -e 's|dbpf XSPRESS3-EXAMPLE:NDAttributesFile, example[0-9]+ChannelApp/(data/XSP3.xml)|dbpf XSPRESS3-EXAMPLE:NDAttributesFile, \1|' %{epics_base}/iocBoot/xspress3/*/bin/%{epics_host_arch}/*.boot


chmod 755 %{epics_base}/iocBoot/xspress3/*/bin/%{epics_host_arch}/*
chmod 755 %{epics_base}/iocBoot/xspress3/xspress3-ioc.sh

chmod 644 %{epics_base}/iocBoot/xspress3/*/dbd/*
chmod 644 %{epics_base}/iocBoot/xspress3/*/db/*

chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.a
chmod 644 %{epics_base}/lib/%{epics_host_arch}/*.so
#chmod 755 %{epics_base}/bin/%{epics_host_arch}/*

chrpath --delete %{epics_base}/lib/%{epics_host_arch}/*.so
#chrpath --delete %{epics_base}/bin/%{epics_host_arch}/*

export GLOBIGNORE="*.sh:*-gui:*.boot"
chrpath --delete %{epics_base}/iocBoot/xspress3/*/bin/%{epics_host_arch}/*
unset GLOBIGNORE

cd %{epics_base}/lib/%{epics_host_arch}
ln -sr * ../../../../..%{_libdir}/

#cd %{epics_base}/bin/%{epics_host_arch}
#ln -sr * ../../../../..%{_bindir}/

cd %{epics_base}/iocBoot/xspress3/xspress3Example/bin/%{epics_host_arch}
ln -sr xspress3-medm.sh ../../../../../../../..%{_bindir}/
ln -sr xspress3-edm.sh ../../../../../../../..%{_bindir}/

cd %{epics_base}/iocBoot/xspress3
ln -sr xspress3-ioc.sh ../../../../..%{_bindir}/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{__libdir}/*
%{_libdir}/*
%{_bindir}/*
%{_sysconfdir}/*
%exclude %{__libdir}/epics/include/*
%exclude %{__libdir}/epics/lib/%{epics_host_arch}/*.a
%exclude %{_libdir}/*.a


%files devel
%{__libdir}/epics/include/*
%{__libdir}/epics/lib/%{epics_host_arch}/*.a
%{_libdir}/*.a


%changelog
* Wed Sep 16 2020 Liam<liam@quantumdetectors.com>
- Update library and X3 server for X3X fan control
* Wed Jun 19 2019 Liam<liam@quantumdetectors.com>
- Update library and headers for RevE 
* Tue Jan 22 2019 Stu<stu@quantumdetectors.com>
- Bump sdk for X4, add X3m IOCs, limit frames for X3m
* Mon Mar 12 2018 Stu<stu@quantumdetectors.com>
- Remove x3.server and imgd
* Wed Feb 7 2018 Stu<stu@quantumdetectors.com>
- Update all ROI/SCA lengths, remove old settings, add epics.sh
* Thu Jan 11 2018 Stu<stu@quantumdetectors.com>
- Add devel package dependencies
* Mon Aug 21 2017 Stu<stu@quantumdetectors.com>
- 2 channel ioc
* Mon Jun 26 2017 Stu<stu@quantumdetectors.com>
- X3m 4 channel ioc
* Mon Jun 26 2017 Stu<stu@quantumdetectors.com>
- Update edm screens
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
- Split into devel package
* Wed Jun 07 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
