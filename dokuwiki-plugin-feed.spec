%define		plugin		feed
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki plugin to generate feeds for other plugins
Summary(pl.UTF-8):	Wtyczka feed dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	20100107
Release:	7
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/dokufreaks/plugin-feed/tarball/master#/%{name}-%{version}.tgz
# Source0-md5:	0d3c979368896d3bb844f5a33829eece
URL:		http://www.dokuwiki.org/plugin:feed
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20091225
Requires:	php(core) >= %{php_min_version}
Requires:	php(session)
Requires:	php-date
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

# no pear deps
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-someext

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
The Feed Plugin is a helper plugin that generates RSS and Atom feeds
for other plugins.

%description -l pl.UTF-8
Wtyczka dla DokuWiki

%prep
%setup -qc
mv dokufreaks-plugin-feed-*/* .

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{COPYING,README,VERSION}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/images
