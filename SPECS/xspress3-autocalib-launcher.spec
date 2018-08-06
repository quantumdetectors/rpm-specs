Name:           xspress3-autocalib-launcher
Version:        1.0.0
Release:        1%{?dist}
Summary:        Xspress 3 Calibration X11 Launcher
Packager:       quantumdetectors.com
License:        GPL
URL:            https://github.com/quantumdetectors/rpm-specs
Source0:        https://github.com/quantumdetectors/rpm-specs/tree/master/SOURCES/xspress3-autocalib-launcher-1.0.0.tar.gz
Requires:       xspress3-autocalib
Requires:       firefox

%description
Installs Xspress 3 Calibration X11 Launcher


%prep
%setup -q


%build


%install
install -d %{buildroot}%{_datadir}/applications
install xspress3.desktop %{buildroot}%{_datadir}/applications/
install x3_logo.png %{buildroot}%{_datadir}/applications/

install -d %{buildroot}%{_bindir}/
install x3-calib-launcher.sh %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*


%changelog
* Mon Aug 06 2018 Stu Fisher <stu@quantumdetectors.com> 1.0.0
- X3 Calibration Launcher
