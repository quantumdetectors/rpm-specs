Name:           lima-xspress3
Version: 		1.74
Release: 		1%{?dist}
Url: 			https://github.com/quantumdetectors/Lima-camera-xspress3
Summary: 		Lima Xspress 3 Device Server
License: 		GPL
Source: 		Lima-%{version}.tar.gz
Packager: 		quantumdetectors.com
BuildRoot: 		%{_tmppath}/%{name}-%{version}-root
Patch0: 		Lima-xspress3-config.inc.patch
Requires:		python-pytango
Requires: 		python-gevent
Requires: 		python-bottle
Requires: 		numpy
Requires: 		sip
Requires: 		gsl
BuildRequires:	gsl-devel
BuildRequires:	sip-devel
BuildRequires:	chrpath

%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%description
Xspress 3 Lima Device Server

%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}

%prep
%setup -q -n Lima-%{version}
cp config.inc_default config.inc
%patch0 -p0
tar xvfz camera/xspress3/sdk/sdk_linux_libs.tar.gz -C camera/xspress3/sdk/

%build
%{__make} config
%{__make}
%{__make} -C sip

%install
%define limax3 %{buildroot}%{python_sitelib}/Lima/xspress3
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export QA_RPATHS=$[ 0x0001|0x0002|0x0020 ]
export INSTALL_DIR=%{limax3}
%{__make} install

cp --preserve=links %{_builddir}/Lima-%{version}/camera/xspress3/sdk/libs/linux.x86_64/* %{limax3}/Lima/lib/
cp -r %{_builddir}/Lima-%{version}/applications/tango/python %{limax3}/

mkdir -p %{buildroot}%{_bindir}
cp %{_sourcedir}/Lima-xspress3-LimaCCDs %{buildroot}%{_bindir}/LimaCCDs

chrpath --delete %{limax3}/Lima/lib/libhdf5_cpp.so.9.0.0
chrpath --delete %{limax3}/Lima/lib/libhdf5_hl.so.9.0.0
chrpath --delete %{limax3}/Lima/lib/libhdf5_hl_cpp.so.9.0.0
chrpath --delete %{limax3}/Lima/lib/liblimacore.so.1.7.0
chrpath --delete %{limax3}/Lima/lib/liblimaxspress3.so.1.4.0
chrpath --delete %{limax3}/Lima/bin/h5diff
chrpath --delete %{limax3}/Lima/bin/h5ls
chrpath --delete %{limax3}/Lima/bin/h5dump
chrpath --delete %{limax3}/Lima/bin/h5debug
chrpath --delete %{limax3}/Lima/bin/h5repart
chrpath --delete %{limax3}/Lima/bin/h5mkgrp
chrpath --delete %{limax3}/Lima/bin/h5import
chrpath --delete %{limax3}/Lima/bin/h5repack
chrpath --delete %{limax3}/Lima/bin/h5jam
chrpath --delete %{limax3}/Lima/bin/h5unjam
chrpath --delete %{limax3}/Lima/bin/h5copy
chrpath --delete %{limax3}/Lima/bin/h5stat
chrpath --delete %{limax3}/Lima/bin/gif2h5
chrpath --delete %{limax3}/Lima/bin/h52gif
chrpath --delete %{limax3}/Lima/bin/h5perf_serial


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%{python_sitelib}/Lima/xspress3/Lima*
%{python_sitelib}/Lima/xspress3/python*
%{_bindir}/LimaCCDs


%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
