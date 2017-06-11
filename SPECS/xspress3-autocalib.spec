Name:           xspress3-autocalib
Version:        1
Release:        1%{?dist}
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


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/*
%{_sysconfdir}/*


%changelog
* Mon Jun 12 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
