Name:           xspress3-autocalib
Version:        1
Release:        12%{?dist}
Url:            https://gitlab.com/xspress3/xspress3-autocalib
Summary:        Xspress 3 Autocalibration Suite
License:        GPL
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:	git
BuildRequires:  python
Requires:       python
Requires:		python-gevent-websocket
Requires:       numpy
Requires:		scipy
Requires:       glibc-devel
Requires:       fping
AutoReqProv:    no

%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")


%description
Xspress 3 web based autocalibration suite


%prep
%setup -T -c -n %{name}-%{version}
git clone %{url}.git
cd xspress3-autocalib
git checkout qd-pkg
cd ../


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

install -d %{buildroot}%{python_sitelib}
install -d %{buildroot}%{_bindir}
install -m 777 -d %{buildroot}%{_sysconfdir}/xspress3
install -m 777 -d %{buildroot}%{_sysconfdir}/xspress3/calibration

chmod 755 xspress3-autocalib/remote.py

mv xspress3-autocalib %{buildroot}%{python_sitelib}/
cd %{buildroot}%{python_sitelib}/xspress3-autocalib
ln -sr remote.py ../../../../..%{_bindir}/xspress3-autocalib.py

ln -sr bin/xspress3.server.6 ../../../../..%{_bindir}/xspress3.server
ln -sr bin/imgd.6 ../../../../..%{_bindir}/imgd


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/*
%{_sysconfdir}/*


%changelog
* Wed Sep 16 2020 Liam<liam@quantumdetectors.com>
- Update to library and X3 server to support X3X fan control hardware
* Thu Jan 16 2020 Richard<richard@quantumdetectors.com>
- Versioning and automatic copyright update.
* Wed Jun 19 2019 Liam<liam@quantumdetectors.com>
- Update binaries, updated libraries for picozed Rev-E
* Thu Mar 21 2019 Stu<stu@quantumdetectors.com>
- Update binaries, minor fixes
* Tue Jan 22 2019 Stu<stu@quantumdetectors.com>
- Add X4
* Wed Apr 25 2018 Stu<stu@quantumdetectors.com>
- Add test suite, add logging
* Mon Mar 12 2018 Stu<stu@quantumdetectors.com>
- Link x3.server and imgd into path, bug in meas gain
* Wed Feb 28 2018 Stu<stu@quantumdetectors.com>
- New ROI peak fitting, cmd line args, non blocking mca, various minor fixes
* Thu Nov 02 2017 Stu<stu@quantumdetectors.com>
– Various multicard fixes and updates, new measure reset tail
* Tue Oct 03 2017 Stu<stu@quantumdetectors.com>
– More multicard support, autorange individual channels
* Fri Jun 30 2017 Stu<stu@quantumdetectors.com>
– Multicard support
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
