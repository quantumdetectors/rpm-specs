Name:           epics-base
Version:        3.15.3
%define         subversion 12
Release:        1%{?dist}
Url:            https://github.com/epicsdeb/epics-base
Summary:        EPICS Controls System Base
License:        GPL
Source:         https://github.com/epicsdeb/epics-base/archive/debian/%{version}-%{subversion}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  git
AutoReqProv:    no


%description
EPICS Controls System - Base Package
Ported from https://github.com/epicsdeb/epics-base

%prep
%setup -q -n epics-base-debian-%{version}-%{subversion}
git apply debian/patches/0002-look-for-base-config-in-etc-epics-configure.patch
git apply debian/patches/0003-allow-more-flexible-makefile-config.patch
%define epics_host_arch linux-x86_64


%build
%{__make}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%define __libdir %{_exec_prefix}/lib

%define epics_base %{buildroot}%{__libdir}/epics

mkdir -p %{epics_base}/bin/%{epics_host_arch}
mkdir -p %{epics_base}/lib/%{epics_host_arch}
mkdir -p %{epics_base}/startup

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_sysconfdir}/epics

cp -r bin/linux-* %{epics_base}/bin/
cp -r configure %{epics_base}/
cp -r db %{epics_base}/
cp -r dbd %{epics_base}/
cp -r include %{epics_base}/
cp -r templates %{epics_base}/

mv lib/%{epics_host_arch}/libCom* %{epics_base}/lib/%{epics_host_arch}/
mv lib/%{epics_host_arch}/libca* %{epics_base}/lib/%{epics_host_arch}/
mv lib/%{epics_host_arch}/libgdd* %{epics_base}/lib/%{epics_host_arch}/
mv lib/%{epics_host_arch}/libdbCore* %{epics_base}/lib/%{epics_host_arch}/
mv lib/%{epics_host_arch}/libdbRecStd* %{epics_base}/lib/%{epics_host_arch}/

sed -i -e 's!%{_builddir}/epics-base-debian-%{version}-%{subversion}!%{__libdir}/epics!g' lib/pkgconfig/*.pc
cp -r lib/pkgconfig %{buildroot}%{_datadir}/

mkdir -p %{epics_base}/lib/perl
cp lib/perl/DBD.pm %{epics_base}/lib/perl/
cp -r lib/perl/DBD %{epics_base}/lib/perl/


%define perllib %(perl -MConfig -e 'print $Config{vendorlib}')
%define perlarch %(perl -MConfig -e 'print $Config{vendorarch}')

mkdir -p %{buildroot}/%{perllib}/
mkdir -p %{buildroot}/%{perlarch}/auto
mv lib/perl/EPICS %{buildroot}/%{perllib}/

mv lib/perl/CA.pm %{buildroot}/%{perlarch}/
mv lib/perl/5.*/*/libCap5.so %{buildroot}/%{perlarch}/auto/
chmod 644 %{buildroot}/%{perlarch}/auto/*.so


cp -r html %{epics_base}/

cp startup/EpicsHostArch %{epics_base}/startup/
cp startup/EpicsHostArch.pl %{epics_base}/startup/
cp startup/Site.profile %{epics_base}/startup/

#configure/Sample.Makefile %{epics_base}/configure/

chmod 644 %{epics_base}/lib/linux-*/*.a
chmod 644 %{epics_base}/lib/linux-*/*.so
chmod 755 %{epics_base}/bin/linux-*/*

