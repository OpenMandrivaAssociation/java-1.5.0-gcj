
# with => disabled by default
# without => enabled by default

%bcond_with bootstrap
%bcond_with             plugin
%bcond_with             fastjar

%define origin		gcj
%define gccsuffix	%nil
%define gccsoversion	13
%define priority	1500
%define	javaver		1.5.0
%define buildver	0
# the version-release string for the gcj rpms we require
%define gccver		%(gcc%{gccsuffix} -dumpversion 2>/dev/null || echo 0)
%define jgcver		1.0.80
%define jar		%{_bindir}/gjar%{gccsuffix}

%define	sdklnk		java-%{javaver}-%{origin}
%define	jrelnk		jre-%{javaver}-%{origin}
%define	sdkdir		%{name}-%{version}
%define	jredir		%{sdkdir}/jre
%define sdkbindir	%{_jvmdir}/%{sdklnk}/bin
%define jrebindir	%{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}
%define jafver          1.1

%if %with plugin
%define plugindir       %{_libdir}/mozilla/plugins
%endif

Name:		java-%{javaver}-%{origin}
Version:	%{javaver}.%{buildver}
Release:	23
Summary:	JPackage runtime scripts for GCJ

Group:		Development/Java
License:	GPL
URL:		http://sources.redhat.com/rhug/java-gcj-compat.html
Source0:	ftp://sources.redhat.com/pub/rhug/java-gcj-compat-%{jgcver}.tar.gz
Patch0:		java-1.4.2-gcj-compat-aot-compile-rpm.patch
# Add only .so linked to correct libgcj_bc.so during rebuild-gcj-db,
# to avoid gij failure with non-rebuilt packages
Patch1:		java-1.5.0-gcj-ensure-soname-compat.patch
# Fix invalid python code causing aotcompile to explode
Patch5:		java-gcj-compat-1.0.80-fix-aotcompile.patch

# required to calculate gcj binary's path to encode in aotcompile.py
# and rebuild-gcj-db
BuildRequires: gcc%{gccsuffix}-java eclipse-ecj
BuildRequires: libgcj%{gccsoversion}-src
# required for cacerts generation
BuildRequires: openssl
BuildRequires: gcj-tools
BuildRequires: python-devel
BuildRequires: java-rpmbuild
%if %without bootstrap
BuildRequires: java-1.7.0-openjdk-devel
%endif
BuildArch: noarch

# required for tools and libgcj.jar
Requires:         %{mklibname gcj %{gccsoversion}} >= %{gccver}
# XXX: this might not be the right place for it, but it needs to be somewhere
Requires:         bouncycastle
# required for directory structures
Requires:         jpackage-utils >= 1.7.3
Requires(post):	jpackage-utils
Requires(postun): jpackage-utils

Requires(post):	update-alternatives >= 1.8.6
Requires(postun):	update-alternatives

