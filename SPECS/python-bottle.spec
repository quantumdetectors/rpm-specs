Name:           python-bottle
Version:        0.12.13
Release:        0
Url:            http://bottlepy.org/
Summary:        Fast and simple WSGI-framework for small web-applications
License:        MIT
Group:          Development/Languages/Python
Source:         https://files.pythonhosted.org/packages/source/b/bottle/bottle-%{version}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildArch:      noarch

%description
Bottle is a fast and simple micro-framework for small web applications. It
offers request dispatching (Routes) with url parameter support, templates,
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and
template engines - all in a single file and with no dependencies other than the
Python Standard Library.

Homepage and documentation: http://bottlepy.org/

Copyright (c) 2016, Marcel Hellkamp.
License: MIT (see LICENSE for details)

%prep
%setup -q -n bottle-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/lib/python2.7/site-packages/*
%{_bindir}/*

%changelog
* Fri Jun 02 2017 Stu<stu@quantumdetectors.com>
– Initial rpm build
