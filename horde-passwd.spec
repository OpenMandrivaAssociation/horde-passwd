%define	module	passwd
%define	name	horde-%{module}
%define	version	3.1
%define	release	%mkrel 2

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde password management application
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}/
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Source2:	%{module}-horde.conf.bz2
Patch0:		%{module}-h3-3.1-script-shellbang.patch
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Passwd is the Horde password changing application. While it has been released
and is in production use at many sites, it is also under heavy development in
an effort to expand and improve the module.

Right now, Passwd provides fairly complete support for changing passwords via
poppassd, ldap, unix expect scripts, the unix smbpasswd command for smb/cifs
password support, servuftp, vmailmgr, vpopmail, and sql passwords.

Passwd is part of a suite of account management modules for Horde consisting of
Accounts, Forwards, Passwd, and Vacation.

%prep
%setup -q -n %{module}-h3-%{version}
%patch0 -p 1

%build

%install
rm -rf %{buildroot}

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_var}/www/horde/%{module}
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
install -d -m 755 %{buildroot}%{_sysconfdir}/horde
cp -pR *.php %{buildroot}%{_var}/www/horde/%{module}
cp -pR themes %{buildroot}%{_var}/www/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

# use symlinks to recreate original structure
pushd %{buildroot}%{_var}/www/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
ln -s ../../../..%{_datadir}/horde/%{module}/lib .
ln -s ../../../..%{_datadir}/horde/%{module}/locale .
ln -s ../../../..%{_datadir}/horde/%{module}/templates .
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_var}/www/horde/%{module}