# standard JPackage base provides
Provides: jre-%{javaver}-%{origin} = %{version}-%{release}
Provides: jre-%{origin} = %{version}-%{release}
Provides: jre-%{javaver} = %{version}-%{release}
Provides: java-%{javaver} = %{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{version}-%{release}
Provides: java = %{javaver}
# libgcj provides, translated to JPackage provides
Provides: jaas = %{version}-%{release}
Provides: jce = %{version}-%{release}
Provides: jdbc-stdext = %{version}-%{release}
Provides: jdbc-stdext = 3.0
Provides: jndi = %{version}-%{release}
Provides: jndi-cos = %{version}-%{release}
Provides: jndi-dns = %{version}-%{release}
Provides: jndi-ldap = %{version}-%{release}
Provides: jndi-rmi = %{version}-%{release}
Provides: jsse = %{version}-%{release}
Provides: java-sasl = %{version}-%{release}
Provides: jaxp_parser_impl = %{version}-%{release}
# java-gcj-compat base provides
# (anssi) added release
Provides: java-gcj-compat = %{jgcver}-%{release}
Provides: java-1.4.2-gcj-compat = 1.4.2.0-41
Provides: java-1.5.0-gcj-compat = 1.5.0

# Mandriva added:
Provides: jaxp_transform_impl = %{version}-%{release}
Provides: jta = %{version}-%{release}

Obsoletes: java-1.4.2-gcj-compat < 1.4.2.0-41
Obsoletes: gnu-crypto < 2.1.0-7
Obsoletes: gnu-crypto-der < 2.1.0-7
Obsoletes: gnu-crypto-auth-jdk1.4 < 2.1.0-7
Obsoletes: gnu-crypto-jce-jdk1.4 < 2.1.0-7
Obsoletes: gnu-crypto-sasl-jdk1.4 < 2.1.0-7
Obsoletes: jessie <= 1.0.1-7
Obsoletes: classpathx-jaf <= 1.0-16
Provides:  jaf = 0:%{jafver}
Provides:  activation = 0:%{jafver}
Obsoletes: gnujaf <= 0:1.0-0.rc1.1jp

%description
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible runtime environment with GCJ.

%package devel
Summary:	JPackage development scripts for GCJ
Group:		Development/Java

# require base package
Requires:         %{name} = %{version}-%{release}
# require python for aot-compile
Requires:         python
# post requires alternatives to install tool alternatives
Requires(post):   update-alternatives >= 1.8.6
# postun requires alternatives to uninstall tool alternatives
Requires(postun): update-alternatives
%py_requires -d
Requires:      gcc%{gccsuffix}-java

%if %with fastjar
Requires: fastjar
%endif

%if %without bootstrap
# For javadoc symlink
Requires: java-1.7.0-openjdk-devel
%endif

# standard JPackage devel provides
Provides: java-sdk-%{javaver}-%{origin} = %{version}
Provides: java-sdk-%{javaver} = %{version}
Provides: java-sdk-%{origin} = %{version}
Provides: java-sdk = %{javaver}
Provides: java-%{javaver}-devel = %{version}
Provides: java-devel-%{origin} = %{version}
Provides: java-devel = %{javaver}
# java-gcj-compat devel provides
# (anssi) added release
Provides: java-gcj-compat-devel = %{jgcver}-%{release}
Provides: java-1.4.2-gcj-compat-devel = 1.4.2.0-41

Obsoletes: java-1.4.2-gcj-compat-devel < 1.4.2.0-41

%if %without bootstrap
Requires:	eclipse-ecj
%else
Requires:	ecj-bootstrap
%endif

%description devel
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible development environment with
GCJ.

%package src
Summary:	Source files for libgcj
Group:		Development/Java

Requires:       %{name} = %{version}-%{release}
Requires:       libgcj%{gccsoversion}-src >= %{gccver}

# java-gcj-compat src provides
Provides: java-1.4.2-gcj-compat-src = 1.4.2.0-41
Obsoletes: java-1.4.2-gcj-compat-src < 1.4.2.0-41

%description src
This package installs a versionless src.zip symlink that points to a
specific version of the libgcj sources.

%if %without bootstrap
%package javadoc
Summary:       API documentation for libgcj
Group:         Development/Java

# require base package
# (walluck): why? docs should not require a JVM
#Requires: %{name} = %{version}-%{release}

# standard JPackage javadoc provides
Provides:	java-javadoc = %{version}-%{release}
Provides:	java-%{javaver}-javadoc = %{version}-%{release}
# java-gcj-compat javadoc provides
Provides:	java-1.4.2-gcj-compat-javadoc = 1.4.2.0-41

Obsoletes:	java-1.4.2-gcj-compat-javadoc < 1.4.2.0-41
Obsoletes:	gnu-crypto-javadoc < 2.1.0-7
Obsoletes:	classpathx-jaf-javadoc <= 1.0-16
Provides:	jaf-javadoc = 0:%{jafver}
Provides:	activation-javadoc = 0:%{jafver}
Obsoletes:	gnujaf-javadoc <= 0:1.0-0.rc1.1jpp

%description javadoc
This package installs Javadoc API documentation for libgcj.
%endif

%if %with plugin
%package plugin
Summary:       Web browser plugin that handles applets
Group:         Development/Java

# require base package
Requires:         %{name} = %{version}-%{release}
# require libgcj for plugin shared object
Requires:	  %{_lib}gcj%{gccsoversion} >= %{gccver}
# post requires alternatives to install plugin alternative
Requires(post):   update-alternatives
# postun requires alternatives to uninstall plugin alternative
Requires(postun): update-alternatives

# standard JPackage plugin provides
Provides: java-plugin = %{javaver}
Provides: java-%{javaver}-plugin = %{version}
# java-gcj-compat plugin provides
Provides: java-1.4.2-gcj-compat-plugin = 1.4.2.0-41
Obsoletes: java-1.4.2-gcj-compat-plugin < 1.4.2.0-41

%description plugin
This package installs gcjwebplugin, a Mozilla plugin for applets.
%endif

%prep
%setup -q -n java-gcj-compat-%{jgcver}
%patch0 -p1
%patch1 -p1
%patch5 -p1
# (anssi) for patch4:
GCJ_BC_MAJOR=$(objdump -p $(gcj%gccsuffix -print-file-name=libgcj_bc.so) | \
	grep SONAME | sed -ne 's,^.*libgcj_bc.so.\([^ ]\).*$,\1,p')
perl -pi -e "s,\@GCJ_BC_MAJOR\@,$GCJ_BC_MAJOR," rebuild-gcj-db.in

# (anssi)
perl -pi -e 's,gkeytool ,gkeytool%{gccsuffix} ,' generate-cacerts.pl
perl -pi -e 's,gjarsigner ,gjarsigner%{gccsuffix} ,' Makefile.am
perl -pi -e 's,gappletviewer ,gappletviewer%{gccsuffix} ,' Makefile.am

%if %with fastjar
# (anssi) GCC4.2 contains gjar instead of fastjar
# we use external fastjar due to upstream classpath bug anyway:
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=32516
perl -pi -e 's,fastjar\$\(gcc_suffix\),fastjar,' Makefile.am
%else
perl -pi -e 's,fastjar\$\(gcc_suffix\),gjar\$\(gcc_suffix\),' Makefile.am
%endif
aclocal
automake
autoconf

%build
export CLASSPATH=
export JAR=%jar
%configure2_5x --disable-symlinks --with-arch-directory=%{_arch} \
  --with-os-directory=linux \
  --with-security-directory=%{_sysconfdir}/java/security/security.d \
  --with-gcc-suffix=%{gccsuffix} --with-origin-name=gcj

%{__make}

# the python compiler encodes the source file's timestamp in the .pyc
# and .pyo headers.  since aotcompile.py is generated by configure,
# its timestamp will differ from build to build.  this causes multilib
# conflicts.  we work around this by setting aotcompile.py's timestamp
# to equal aotcompile.py.in's timestamp. (205216)
touch --reference=aotcompile.py.in aotcompile.py

%install
%makeinstall_std

# extensions handling
install -dm 755 $RPM_BUILD_ROOT%{jvmjardir}
pushd $RPM_BUILD_ROOT%{jvmjardir}
  for jarname in jaas jce jdbc-stdext jndi jndi-cos jndi-dns \
    jndi-ldap jndi-rmi jsse sasl jta; do
    ln -s %{_jvmdir}/%{jredir}/lib/$jarname.jar $jarname-%{version}.jar
  done
  for jar in *-%{version}.jar ; do
    ln -sf ${jar} $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
    ln -sf ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
  done
popd

# security directory and provider list
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
ln -sf %{_prefix}/lib/security/classpath.security $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/java.security

%if 0
# (anssi) we have those in jpackage-utils

# default security providers, provided by libgcj
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d
for provider in \
  1000-gnu.java.security.provider.Gnu \
  1001-gnu.javax.crypto.jce.GnuCrypto \
  1002-gnu.javax.crypto.jce.GnuSasl \
  1003-gnu.javax.net.ssl.provider.Jessie \
  1004-gnu.javax.security.auth.callback.GnuCallbacks
do
  cat > $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d/$provider << EOF
# This file's contents are ignored.  It's name, of the form
# <priority>-<provider name>, is used by rebuild-security-providers to
# rebuild the list of security providers in libgcj's
# classpath.security file.
EOF
done

%endif

# cacerts
%{__perl} generate-cacerts.pl
install -m 644 cacerts $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security

# versionless symlinks
pushd $RPM_BUILD_ROOT%{_jvmdir}
   ln -s %{jredir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

pushd $RPM_BUILD_ROOT%{_jvmjardir}
   ln -s %{sdkdir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

# classmap database directory
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/gcj

%if %without bootstrap
# build and install API documentation
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
pushd $RPM_BUILD_ROOT%{_javadocdir}
  ln -s %{name} java
popd
mkdir docsbuild
pushd docsbuild
  GIJ_VERSION=$(gij%{gccsuffix} --version | head -n 2 | tail -n 1 \
    | awk '{ print $5 }')
  %jar xvf /usr/share/java/src-$GIJ_VERSION.zip
  rm -rf gnu
  find ./ -name \*.java | xargs -n 1 dirname | sort | uniq \
    | sed -e "s/\.\///" | sed -e "s/\//\./" \
    | sed -e "s/\//\./" | sed -e "s/\//\./" \
    | sed -e "s/\//\./" | sed -e "s/\//\./" \
    | xargs -n 1 javadoc \
    -d $RPM_BUILD_ROOT%{_javadocdir}/%{name} \
    -encoding UTF-8 -breakiterator \
    -linksource -splitindex -doctitle "GNU libgcj $GIJ_VERSION" \
    -windowtitle "GNU libgcj $GIJ_VERSION Documentation" || \
      [ 0$(find $RPM_BUILD_ROOT%{_javadocdir}/%{name} | wc -l) -gt 3800 ]
# (anssi) if over 3800 docfiles are created, consider it a success enough
popd
%endif

%ifarch x86_64
cd %{buildroot}%{_jvmdir}/%{jredir}/lib && \
%{__ln_s} %{_arch} amd64
%endif

# install operating system include directory
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/include/linux

# install libjvm.so directories
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{_arch}/client
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{_arch}/server

# install native_threads directory
%{__mkdir_p} %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/native_threads

# install tools.jar directory
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/lib

# (anssi) Link at build-time, not runtime
# src
ln -s %{_javadir}/src-%{gccver}.zip %{buildroot}%{_jvmdir}/%{sdkdir}/src.zip
# %name
ln -s %{_javadir}/libgcj-%{gccver}.jar %{buildroot}%{_jvmdir}/%{sdkdir}/jre/lib/rt.jar
ln -s %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libjawt.so %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/libjawt.so
ln -s %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libjvm.so %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/client/libjvm.so
ln -s %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libjvm.so %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/server/libjvm.so
ln -s %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libjvm.so %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/native_threads/libhpi.so
# devel
ln -s %{_javadir}/libgcj-tools-%{gccver}.jar %{buildroot}%{_jvmdir}/%{sdkdir}/lib/tools.jar
ln -s $(gcj%{gccsuffix} -print-file-name=include/jawt.h) %{buildroot}%{_jvmdir}/%{sdkdir}/include/jawt.h
ln -s $(gcj%{gccsuffix} -print-file-name=include/jni.h) %{buildroot}%{_jvmdir}/%{sdkdir}/include/jni.h
ln -s $(gcj%{gccsuffix} -print-file-name=include/jawt_md.h) %{buildroot}%{_jvmdir}/%{sdkdir}/include/linux/jawt_md.h
ln -s $(gcj%{gccsuffix} -print-file-name=include/jni_md.h) %{buildroot}%{_jvmdir}/%{sdkdir}/include/linux/jni_md.h

# (anssi) needed by jni_md.h (since gcj4.2 or gcj4.3):
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/include/linux/gcj
ln -s $(gcj%{gccsuffix} -print-file-name=include/gcj/libgcj-config.h) %{buildroot}%{_jvmdir}/%{sdkdir}/include/linux/gcj/libgcj-config.h

# (anssi) Normally there is no need to do -I$JAVA_HOME/include/linux when
# building with gcj. Therefore some software (OOo) may assume it is not
# needed, thus these compatibility symlinks.
ln -s linux/gcj %{buildroot}%{_jvmdir}/%{sdkdir}/include/gcj
ln -s linux/jni_md.h %{buildroot}%{_jvmdir}/%{sdkdir}/include/jni_md.h
ln -s linux/jawt_md.h %{buildroot}%{_jvmdir}/%{sdkdir}/include/jawt_md.h

pushd $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/jre/lib
  for jarname in jaas jce jdbc-stdext jndi jndi-cos jndi-dns \
    jndi-ldap jndi-rmi jsse sasl jta
  do
    ln -s rt.jar $jarname.jar
  done
popd

# (anssi)
install -dm 755 %{buildroot}%{_sysconfdir}/rpm/macros.d
cat > %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros <<EOF
# The GCJ that should be used when building packages with %{name}-devel
%%gcj %{_bindir}/gcj%{gccsuffix}
# The GCJ dbtool that should be used
%%gcj_dbtool %{_bindir}/gcj-dbtool%{gccsuffix}
EOF

## FIXME - (temporarily?) using versions installed by gcc-java-4.6.0
rm -f %{buildroot}%{_bindir}/aot-compile
rm -f %{buildroot}%{_bindir}/rebuild-gcj-db

%post
%{_sbindir}/update-alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre          jre          %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre       jre_exports  %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/keytool      keytool      %{jrebindir}/keytool \
  --slave %{_bindir}/rmiregistry  rmiregistry  %{jrebindir}/rmiregistry

%{_sbindir}/update-alternatives \
  --install %{_jvmdir}/jre-%{origin} \
  jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} \
  jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

%{_sbindir}/update-alternatives \
  --install %{_jvmdir}/jre-%{javaver} \
  jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} \
  jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

# jaxp_parser_impl
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl %{_javadir}/libgcj-%{gccver}.jar 20

# jaxp_transform_impl
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/libgcj-%{gccver}.jar 20

if [ -x %{_bindir}/rebuild-security-providers ]
then
  %{_bindir}/rebuild-security-providers
fi
%{update_gcjdb}

# (anssi) I do not like the retarget-alternatives hacks with triggers
# "new gcc => rebuild" is easier

%postun
if [ $1 -eq 0 ]
then
  %{_sbindir}/update-alternatives --remove java %{jrebindir}/java
  %{_sbindir}/update-alternatives --remove jre_%{origin} %{_jvmdir}/%{jrelnk}
  %{_sbindir}/update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi
# (anssi) if gcc version changes, we want to remove the stale links:
if [ $1 -eq 0 ] || ! [ -e %{_javadir}/libgcj-%{gccver}.jar ]; then
  %{_sbindir}/update-alternatives --remove jaxp_parser_impl \
    %{_javadir}/libgcj-%{gccver}.jar
  %{_sbindir}/update-alternatives --remove jaxp_transform_impl \
    %{_javadir}/libgcj-%{gccver}.jar
fi

if [ -x %{_bindir}/rebuild-security-providers ]
then
  %{_bindir}/rebuild-security-providers
fi

%{clean_gcjdb}

%post devel

%{_sbindir}/update-alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java         java_sdk          %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java      java_sdk_exports  %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/javadoc      javadoc           %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah        javah             %{sdkbindir}/javah \
  --slave %{_bindir}/jar          jar               %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner    jarsigner         %{sdkbindir}/jarsigner \
  --slave %{_bindir}/appletviewer appletviewer      %{sdkbindir}/appletviewer \
  --slave %{_bindir}/rmic         rmic              %{sdkbindir}/rmic

%{_sbindir}/update-alternatives \
  --install %{_jvmdir}/java-%{origin} \
  java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} \
  java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

