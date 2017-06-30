Name:           epics-edm
Version:        1.12.98
%define         subversion 5
Release:        1%{?dist}
Url:            https://ics-web.sns.ornl.gov/edm
Summary:        Extensible Display Manager
License:        GPL
Source:         https://github.com/epicsdeb/edm/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-5-root
BuildRequires:  git
BuildRequires:  epics-base-devel
BuildRequires:  epics-extensions
BuildRequires:  libXt-devel
BuildRequires:  libXmu-devel
BuildRequires:  motif-devel
BuildRequires:  motif-static
BuildRequires:  libXtst-devel
BuildRequires:  giflib-devel
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
Requires:       epics-base
Requires:       epics-extensions
Requires:       libXt
Requires:       libXmu
Requires:       libXtst
Requires:       motif
Requires:       giflib
Requires:       zlib
Requires:       libpng
Requires:       gtk2
Requires:       xorg-x11-fonts-Type1
Requires:       xorg-x11-fonts-75dpi
AutoReqProv:    no


%description
EPICS Controls System - EDM
Ported from https://github.com/epicsdeb/edm


%prep
%setup -q -n edm-debian-%{version}-%{subversion}
ln -s /usr/lib/epics/extensions/configure .

# Eh?
sed -i '1s;^;#include <zlib.h>\n;' pnglib/png.cc

git apply debian/patches/0001-fix-TOP.patch
git apply debian/patches/0004-fixup-font-list-for-Debian.patch
git apply debian/patches/0007-motif-and-X-libraries-in-system-path.patch

%define epics_host_arch %(/usr/lib/epics/startup/EpicsHostArch)


%build
export EPICS_HOST_ARCH=%{epics_host_arch}
export EPICS_BASE=/usr/lib/epics
make


edmlibs="EdmBase "
edmlibs+="cfcaa62e-8199-11d3-a77f-00104b8742df "
edmlibs+="114135a4-6f6c-11d3-95bc-00104b8742df "

edmpvplug="Epics Calc Loc Log"

edmplug="EdmBase "
edmplug+="57d79238-2924-420b-ba67-dfbecdf03fcd "
edmplug+="7e1b4e6f-239d-4650-95e6-a040d41ba633 "
edmplug+="cf322683-513e-4570-a44b-7cdd7cae0de5 "
edmplug+="EdmDiamond EdmTriumf Indicator "
edmplug+="MultSegRamp PV TwoDProfileMonitor "

# Build edm objs
%define _pwd %{_builddir}/edm-debian-%{version}-5
%define binbuild %{_pwd}/bin/%{epics_host_arch}
%define libbuild %{_pwd}/lib/%{epics_host_arch}

rm -f edmPvObjects
for pv in $edmpvplug; do \
echo $pv; \
EDMPVOBJECTS=%{_pwd} EDMOBJECTS=%{_pwd} \
LD_LIBRARY_PATH=%{libbuild}:$LD_LIBRARY_PATH %{binbuild}/edm -addpv %{libbuild}/lib$pv.so; \
done

rm -f edmObjects
for obj in $edmplug; do \
echo $obj; \
EDMPVOBJECTS=%{_pwd} EDMOBJECTS=%{_pwd} \
LD_LIBRARY_PATH=%{libbuild}:$LD_LIBRARY_PATH %{binbuild}/edm -add %{libbuild}/lib$obj.so; \
done

sed -i -e "s|%{libbuild}|%{_libdir}/edm|" edmObjects edmPvObjects
sed -i -e "s|edm/libEdmBase|libEdmBase|" edmObjects




%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%define __libdir %{_exec_prefix}/lib
%define epics_base %{buildroot}%{__libdir}/epics

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_libdir}/edm
install -d %{buildroot}%{_datadir}/edm
install -d %{buildroot}%{_sysconfdir}/edm


cp bin/%{epics_host_arch}/edm %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_bindir}/edm

edmlibs="EdmBase "
edmlibs+="cfcaa62e-8199-11d3-a77f-00104b8742df "
edmlibs+="114135a4-6f6c-11d3-95bc-00104b8742df "

edmpvplug="Epics Calc Loc Log"

# edmplug="EdmBase "
edmplug="57d79238-2924-420b-ba67-dfbecdf03fcd "
edmplug+="7e1b4e6f-239d-4650-95e6-a040d41ba633 "
edmplug+="cf322683-513e-4570-a44b-7cdd7cae0de5 "
edmplug+="EdmDiamond EdmTriumf Indicator "
edmplug+="MultSegRamp PV TwoDProfileMonitor "

# Basic libraries go in /usr/lib
for ff in $edmlibs;do \
    mv lib/%{epics_host_arch}/lib$ff.so %{buildroot}%{_libdir}; \
    # ln -s %{buildroot}%{_libdir}/lib$ff.so ../lib/epics/lib/
done

# Plugins go in /usr/lib/edm
for ff in $edmpvplug $edmplug;do \
    mv lib/%{epics_host_arch}/lib$ff.so %{buildroot}%{_libdir}/edm; \
    # ln -sr %{buildroot}%{_libdir}/edm/lib$ff.so ../../lib/epics/lib/
done

install -m 644 -t %{buildroot}%{_sysconfdir}/edm edmPvObjects edmObjects
install -m 644 -t %{buildroot}%{_sysconfdir}/edm setup/calc.list

cp -r helpFiles %{buildroot}%{_datadir}/edm/
find %{buildroot}%{_datadir}/edm/helpFiles -type f -exec chmod -x {} \;

install -m 644 -t %{buildroot}%{_sysconfdir}/edm edmMain/edmPrintDef

install -m 644 edmMain/colors.list %{buildroot}%{_sysconfdir}/edm
install -m 644 edmMain/fonts.list %{buildroot}%{_sysconfdir}/edm

install -m 755 contrib/fontparse.py %{buildroot}%{_datadir}/edm/


chmod 644 %{buildroot}%{_libdir}/*.so
chmod 644 %{buildroot}%{_libdir}/edm/*.so

chrpath --delete %{buildroot}%{_bindir}/edm
chrpath --delete %{buildroot}%{_libdir}/*.so
chrpath --delete %{buildroot}%{_libdir}/edm/*.so


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*
%{_sysconfdir}/*

%changelog
* Mon Jun 26 2017 Stu<stu@quantumdetectors.com>
- Missing dependency
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
