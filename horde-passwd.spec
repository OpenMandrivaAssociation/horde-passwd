%define	module	passwd

Name:		horde-%{module}
Version:	3.1.3
Release:	4
Summary:	The Horde password management application
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}/
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Source2:	%{module}-horde.conf.bz2
#Patch0:		%{module}-h3-3.1.2-script-shellbang.patch
Requires:	horde >= 3.3.5
Requires:	php-soap
BuildArch:	noarch

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
#%patch0 -p 1

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Deny from all
    Order allow,deny
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
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
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Sun Aug 29 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.1.3-2mdv2011.0
+ Revision: 574243
- added requires php-soap

* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.1.3-1mdv2011.0
+ Revision: 567526
- Updated to version 3.1.3
- added version 3.1.3 source file

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.1.2-2mdv2011.0
+ Revision: 565290
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.2-1mdv2010.1
+ Revision: 493341
- new version
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.1-2mdv2010.0
+ Revision: 445914
- don't forget call webapps post-installation macros to load module configuration

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.1-1mdv2010.0
+ Revision: 445893
- new version
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 3.1-2mdv2010.0
+ Revision: 437886
- rebuild

* Fri Mar 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-1mdv2009.1
+ Revision: 359193
- new version

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 3.0.1-3mdv2009.0
+ Revision: 240833
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Sep 06 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.0.1-1mdv2008.0
+ Revision: 81205
- new version


* Mon Jan 01 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-4mdv2007.0
+ Revision: 103022
- don't forget theme

  + Andreas Hasenack <andreas@mandriva.com>
    - Import horde-passwd

* Sat Aug 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-3mdv2007.0
- Rebuild

* Wed Jan 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-2mdk
- fix automatic dependencies

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-1mdk
- new version
- rediff patch 0
- %%mkrel

* Fri Jul 01 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-1mdk 
- new version
- better fix encodings
- spec cleanup
- fix script shellbang

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.2.1-4mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-3mdk 
- top-level is now /var/www/horde/passwd
- config is now in /etc/horde/passwd
- other non-accessible files are now in /usr/share/horde/passwd
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Wed Sep 15 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-2mdk 
- fixed icon name in horde config

* Sun Sep 05 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-1mdk 
- new release
- correct description

* Tue Jul 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2-5mdk 
- apache config file in /etc/httpd/webapps.d

* Sat Jul 03 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2-4mdk 
- really remove useless provide

* Sun May 02 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2-3mdk
- renamed to horde-passwd
- pluggable horde configuration
- standard perms for /etc/httpd/conf.d/%%{order}_horde-passwd.conf
- don't provide useless ADVXpackage virtual package

* Wed Apr 07 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2-1mdk
- first distinct package