%{_sbindir}/update-alternatives \
  --install %{_jvmdir}/java-%{javaver} \
  java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} \
  java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

%postun devel
if [ $1 -eq 0 ]
then
  %{_sbindir}/update-alternatives --remove javac %{sdkbindir}/javac
  %{_sbindir}/update-alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdklnk}
  %{_sbindir}/update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

%if %with plugin
%post plugin
[ -d %{plugindir} ] || %{__mkdir_p} %{plugindir}
%{_sbindir}/update-alternatives --install %{plugindir}/libjavaplugin.so \
    libjavaplugin.so %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libgcjwebplugin.so %{priority}

%postun plugin
if [ $1 -eq 0 ] || ! [ -e  %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libgcjwebplugin.so ]; then
   %{_sbindir}/update-alternatives --remove libjavaplugin.so %{_libdir}/gcj-%{gccver}-%{gccsoversion}/libgcjwebplugin.so
fi
%endif

%files
%doc AUTHORS ChangeLog COPYING LICENSE README
%dir %{_jvmdir}/%{sdkdir}
%dir %{_jvmdir}/%{jredir}
%dir %{_jvmdir}/%{jredir}/bin
%dir %{_jvmdir}/%{jredir}/lib
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}/client
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}/server
%dir %{_jvmdir}/%{jredir}/lib/security
%dir %{jvmjardir}
%dir %{_libdir}/gcj
#%{_bindir}/rebuild-gcj-db
%{_jvmdir}/%{jredir}/bin/java
%{_jvmdir}/%{jredir}/bin/keytool
%{_jvmdir}/%{jredir}/bin/rmiregistry
%{_jvmdir}/%{jredir}/lib/security/cacerts
%{_jvmdir}/%{jredir}/lib/security/java.security
%{_jvmdir}/%{jredir}/lib/jaas.jar
%{_jvmdir}/%{jredir}/lib/jce.jar
%{_jvmdir}/%{jredir}/lib/jdbc-stdext.jar
%{_jvmdir}/%{jredir}/lib/jndi-cos.jar
%{_jvmdir}/%{jredir}/lib/jndi-dns.jar
%{_jvmdir}/%{jredir}/lib/jndi-ldap.jar
%{_jvmdir}/%{jredir}/lib/jndi-rmi.jar
%{_jvmdir}/%{jredir}/lib/jndi.jar
%{_jvmdir}/%{jredir}/lib/jta.jar
%{_jvmdir}/%{jredir}/lib/jsse.jar
%{_jvmdir}/%{jredir}/lib/sasl.jar
%ifarch x86_64
%{_jvmdir}/%{jredir}/lib/amd64
%endif
%{_jvmdir}/%{jrelnk}
%{jvmjardir}/jaas.jar
%{jvmjardir}/jaas-%{javaver}.jar
%{jvmjardir}/jaas-%{version}.jar
%{jvmjardir}/jce.jar
%{jvmjardir}/jce-%{javaver}.jar
%{jvmjardir}/jce-%{version}.jar
%{jvmjardir}/jdbc-stdext.jar
%{jvmjardir}/jdbc-stdext-%{javaver}.jar
%{jvmjardir}/jdbc-stdext-%{version}.jar
%{jvmjardir}/jndi.jar
%{jvmjardir}/jndi-%{javaver}.jar
%{jvmjardir}/jndi-%{version}.jar
%{jvmjardir}/jndi-cos.jar
%{jvmjardir}/jndi-cos-%{javaver}.jar
%{jvmjardir}/jndi-cos-%{version}.jar
%{jvmjardir}/jndi-dns.jar
%{jvmjardir}/jndi-dns-%{javaver}.jar
%{jvmjardir}/jndi-dns-%{version}.jar
%{jvmjardir}/jndi-ldap.jar
%{jvmjardir}/jndi-ldap-%{javaver}.jar
%{jvmjardir}/jndi-ldap-%{version}.jar
%{jvmjardir}/jndi-rmi.jar
%{jvmjardir}/jndi-rmi-%{javaver}.jar
%{jvmjardir}/jndi-rmi-%{version}.jar
%{jvmjardir}/jta.jar
%{jvmjardir}/jta-%{javaver}.jar
%{jvmjardir}/jta-%{version}.jar
%{jvmjardir}/jsse.jar
%{jvmjardir}/jsse-%{javaver}.jar
%{jvmjardir}/jsse-%{version}.jar
%{jvmjardir}/sasl.jar
%{jvmjardir}/sasl-%{javaver}.jar
%{jvmjardir}/sasl-%{version}.jar
%{_jvmjardir}/%{jrelnk}
%{_jvmdir}/%{sdkdir}/jre/lib/rt.jar
%{_jvmdir}/%{jredir}/lib/%{_arch}/libjawt.so
%{_jvmdir}/%{jredir}/lib/%{_arch}/client/libjvm.so
%{_jvmdir}/%{jredir}/lib/%{_arch}/server/libjvm.so
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}/native_threads
%{_jvmdir}/%{jredir}/lib/%{_arch}/native_threads/libhpi.so
# these must not be marked %config(noreplace). their names are used by
# rebuild-security-providers, which lists
# %{_sysconfdir}/java/security/security.d/*.  their contents are
# ignored, so replacing them doesn't matter.  .rpmnew files are
# harmful since they're interpreted by rebuild-security-providers as
# classnames ending in rpmnew.
%if 0
# (anssi) see earlier
%{_sysconfdir}/java/security/security.d/1000-gnu.java.security.provider.Gnu
%{_sysconfdir}/java/security/security.d/1001-gnu.javax.crypto.jce.GnuCrypto
%{_sysconfdir}/java/security/security.d/1002-gnu.javax.crypto.jce.GnuSasl
%{_sysconfdir}/java/security/security.d/1003-gnu.javax.net.ssl.provider.Jessie
%{_sysconfdir}/java/security/security.d/1004-gnu.javax.security.auth.callback.GnuCallbacks
%endif

