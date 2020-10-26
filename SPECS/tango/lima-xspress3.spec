Name:           lima-xspress3
Version:        1.9
Release:        1%{?dist}
Url:            https://github.com/quantumdetectors/Lima-camera-xspress3
Summary:        Lima Xspress 3 Device Server
License:        GPL
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:       python-pytango
Requires:       python-gevent
Requires:       numpy
Requires:       gsl
Requires:       hdf5 = 1.10.7
BuildRequires:  git
BuildRequires:  gsl-devel
BuildRequires:  sip = 4.19.8
BuildRequires:  chrpath
BuildRequires:  hdf5-devel = 1.10.7
AutoReqProv:    no

# Run this spec with:
#   QA_SKIP_BUILD_ROOT=1 rpmbuild -bb .
# For some reason check-buildroot still finds references to the ${BUILDROOT}

# RPM for sip version is in maxiv repo:
# http://pubrepo.maxiv.lu.se/rpm/el7/x86_64/sip-4.19.8-1.el7.x86_64.rpm

%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%description
Xspress 3 Lima Device Server

%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}

%prep
%setup -T -c -n %{name}-%{version}

git clone https://github.com/esrf-bliss/Lima .

git submodule init camera/xspress3
git submodule init camera/common/meta
git submodule init applications/tango/python
git submodule init third-party/Processlib

sed -i -e 's|git://|https://|' .gitmodules
git submodule sync
git submodule update


git --git-dir=camera/xspress3/.git checkout master
git --git-dir=camera/xspress3/.git pull
git --git-dir=camera/xspress3/.git remote add qd https://github.com/quantumdetectors/Lima-camera-xspress3
git --git-dir=camera/xspress3/.git fetch qd

# Fix cmake build
git --git-dir=camera/xspress3/.git merge --no-edit qd/fix/cmake

# Fix threading model
git --git-dir=camera/xspress3/.git merge --no-edit qd/threading

# Fixes clocks, various updates
git --git-dir=camera/xspress3/.git merge --no-edit qd/master


cp scripts/config.txt_default scripts/config.txt
sed -i -e 's|LIMACAMERA_SIMULATOR=1|LIMACAMERA_SIMULATOR=0|' scripts/config.txt

# Update libs from latest tar.gz
tar xvfz camera/xspress3/sdk/sdk_linux_libs.tar.gz -C camera/xspress3/sdk/

%build
./install.sh --install=no xspress3 hdf5 python pytango-server

%install
%define limax3 %{buildroot}%{python_sitelib}/Lima/xspress3
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

./install.sh --install-prefix=%{limax3} --install-python-prefix=%{limax3}/python xspress3 hdf5 python pytango-server

cp --preserve=links camera/xspress3/sdk/libs/linux.x86_64/* %{limax3}/lib64/

mkdir -p %{buildroot}%{_bindir}
cp %{_sourcedir}/Lima-xspress3-LimaCCDs %{buildroot}%{_bindir}/LimaCCDs

cp camera/xspress3/scripts/createdevice.py %{limax3}/
chmod 755 %{limax3}/createdevice.py

mkdir -p %{limax3}/test
cp -r camera/xspress3/test/*.py %{limax3}/test/
cp -r camera/xspress3/test/*.cpp %{limax3}/test/

# BPM plugin is not python2.7 compat :( 
sed -i -e "s|f'|'|" %{limax3}/python/Lima/Server/plugins/Bpm.py

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%{python_sitelib}/Lima/xspress3/bin*
%{python_sitelib}/Lima/xspress3/include*
%{python_sitelib}/Lima/xspress3/lib64*
%{python_sitelib}/Lima/xspress3/python*
%{python_sitelib}/Lima/xspress3/test/*
%{python_sitelib}/Lima/xspress3/createdevice.py
%exclude %{python_sitelib}/Lima/xspress3/createdevice.pyc
%exclude %{python_sitelib}/Lima/xspress3/createdevice.pyo
%{_bindir}/LimaCCDs

%post
export TANGO_HOST=localhost:10000
%{python_sitelib}/Lima/xspress3/createdevice.py -n xspress3

%changelog
* Sat Oct 24 2020 Stu<stu@quantumdetectors.com>
- Migrate to lima 1.9, fix threading
* Wed Jun 19 2019 Liam<liam@quantumdetectors.com>
- Update libraries and headers for RevE
* Fri Feb 15 2019 Stu<stu@quantumdetectors.com>
– SDK Bump, X4 Support
* Fri Jun 30 2017 Stu<stu@quantumdetectors.com>
– Multicard support, updated test scripts
* Thu Jun 08 2017 Stu<stu@quantumdetectors.com>
– Remove patch, build from git, sync with qd master, install tests and helper scripts
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
