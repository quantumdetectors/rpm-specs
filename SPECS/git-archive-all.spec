Name:           git-archive-all
Version:        1.16.4
Release:        0
Url:            https://github.com/Kentzo/git-archive-all
Summary:        Archive git repository with its submodules
License:        MIT
Group:          Development/Languages/Python
Source:         https://files.pythonhosted.org/packages/source/g/git-archive-all/git-archive-all-%{version}.tar.gz
Packager:       quantumdetectors.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildArch:      noarch

%description
Archive repository with all its submodules.

::

    git-archive-all [-v] [--prefix PREFIX] [--no-exclude] [--force-submodules] [--extra] [--dry-run] OUTPUT_FILE

    Options:

      --version             Show program's version number and exit.

      -h, --help            Show this help message and exit.

      -v, --verbose         Enable verbose mode.

      --prefix=PREFIX       Prepend PREFIX to each filename in the archive. OUTPUT_FILE name is used by default to avoid tarbomb. You can set it to '' in order to explicitly request tarbomb.

      --no-exclude          Don't read .gitattributes files for patterns containing export-ignore attributes.

      --force-submodules    Force a `git submodule init && git submodule update` at each level before iterating submodules

      --extra               Include extra files to the resulting archive.

      --dry-run             Don't actually archive anything, just show what would be done.

Support
-------
If functional you need is missing but you're ready to pay for it, feel free to `contact me <mailto:kulakov.ilya@gmail.com?subject=git-archive-all>`_. If not, create an issue anyway, I'll take a look as soon as I can.


%prep
%setup -q -n git-archive-all-%{version}

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