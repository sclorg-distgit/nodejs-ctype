%{?scl:%scl_package nodejs-ctype}
%{!?scl:%global pkg_name %{name}}

%{?nodejs_find_provides_and_requires}

%global commit 3aae5f7aa45906cfcb283817cfb6fcb15360391d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           %{?scl_prefix}nodejs-ctype
Version:        0.5.3
Release:        3.1%{?dist}
Summary:        Read and write binary structures and data types with Node.js
BuildArch:      noarch
ExclusiveArch: %{nodejs_arches} noarch

Group:          System Environment/Libraries
License:        MIT
URL:            https://github.com/rmustacc/node-ctype
Source0:        http://registry.npmjs.org/ctype/-/ctype-%{version}.tgz
#grab the tests from github
Source1:        https://github.com/rmustacc/node-ctype/archive/%{commit}/%{pkg_name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)

# fedora-specific patch to have README indicate proper directions for reading
# the man page from the system path
Patch1:         nodejs-ctype-README.patch

BuildRequires:  %{?scl_prefix}nodejs-devel

%description
Node-CType is a way to read and write binary data in a structured and easy to 
use format. Its name comes from the C header file.

There are two APIs that you can use, depending on what abstraction you'd like.
The low level API lets you read and write individual integers and floats from
buffers. The higher level API lets you read and write structures of these.

%prep
%setup -q -n package -a1
%patch1 -p1

#move tests into regular directory
mv node-ctype-%{commit}/tst .
rm -rf node-ctype-%{commit}

%build
#nothing to do

%install
rm -rf %buildroot

mkdir -p %{buildroot}%{nodejs_sitelib}/ctype
cp -pr package.json ctf.js ctio.js ctype.js %{buildroot}%{nodejs_sitelib}/ctype

mkdir -p %{buildroot}%{_mandir}/man3
cp -pr man/man3ctype/ctio.3ctype %{buildroot}%{_mandir}/man3/ctio.3

%nodejs_symlink_deps

%check
pushd tst
for dir in ctf ctio/* ctype; do
    pushd $dir
    for f in *.js; do
	%{?scl:scl enable %{scl} "}
        %{__nodejs} $f
	%{?scl:"}
    done
    popd
done
popd

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/ctype
%{_mandir}/man3/ctio.3.*
%doc CHANGELOG LICENSE README README.old

%changelog
* Wed Dec 11 2013 Tomas Hrcka <thrcka@redhat.com> - 0.5.3-3.1
- enable scl support

* Sun Jun 23 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.5.3-3
- restrict to compatible arches

* Fri Jun 21 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.5.3-2
- fix spelling in description

* Thu Jun 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.5.3-1
- initial package
