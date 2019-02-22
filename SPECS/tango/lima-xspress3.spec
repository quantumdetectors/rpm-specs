Name:           lima-xspress3
Version:        1.74
Release:        1%{?dist}
Url:            https://github.com/quantumdetectors/Lima-camera-xspress3
Summary:        Lima Xspress 3 Device Server
License:        GPL
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:       python-pytango
Requires:       python-gevent
Requires:       numpy
Requires:       sip
Requires:       gsl
BuildRequires:  git
BuildRequires:  gsl-devel
BuildRequires:  sip-devel
BuildRequires:  chrpath
AutoReqProv:    no

%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%description
Xspress 3 Lima Device Server

%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}

%prep
%setup -T -c -n %{name}-%{version}

git clone https://github.com/esrf-bliss/Lima .

# hotfix
git checkout 82d34c

git submodule init third-party/Processlib third-party/Sps third-party/libconfig third-party/hdf5
git submodule init camera/xspress3
git submodule init applications/tango/python

git submodule update

sed -i -e 's|git://github.com/esrf-bliss/Lima-camera-xspress3|git://github.com/quantumdetectors/Lima-camera-xspress3|' .gitmodules
sed -i -e 's|git://github.com/esrf-bliss/Lima-tango-python|git://github.com/quantumdetectors/Lima-tango-python|' .gitmodules

git submodule sync
git submodule update

git --git-dir=camera/xspress3/.git checkout master
git --git-dir=camera/xspress3/.git pull

git --git-dir=applications/tango/python/.git checkout master
git --git-dir=applications/tango/python/.git pull


cp config.inc_default config.inc
sed -i -e 's|COMPILE_SIMULATOR=1|COMPILE_SIMULATOR=0|' config.inc
sed -i -e 's|COMPILE_XSPRESS3=0|COMPILE_XSPRESS3=1|' config.inc
sed -i -e 's|COMPILE_HDF5_SAVING=0|COMPILE_HDF5_SAVING=1|' config.inc

tar xvfz camera/xspress3/sdk/sdk_linux_libs.tar.gz -C camera/xspress3/sdk/

# libconfig is trying to regenerate grammar, dont know why?
echo "exit" > third-party/libconfig/aux-build/ylwrap

%build
%{__make} config
%{__make}
%{__make} -C sip

%install
%define limax3 %{buildroot}%{python_sitelib}/Lima/xspress3
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export INSTALL_DIR=%{limax3}
%{__make} install

cp --preserve=links camera/xspress3/sdk/libs/linux.x86_64/* %{limax3}/Lima/lib/
cp -r applications/tango/python %{limax3}/

mkdir -p %{buildroot}%{_bindir}
cp %{_sourcedir}/Lima-xspress3-LimaCCDs %{buildroot}%{_bindir}/LimaCCDs

cp camera/xspress3/scripts/createdevice.py %{limax3}/
chmod 755 %{limax3}/createdevice.py

mkdir -p %{limax3}/test
cp -r camera/xspress3/test/*.py %{limax3}/test/
cp -r camera/xspress3/test/*.cpp %{limax3}/test/

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
%{python_sitelib}/Lima/xspress3/test/*
%{python_sitelib}/Lima/xspress3/createdevice.py
%{_bindir}/LimaCCDs

%post
export TANGO_HOST=localhost:10000
%{python_sitelib}/Lima/xspress3/createdevice.py -n xspress3

%changelog
* Fri Feb 15 2019 Stu<stu@quantumdetectors.com>
– SDK Bump, X4 Support
* Fri Jun 30 2017 Stu<stu@quantumdetectors.com>
– Multicard support, updated test scripts
* Thu Jun 08 2017 Stu<stu@quantumdetectors.com>
– Remove patch, build from git, sync with qd master, install tests and helper scripts
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
