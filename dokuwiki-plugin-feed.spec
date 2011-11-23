%define		plugin		feed
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki plugin to generate feeds for other plugins
Summary(pl.UTF-8):	Wtyczka feed dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	20100107
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://cloud.github.com/downloads/dokufreaks/plugin-feed/plugin-feed.tgz
# Source0-md5:	ffb84ef4d2fc623648c6d4a77a4e4c42
URL:		http://www.dokuwiki.org/plugin:feed
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20091225
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	php-session
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
mv %{plugin}/* .

version=$(cat VERSION)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
#	exit 1
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
%{plugindir}/images