%files devel
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/include/linux
%dir %{_jvmdir}/%{sdkdir}/lib
#%{_bindir}/aot-compile
%{_bindir}/aot-compile-rpm
%{python_sitelib}/aotcompile.py*
%{python_sitelib}/classfile.py*
%{python_sitelib}/*.egg-info
%{_jvmdir}/%{sdkdir}/bin/appletviewer
%{_jvmdir}/%{sdkdir}/bin/jar
%{_jvmdir}/%{sdkdir}/bin/jarsigner
%{_jvmdir}/%{sdkdir}/bin/java
%{_jvmdir}/%{sdkdir}/bin/javac
%{_jvmdir}/%{sdkdir}/bin/javadoc
%{_jvmdir}/%{sdkdir}/bin/javah
%{_jvmdir}/%{sdkdir}/bin/keytool
%{_jvmdir}/%{sdkdir}/bin/rmic
%{_jvmdir}/%{sdkdir}/bin/rmiregistry
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_jvmdir}/%{sdkdir}/include/jawt.h
%{_jvmdir}/%{sdkdir}/include/jni.h
%{_jvmdir}/%{sdkdir}/include/linux/jawt_md.h
%{_jvmdir}/%{sdkdir}/include/linux/jni_md.h
%{_jvmdir}/%{sdkdir}/include/linux/gcj
%{_jvmdir}/%{sdkdir}/include/gcj
%{_jvmdir}/%{sdkdir}/include/jni_md.h
%{_jvmdir}/%{sdkdir}/include/jawt_md.h
%{_jvmdir}/%{sdkdir}/lib/tools.jar

%files src
%{_jvmdir}/%{sdkdir}/src.zip

%if %without bootstrap
%files javadoc
%doc %{_javadocdir}/%{name}
# A JPackage that "provides" this directory will, in its %post script,
# remove the existing directory and install a new symbolic link to its
# versioned directory.  For Fedora we want clear file ownership so we
# make java-1.5.0-gcj-javadoc own this file.  Installing the
# corresponding JPackage over java-1.5.0-gcj-javadoc will work but
# will invalidate this file.
# (Anssi) Agreed, we also want this for Mandriva
%doc %{_javadocdir}/java
%endif

%if %with plugin
%files plugin
%endif




%changelog
* Mon Jul 23 2012 Arkady L. Shane <arkady.shane@rosalab.ru> - 1.5.0.0-19
- rebuilt against new gcc

* Tue Apr 26 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.5.0.0-18mdv2011.0
+ Revision: 659393
- Merge patches to aot-compile-rpm and add change to work with recent python

* Fri Apr 08 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.5.0.0-17.1.17
+ Revision: 651843
- Use libdir for java files, following default gcc-java install

* Wed Apr 06 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.5.0.0-17.1.16
+ Revision: 651345
- Properly correct dependency with gcc 4.6.0

* Wed Apr 06 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.5.0.0-17.1.15
+ Revision: 651293
- Rebuild with gcc 4.6.0

* Wed Feb 16 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.5.0.0-17.1.14
+ Revision: 638010
- Rebuild for gcc 4.5.2

* Sat Oct 30 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 1.5.0.0-17.1.13mdv2011.0
+ Revision: 590348
- rebuild with new python 2.7

* Wed Aug 25 2010 Funda Wang <fwang@mandriva.org> 1.5.0.0-17.1.12mdv2011.0
+ Revision: 573153
- rebuild for new gcc

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.0.0-17.1.11mdv2010.1
+ Revision: 520136
- rebuilt for 2010.1

* Sat Sep 26 2009 Michael Scherer <misc@mandriva.org> 1.5.0.0-17.1.10mdv2010.0
+ Revision: 449457
- rebuild for new gcc

* Thu Jun 04 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.5.0.0-17.1.9mdv2010.0
+ Revision: 382771
- update to 1.0.80 release and rebuild for gcc 4.4

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 1.5.0.0-17.1.8mdv2009.1
+ Revision: 320061
- move python requires to devel pacakge

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Wed May 21 2008 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-17.1.7mdv2009.0
+ Revision: 209808
- rebuild for new gcc

* Wed Mar 12 2008 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-17.1.6mdv2008.1
+ Revision: 187138
- rebuild for new gcc4.3

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Fri Jan 18 2008 David Walluck <walluck@mandriva.org> 1.5.0.0-17.1.5mdv2008.1
+ Revision: 154535
- javadoc should not require base package

* Wed Dec 19 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-17.1.4mdv2008.1
+ Revision: 133869
- use macro for python (Build)Requires
- fix gcj libdir

* Wed Dec 19 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-17.1.2mdv2008.1
+ Revision: 133778
- use gjar4.3 over fastjar by default

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Oct 27 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-17.1.0mdv2008.1
+ Revision: 102700
- don't raise error if aot-compile-rpm dir exists

* Wed Oct 24 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-17.1mdv2008.1
+ Revision: 101873
- add aot-compile-rpm.patch
- add aot-compile-rpm patch from Fedora

* Tue Sep 18 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.14mdv2008.0
+ Revision: 89539
- rebuild due to package loss

* Thu Aug 16 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.13mdv2008.0
+ Revision: 64137
- use external fastjar as jar instead of classpath gjar due to upstream
  classpath bug #32516

* Tue Aug 14 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-14.12mdv2008.0
+ Revision: 63478
- add %%{_jvmdir}/%%{jredir}/lib/%%{_arch}/native_threads/libhpi.so link to %%{_libdir}/gcj-%%{gccver}/libjvm.so for compatibility with kdebindings

* Sun Aug 12 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-14.11mdv2008.0
+ Revision: 62382
- fix symlink to from java.security to classpath.security

* Wed Jul 11 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-14.10mdv2008.0
+ Revision: 51195
- Requires: bouncycastle
- Provides: java-1.5.0-gcj-compat = 1.5.0

* Mon Jul 02 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.9mdv2008.0
+ Revision: 47223
- add compatibility symlink for jawt_md.h as well

* Mon Jul 02 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.8mdv2008.0
+ Revision: 47108
- add compatibility symlinks to allow jni.h to be included without having
  JAVA_HOME/include/linux as includedir, as that dir is not required when
  using libgcj normally
- add %%release to java-gcj-compat provides

* Sun Jul 01 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.7mdv2008.0
+ Revision: 46610
- provide symlink for gcj/libgcj-config.h, now needed by jni_md.h

* Sun Jul 01 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.6mdv2008.0
+ Revision: 46467
- add global macros %%gcj and %%gcj_dbtool

* Fri Jun 29 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.5mdv2008.0
+ Revision: 45734
- only require gcc4.3-java in the -devel package

* Fri Jun 29 2007 David Walluck <walluck@mandriva.org> 1.5.0.0-14.4mdv2008.0
+ Revision: 45674
- Requires: gcc%%{gccsuffix}-java for aot-compile-rpm

* Thu Jun 28 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.3mdv2008.0
+ Revision: 45416
- fix appletviewer symlink target
- require sinjdoc for javadoc symlink in devel package

* Wed Jun 27 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.2mdv2008.0
+ Revision: 45136
- allow sinjdoc failure if over 4000 docfiles were created
- disable bootstrap

* Tue Jun 26 2007 Anssi Hannula <anssi@mandriva.org> 1.5.0.0-14.1mdv2008.0
+ Revision: 44747
- drop now unneeded patch3
- enable bootstrap
- sync with fedora 1.5.0.0-14
- add only .so files linked against correct libgcj_bc to .db file (patch4)
- adapt for gcc4.3
- drop triggers for simplicity
- rename from java-1.4.2-gcj-compat to java-1.5.0-gcj

* Sun Jun 24 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.2.0-40.111.4mdv2008.0
+ Revision: 43659
- Do not hardcode jar versions (patch3)
- Fix --exclude option of aot-compile-rpm to work correctly when buildroot
  contains ending slash (patch2, fixes eclipse build on iurt)


* Thu Mar 15 2007 David Walluck <walluck@mandriva.org> 1.4.2.0-40.111.3mdv2007.1
+ Revision: 143957
- remove plugin package

* Sat Mar 10 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.2.0-40.111.2mdv2007.1
+ Revision: 140478
- drop keytool symlink from default build as it requires classpath

* Sat Mar 03 2007 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.111.1mdv2007.1
+ Revision: 131771
- 40.111

* Fri Mar 02 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.2.0-40.110.3mdv2007.1
+ Revision: 130927
- add bcond for classpathtools, disable by default to avoid
  requires on classpath
- fix requires when classpathtools is enabled

  + Thierry Vignaud <tvignaud@mandriva.com>
    - do not package empty NEWS

* Sat Dec 09 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.110.2mdv2007.1
+ Revision: 93971
- rebuild for new python

* Tue Oct 31 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.110.1mdv2007.1
+ Revision: 73919
- 40.110 (1.0.68)
- Import java-1.4.2-gcj-compat

* Fri Sep 01 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.103.1mdv2007.0
- 1.0.65 (40jpp_103rh)

* Sat Aug 26 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.102.1mdv2007.0
- 1.0.62 (40jpp_102rh)

* Sat Aug 26 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.101.2mdv2007.0
- remove update-alternatives --auto and update-alternatives --verbose
- fix aot-compile-rpm libdir

* Fri Aug 11 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.101.1mdv2007.0
- 1.0.62 (40jpp_101rh)

* Fri Aug 11 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.100.4mdv2007.0
- BuildRequires: python-devel

* Thu Aug 10 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.100.3mdv2007.0
- BuildRequires: python

* Sat Aug 05 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.100.2mdv2007.0
- try using update-alternatives --auto

* Fri Aug 04 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.100.1mdv2007.0
- 1.0.61 (40jpp_100rh)

* Mon Jul 31 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.98.1mdv2007.0
- 1.0.61 (40jpp_98rh)
- use full path to update-alternatives
- make update-alternatives --verbose to track down problems

* Tue Jul 18 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.88.5mdv2007.0
- provide jta for castor, tomcat5

* Tue Jul 18 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.88.4mdv2007.0
- something happened to the previous patch
- don't obsolete gnu-crypto

* Sun Jul 16 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.88.3mdv2007.0
- allow for -O0 to aot-compile-rpm

* Fri Jul 14 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.88.2mdv2007.0
- don't require classpath for bootstrap
- require ecj-boostrap for bootstrap
- use Conflicts instead of Obsoletes

* Mon Jul 10 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.88.1mdv2007.0
- 1.0.52 (40jpp_88rh)

* Sat Jun 24 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.87.2mdv2007.0
- fix macro definitions

* Sat Jun 24 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.87.1mdv2007.0
- 1.0.52 (40jpp_87rh)
- require classpath for appletviewer, jarsigner, and keytool

* Mon Apr 24 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.83.1mdv2007.0
- 1.0.52 (40jpp_83rh)
- remove %%{_bindir}/rebuild-security-providers
- build with libgcj.so.7
- patch aot-compile-rpm to lower -O level

* Thu Feb 23 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.80.3mdk
- requires xalan-j2 and xerces-j2

* Wed Feb 22 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.80.2mdk
- rebuild for gcc 4.0.3

* Mon Feb 13 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.80.1mdk
- 1.0.52 (40jpp_80rh)

* Tue Feb 07 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.76.1mdk
- 1.0.52 (40jpp_76rh)

* Thu Jan 26 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.63.1mdk
- 1.0.52 (40jpp_63rh)

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.62.4mdk
- Requires: bouncycastle

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.62.3mdk
- require ecj even when %%bootstrap is 1

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.62.2mdk
- add version to bootstrap provides

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.62.1mdk
- 1.0.51 (40jpp_62rh)

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.61.4mdk
- provide/obsolete all bootstrap packages

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.61.3mdk
- build bootstrap without gjdoc

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.61.2mdk
- BuildRequires: gjdoc

* Wed Jan 11 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.61.1mdk
- 1.0.50 (40jpp_61rh)
- ecj and gjdoc should only be reqired by the devel package

* Tue Jan 10 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.59.2mdk
- javadoc script wasn't included in the last build (why?)

* Thu Jan 05 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.59.1mdk
- 1.0.47 (40jpp_59rh)
- pthread patch merged upstream

* Wed Jan 04 2006 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.57.1mdk
- 1.0.45 (40jpp_57rh)
- add pthread patch

* Thu Dec 01 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.55.2mdk
- fix find command syntax in rebuild-gcj-db (bug #20030)

* Fri Nov 18 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.55.1mdk
- 1.0.45 (40jpp_55rh)

* Tue Nov 15 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.53.1mdk
- put back rebuild-security-providers

* Tue Nov 15 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.53.1mdk
- 1.0.44 (40jpp_51rh)

* Fri Nov 11 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.51.5mdk
- update for gcc 4.0.2

* Sun Nov 06 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.51.4mdk
- include native2ascii from cp-tools (20051106)

* Sun Nov 06 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.51.3mdk
- don't use alternatives for rebuild-gcj-db and aot-compile-rpm

* Sat Oct 29 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.51.2mdk
- link jni_md.h which no longer exists to jni.h for now

* Sat Oct 29 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.51.1mdk
- rebuild

* Fri Oct 21 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.19mdk
- fix rebuild-security-providers

* Thu Oct 20 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.18mdk
- don't count backup files as security providers

* Sun Oct 09 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.17mdk
- sync with java-gcj-compat 1.0.43 (51rh)
- add docs

* Wed Sep 07 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.16mdk
- use %%mkrel
- don't add provider file if %%bootstrap is 1

* Wed Sep 07 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.15mdk
- add %%{_sysconfdir}/java/security and %%{_sysconfdir}/java/security.d as %%dir

* Wed Sep 07 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.14mdk
- update bootstrap
- add gcj-specific files from jpackage-utils

* Sat Sep 03 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.13mdk
- sync with 40jpp_47rh and java-gcj-compat 1.0.40
- don't provide jndi-ldap or jta

* Fri Jul 29 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.12mdk
- sync with 40jpp_43rh and java-gcj-compat 1.0.36
- provides jndi-ldap
- use alternatives for jaxp_parser_impl and jaxp_transform_impl
- don't provide java-javadoc (use, e.g., classpath javadocs instead)

* Sun Jun 26 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0:1.4.2.0-40.11mdk
- gcc 4.0.1

* Sat Jun 11 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.10mdk
- sync with 40jpp_30rh and java-gcj-compat 1.0.30

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.9mdk
- export jaxp_parser_impl.jar and jaxp_transform_impl.jar

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.8mdk
- add symlink to jaxp_parser_impl.jar
- provide jaxp_transform_impl and add symlink to jaxp_transform_impl.jar

* Wed May 18 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.7mdk
- add requires on %%{_bindir}/rebuild-security-providers (fixes bug #16023)

* Thu May 12 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.6mdk
- rebuild as non-bootstrap

* Tue May 10 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.5mdk
- fix src dependency, but don't require it (yet)

* Tue May 10 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.4mdk
- provide java-javadoc
- don't require on gcc-java release

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.3mdk
- provide java-%%{javaver}-javadoc

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.2mdk
- fix symlinks and bin locations
- fix group

* Wed May 04 2005 David Walluck <walluck@mandriva.org> 0:1.4.2.0-40.1mdk
- release

* Sat Apr 16 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_18rh
- Require gnu-crypto.

* Sat Apr 16 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_17rh
- Provide jaxp_parser_impl.

* Thu Apr 14 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_16rh
- Import java-gcj-compat 1.0.28.

* Tue Apr 05 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_15rh
- Import java-gcj-compat 1.0.27.
- Bump gccver to 4.0.0-0.39.
- Make -devel take ownership of symlinks as well as regular files.

* Thu Mar 31 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_14rh
- Import java-gcj-compat 1.0.23.
- Always look for classpath.security in /usr/lib. (151561)
- Provide jsse. (151662)

* Thu Mar 17 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_13rh
- Uncomment rebuild-security-providers.
- Require jessie >= 1.0.0-3.

* Tue Mar 15 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_12rh
- Don't re-run rebuild-security-providers.

* Tue Mar 15 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_11rh
- Add jaas and jta provides.

* Tue Mar 08 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_10rh
- Import java-gcj-compat 1.0.22.
- Symlink jaas.jar, jdbc-stdext.jar, jndi.jar and jta.jar to
  libgcj.jar.

* Sat Mar 05 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_9rh
- Import java-gcj-compat 1.0.21.

* Sat Mar 05 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_8rh
- Import java-gcj-compat 1.0.20.
- Depend on jessie.
- Install jsse.jar.
- Install security directory.
- Symlink classpath.security to java.security.

* Sat Mar 05 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_7rh
- Import java-gcj-compat 1.0.19.

* Thu Mar 03 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_6rh
- Import java-gcj-compat 1.0.18.

* Thu Mar 03 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_5rh
- Update descriptions.

* Wed Mar 02 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_4rh
- Bump release number.

* Wed Mar 02 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_3rh
- Make java-1.4.2-gcj-compat-devel obsolete java-1.4.2-gcj4-compat-devel.
- Import java-gcj-compat 1.0.17.
- Specify --with-arch-directory and --with-os-directory options on
  configure line.

* Tue Mar 01 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_2rh
- Make arch-specific.

* Tue Mar 01 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-40jpp_1rh
- Merge java-1.4.2-gcj4-compat into java-1.4.2-gcj-compat.
- Import java-gcj-compat 1.0.15.
- Add AWT Native Interface symlinks.
- Remove build requires on eclipse-ecj.

* Thu Feb 17 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp_4rh
- Add -src sub-package.

* Wed Feb 09 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp_3rh
- Import java-gcj-compat 1.0.14.

* Tue Feb 08 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp_2rh
- Import java-gcj-compat 1.0.13.

* Mon Feb 07 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp_1rh
- Import java-gcj-compat 1.0.12.

* Wed Feb 02 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp_1rh
- Add Red Hat release number.

* Tue Feb 01 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp
- Remove gjdoc version requirement.
- Change java-gcj-compat version number.

* Tue Feb 01 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp
- Import java-gcj-compat 1.0.11.
- Require gjdoc.

* Tue Feb 01 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-4jpp
- Add jni.h symlink.
- Install rt.jar as an unmanaged symlink.
- Conflict and obsolete old java-gcj-compat rpms.
- Import java-gcj-compat 1.0.9.

* Mon Jan 24 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-3jpp
- Import java-gcj-compat 1.0.8.

* Thu Jan 13 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-2jpp
- Make jvmjardir use cname, not name.

* Wed Jan 12 2005 Thomas Fitzsimmons <fitzsim@redhat.com> 0:1.4.2.0-1jpp
- Initial build.

