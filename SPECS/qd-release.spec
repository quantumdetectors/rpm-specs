Name:           qd-release
Version:        1.0.0
Release:        1%{?dist}
Summary:        QD repository file and GPG Key
Packager:       quantumdetectors.com
License:        GPL
URL:            https://github.com/quantumdetectors/rpm-specs
Source0:        https://github.com/quantumdetectors/rpm-specs/tree/master/SOURCES/qd-release-1.0.0.tar.gz

%description
Installs Quantum Detectors EL7 Repository


%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/
cp -p qd.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/
cp -p RPM-GPG-KEY-qd $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/qd.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-qd


%post
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-qd


%changelog
* Tue Jul 31 2018 Stu Fisher <stu@quantumdetectors.com> 1.0.0
- QD repo and GPG file