chrpath --delete %{epics_base}/lib/linux-*/*.so

chrpath --delete %{epics_base}/bin/linux-*/antelope
chrpath --delete %{epics_base}/bin/linux-*/e_flex
chrpath --delete %{epics_base}/bin/linux-*/iocLogServer
chrpath --delete %{epics_base}/bin/linux-*/caRepeater
chrpath --delete %{epics_base}/bin/linux-*/catime
chrpath --delete %{epics_base}/bin/linux-*/caConnTest
chrpath --delete %{epics_base}/bin/linux-*/casw
chrpath --delete %{epics_base}/bin/linux-*/caEventRate
chrpath --delete %{epics_base}/bin/linux-*/ca_test
chrpath --delete %{epics_base}/bin/linux-*/acctst
chrpath --delete %{epics_base}/bin/linux-*/caget
chrpath --delete %{epics_base}/bin/linux-*/camonitor
chrpath --delete %{epics_base}/bin/linux-*/cainfo
chrpath --delete %{epics_base}/bin/linux-*/caput
chrpath --delete %{epics_base}/bin/linux-*/aitGen
chrpath --delete %{epics_base}/bin/linux-*/genApps
chrpath --delete %{epics_base}/bin/linux-*/makeBpt
chrpath --delete %{epics_base}/bin/linux-*/ascheck
chrpath --delete %{epics_base}/bin/linux-*/msi
chrpath --delete %{epics_base}/bin/linux-*/caDirServ
chrpath --delete %{epics_base}/bin/linux-*/excas
chrpath --delete %{epics_base}/bin/linux-*/softIoc
chrpath --delete %{buildroot}/%{perlarch}/auto/libCap5.so

cd %{epics_base}/lib/%{epics_host_arch}
ln -sr * ../../../../..%{_libdir}/

cd %{epics_base}/bin/%{epics_host_arch}
ln -sr * ../../../../..%{_bindir}/

cd %{epics_base}/startup
ln -sr ./EpicsHostArch ../lib/host

cd %{epics_base}
ln -sr configure ../../..%{_sysconfdir}/epics/

# %post
# %define epics_base %{__libdir}/epics
# %{__ln_s} %{epics_base}/bin/*/ascheck %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/makeBaseApp.pl %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/makeBaseExt.pl %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/iocLogServer %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/msi %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/caget %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/cainfo %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/camonitor %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/caput %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/caRepeater %{_bindir}/
# %{__ln_s} %{epics_base}/bin/*/casw %{_bindir}/
# %{__ln_s} %{epics_base}/configure %{_sysconfdir}/epics/

# %{__ln_s} %{epics_base}/lib/linux-*/libCom.so.%{version} %{_libdir}/
# %{__ln_s} %{epics_base}/lib/linux-*/libca.so.%{version} %{_libdir}/
# %{__ln_s} %{epics_base}/lib/linux-*/libgdd.so.%{version} %{_libdir}/
# %{__ln_s} %{epics_base}/lib/linux-*/libcas.so.%{version} %{_libdir}/
# %{__ln_s} %{epics_base}/lib/linux-*/libdbCore.so.%{version} %{_libdir}/
# %{__ln_s} %{epics_base}/lib/linux-*/libdbRecStd.so.%{version} %{_libdir}/

# # This path is used by CA.pm
# ln -s %{epics_base}/startup/EpicsHostArch %{epics_base}/lib/host

# %postun
# rm -f %{_bindir}/ascheck
# rm -f %{_bindir}/makeBaseApp.pl
# rm -f %{_bindir}/makeBaseExt.pl
# rm -f %{_bindir}/iocLogServer
# rm -f %{_bindir}/msi
# rm -f %{_bindir}/caget
# rm -f %{_bindir}/cainfo
# rm -f %{_bindir}/camonitor
# rm -f %{_bindir}/caput
# rm -f %{_bindir}/caRepeater
# rm -f %{_bindir}/casw
# rm -f %{_sysconfdir}/epics/configure

# rm -f %{_libdir}/libCom.so.%{version}
# rm -f %{_libdir}/libca.so.%{version}
# rm -f %{_libdir}/libgdd.so.%{version}
# rm -f %{_libdir}/libcas.so.%{version}
# rm -f %{_libdir}/libdbCore.so.%{version}
# rm -f %{_libdir}/libdbRecStd.so.%{version}


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{__libdir}/*
%{_datadir}/*
%{_sysconfdir}/*
%{_libdir}/*
%{_bindir}/*

%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
