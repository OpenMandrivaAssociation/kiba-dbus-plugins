%define svn	722
%define release 0.%{svn}.2

%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"
%define python_compile     python -c "import compileall; compileall.compile_dir('.')"

Name:		kiba-dbus-plugins
Version:	0.1
Release:	%{release}
Summary:	D-Bus plugins for Kiba-Dock
Group:		System/X11
URL:		http://www.kiba-dock.org/
Source0:	%{name}-%{svn}.tar.lzma
patch0:		kiba-dbus-plugins-722.kiba-doc-version.patch
License:	GPLv2+
BuildArch:	noarch
BuildRequires:	kiba-dock-devel = %{version}
BuildRequires:	intltool
BuildRequires:	dbus-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	python2-devel

Requires:	kiba-dock

%description
D-Bus plugins for Kiba-Dock.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .kiba-doc-version

%build
export PYTHON=%{__python2}

sh autogen.sh -V
%configure
%make

%install
%makeinstall_std
%find_lang kiba-dbus-plugin

pushd scripts
%python_compile_opt
%python_compile
# Some of the scripts are never installed, apparently, so can't just
# use * - AdamW 2008/03
for i in mail weather signal battery feeder; do \
install -m 0644 kiba-$i.pyc kiba-$i.pyo %{buildroot}%{_datadir}/kiba-dock/dbus_scripts; \
done
popd

%files -f kiba-dbus-plugin.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog
%{_datadir}/kiba-dock/config_schemas/plugins/python_scripts.xml
%{_datadir}/kiba-dock/dbus_scripts
%{_datadir}/kiba-dock/icons/kiba-battery
%{_datadir}/kiba-dock/icons/kiba-feeder
%{_datadir}/kiba-dock/icons/kiba-mail
%{_datadir}/kiba-dock/icons/kiba-signal
%{_datadir}/kiba-dock/icons/kiba-weather
