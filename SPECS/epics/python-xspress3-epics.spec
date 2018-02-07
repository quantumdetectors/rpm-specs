Name:           python-xspress3-epics
Version:        1.0.0
Release:        0
Url:            https://github.com/quantumdetectors/python-xspress3-epics
Summary:        Python Xspress 3 EPICS Classes
License:        GPL
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
Requires:       epics-base
Requires:       python-pyepics
Requires:       h5py
Requires:       numpy

%description
Classes to control an Xspress 3 EPICS device and parse outputted hdf5 files

%prep
%setup -T -c -n %{name}-%{version}
git clone https://github.com/quantumdetectors/python-xspress3-epics .

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

mkdir -p %{buildroot}%{_bindir}
cp scripts/hdf2csv.py %{buildroot}%{_bindir}/hdf2csv

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/*

%changelog
* Tue Feb 06 2018 Stu<stu@quantumdetectors.com>
– Initial rpm build
