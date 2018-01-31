#
# spec file for package python-pyepics
#
# Copyright (c) 2018 xspress3.
#

Name:           python-pyepics
Version:        3.3.1
Release:        0
Url:            http://pyepics.github.io/pyepics/
Summary:        Epics Channel Access for Python
License:        Epics Open License (FIXME:No SPDX)
Group:          Development/Languages/Python
Source:         https://files.pythonhosted.org/packages/source/p/pyepics/pyepics-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  epics-base
Requires:       epics-base

%description
Python Interface to the Epics Channel Access protocol
of the Epics control system.   PyEpics provides 3 layers of access to
Channel Access (CA):
  1. a light wrapping of the CA C library calls, using ctypes. This
     provides a procedural CA library in which the user is expected
     to manage Channel IDs. It is mostly provided as a foundation
     upon which higher-level access is built.
  2. PV() (Process Variable) objects, which represent the basic object
     in CA, allowing one to keep a persistent connection to a remote
     Process Variable.
  3. A simple set of functions caget(), caput() and so on to mimic
     the CA command-line tools and give the simplest access to CA.

In addition, the library includes convenience classes to define
Devices -- collections of PVs that might represent an Epics Record
or physical device (say, a camera, amplifier, or power supply), and
to help write GUIs for CA.

%prep
%setup -q -n pyepics-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%exclude %{python_sitelib}/epics/clibs/linux64
%exclude %{python_sitelib}/epics/clibs/linux32
%exclude %{python_sitelib}/epics/clibs/win32
%exclude %{python_sitelib}/epics/clibs/win64
%exclude %{python_sitelib}/epics/clibs/darwin64

%changelog
