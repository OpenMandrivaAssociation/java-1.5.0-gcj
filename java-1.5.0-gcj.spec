# with => disabled by default
# without => enabled by default

%bcond_without bootstrap
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

Summary:	JPackage runtime scripts for GCJ
Name:		java-%{javaver}-%{origin}
Version:	%{javaver}.%{buildver}
Release:	26
Group:		Development/Java
License:	GPLv2
Url:		http://sources.redhat.com/rhug/java-gcj-compat.html
Source0:	ftp://sources.redhat.com/pub/rhug/java-gcj-compat-%{jgcver}.tar.gz
Patch0:		java-1.4.2-gcj-compat-aot-compile-rpm.patch
# Add only .so linked to correct libgcj_bc.so during rebuild-gcj-db,
# to avoid gij failure with non-rebuilt packages
Patch1:		java-1.5.0-gcj-ensure-soname-compat.patch
# Fix invalid python code causing aotcompile to explode
Patch5:		java-gcj-compat-1.0.80-fix-aotcompile.patch

# required to calculate gcj binary's path to encode in aotcompile.py
# and rebuild-gcj-db
BuildRequires:	gcc%{gccsuffix}-java eclipse-ecj
BuildRequires:	libgcj%{gccsoversion}-src
# required for cacerts generation
BuildRequires:	openssl
BuildRequires:	gcj-tools
BuildRequires:	python-devel
BuildRequires:	java-rpmbuild
%if %without bootstrap
BuildRequires:	java-1.7.0-openjdk-devel
%endif
BuildArch:	noarch

# required for tools and libgcj.jar
Requires:	%{mklibname gcj %{gccsoversion}} >= %{gccver}
# XXX:	this might not be the right place for it, but it needs to be somewhere
Requires:	bouncycastle
# required for directory structures
Requires:	jpackage-utils >= 1.7.3
Requires(post,postun):	jpackage-utils
Requires(post,postun):	update-alternatives >= 1.8.6

# standard JPackage base provides
Provides:	jre-%{javaver}-%{origin} = %{version}-%{release}
Provides:	jre-%{origin} = %{version}-%{release}
Provides:	jre-%{javaver} = %{version}-%{release}
Provides:	java-%{javaver} = %{version}-%{release}
Provides:	jre = %{javaver}
Provides:	java-%{origin} = %{version}-%{release}
Provides:	java = %{javaver}
# libgcj provides, translated to JPackage provides
Provides:	jaas = %{version}-%{release}
Provides:	jce = %{version}-%{release}
Provides:	jdbc-stdext = %{version}-%{release}
Provides:	jdbc-stdext = 3.0
Provides:	jndi = %{version}-%{release}
Provides:	jndi-cos = %{version}-%{release}
Provides:	jndi-dns = %{version}-%{release}
Provides:	jndi-ldap = %{version}-%{release}
Provides:	jndi-rmi = %{version}-%{release}
Provides:	jsse = %{version}-%{release}
Provides:	java-sasl = %{version}-%{release}
Provides:	jaxp_parser_impl = %{version}-%{release}
# java-gcj-compat base provides
# (anssi) added release
Provides:	java-gcj-compat = %{jgcver}-%{release}
Provides:	java-1.4.2-gcj-compat = 1.4.2.0-41
Provides:	java-1.5.0-gcj-compat = 1.5.0

# Mandriva added:
Provides:	jaxp_transform_impl = %{version}-%{release}
Provides:	jta = %{version}-%{release}

Obsoletes:	java-1.4.2-gcj-compat < 1.4.2.0-41
Obsoletes:	gnu-crypto < 2.1.0-7
Obsoletes:	gnu-crypto-der < 2.1.0-7
Obsoletes:	gnu-crypto-auth-jdk1.4 < 2.1.0-7
Obsoletes:	gnu-crypto-jce-jdk1.4 < 2.1.0-7
Obsoletes:	gnu-crypto-sasl-jdk1.4 < 2.1.0-7
Obsoletes:	jessie <= 1.0.1-7
Obsoletes:	classpathx-jaf <= 1.0-16
Provides:	jaf = 0:%{jafver}
Provides:	activation = 0:%{jafver}
Obsoletes:	gnujaf <= 0:1.0-0.rc1.1jp

%description
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible runtime environment with GCJ.

%package devel
Summary:	JPackage development scripts for GCJ
Group:		Development/Java

# require base package
Requires:	%{name} = %{version}-%{release}
# require python for aot-compile
Requires:	python
# post requires alternatives to install tool alternatives
Requires(post):	update-alternatives >= 1.8.6
# postun requires alternatives to uninstall tool alternatives
Requires(postun):	update-alternatives
%py_requires -d
Requires:	gcc%{gccsuffix}-java

%if %with fastjar
Requires:	fastjar
%endif

%if %without bootstrap
# For javadoc symlink
Requires:	java-1.7.0-openjdk-devel
%endif
# For java == gij symlink
Requires:	gcj-tools

# standard JPackage devel provides
Provides:	java-sdk-%{javaver}-%{origin} = %{version}
Provides:	java-sdk-%{javaver} = %{version}
Provides:	java-sdk-%{origin} = %{version}
Provides:	java-sdk = %{javaver}
Provides:	java-%{javaver}-devel = %{version}
Provides:	java-devel-%{origin} = %{version}
Provides:	java-devel = %{javaver}
# java-gcj-compat devel provides
# (anssi) added release
Provides:	java-gcj-compat-devel = %{jgcver}-%{release}
Provides:	java-1.4.2-gcj-compat-devel = 1.4.2.0-41

Obsoletes:	java-1.4.2-gcj-compat-devel < 1.4.2.0-41

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

Requires:	%{name} = %{version}-%{release}
Requires:	libgcj%{gccsoversion}-src >= %{gccver}

# java-gcj-compat src provides
Provides:	java-1.4.2-gcj-compat-src = 1.4.2.0-41
Obsoletes:	java-1.4.2-gcj-compat-src < 1.4.2.0-41

%description src
This package installs a versionless src.zip symlink that points to a
specific version of the libgcj sources.

%if %without bootstrap
%package javadoc
Summary:	API documentation for libgcj
Group:		Development/Java

# require base package
# (walluck):	why? docs should not require a JVM
#Requires:	%{name} = %{version}-%{release}

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
Summary:	Web browser plugin that handles applets
Group:		Development/Java

# require base package
Requires:	%{name} = %{version}-%{release}
# require libgcj for plugin shared object
Requires:	%{_lib}gcj%{gccsoversion} >= %{gccver}
# post requires alternatives to install plugin alternative
Requires(post):	update-alternatives
# postun requires alternatives to uninstall plugin alternative
Requires(postun):	update-alternatives

# standard JPackage plugin provides
Provides:	java-plugin = %{javaver}
Provides:	java-%{javaver}-plugin = %{version}
# java-gcj-compat plugin provides
Provides:	java-1.4.2-gcj-compat-plugin = 1.4.2.0-41
Obsoletes:	java-1.4.2-gcj-compat-plugin < 1.4.2.0-41

%description plugin
This package installs gcjwebplugin, a Mozilla plugin for applets.
%endif

%prep
%setup -qn java-gcj-compat-%{jgcver}
%apply_patches
# (anssi) for patch4:
GCJ_BC_MAJOR=$(objdump -p $(gcj%gccsuffix -print-file-name=libgcj_bc.so) | \
	grep SONAME | sed -ne 's,^.*libgcj_bc.so.\([^ ]\).*$,\1,p')
sed -i -e "s,\@GCJ_BC_MAJOR\@,$GCJ_BC_MAJOR," rebuild-gcj-db.in

# (anssi)
sed -i -e 's,gkeytool ,gkeytool%{gccsuffix} ,' generate-cacerts.pl
sed -i -e 's,gjarsigner ,gjarsigner%{gccsuffix} ,' Makefile.am
sed -i -e 's,gappletviewer ,gappletviewer%{gccsuffix} ,' Makefile.am

%if %with fastjar
# (anssi) GCC4.2 contains gjar instead of fastjar
# we use external fastjar due to upstream classpath bug anyway:
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=32516
sed -i -e 's,fastjar\$\(gcc_suffix\),fastjar,' Makefile.am
%else
sed -i -e 's,fastjar\$\(gcc_suffix\),gjar\$\(gcc_suffix\),' Makefile.am
%endif
aclocal
automake
autoconf

%build
export CLASSPATH=
export JAR=%jar
%configure2_5x \
	--disable-symlinks \
	--with-arch-directory=%{_arch} \
	--with-os-directory=linux \
	--with-security-directory=%{_sysconfdir}/java/security/security.d \
	--with-gcc-suffix=%{gccsuffix} \
	--with-origin-name=gcj

%make

# the python compiler encodes the source file's timestamp in the .pyc
# and .pyo headers.  since aotcompile.py is generated by configure,
# its timestamp will differ from build to build.  this causes multilib
# conflicts.  we work around this by setting aotcompile.py's timestamp
# to equal aotcompile.py.in's timestamp. (205216)
touch --reference=aotcompile.py.in aotcompile.py

%install
%makeinstall_std

# extensions handling
install -dm 755 %{buildroot}%{jvmjardir}
pushd %{buildroot}%{jvmjardir}
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
install -dm 755 %{buildroot}%{_jvmdir}/%{jredir}/lib/security
ln -sf %{_prefix}/lib/security/classpath.security %{buildroot}%{_jvmdir}/%{jredir}/lib/security/java.security

%if 0
# (anssi) we have those in jpackage-utils

# default security providers, provided by libgcj
install -dm 755 %{buildroot}%{_sysconfdir}/java/security/security.d
for provider in \
  1000-gnu.java.security.provider.Gnu \
  1001-gnu.javax.crypto.jce.GnuCrypto \
  1002-gnu.javax.crypto.jce.GnuSasl \
  1003-gnu.javax.net.ssl.provider.Jessie \
  1004-gnu.javax.security.auth.callback.GnuCallbacks
do
  cat > %{buildroot}%{_sysconfdir}/java/security/security.d/$provider << EOF
# This file's contents are ignored.  It's name, of the form
# <priority>-<provider name>, is used by rebuild-security-providers to
# rebuild the list of security providers in libgcj's
# classpath.security file.
EOF
done

%endif

# cacerts
%{__perl} generate-cacerts.pl
install -m 644 cacerts %{buildroot}%{_jvmdir}/%{jredir}/lib/security

# versionless symlinks
pushd %{buildroot}%{_jvmdir}
   ln -s %{jredir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

pushd %{buildroot}%{_jvmjardir}
   ln -s %{sdkdir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

# classmap database directory
install -dm 755 %{buildroot}%{_libdir}/gcj

%if %without bootstrap
# build and install API documentation
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
pushd %{buildroot}%{_javadocdir}
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
    -d %{buildroot}%{_javadocdir}/%{name} \
    -encoding UTF-8 -breakiterator \
    -linksource -splitindex -doctitle "GNU libgcj $GIJ_VERSION" \
    -windowtitle "GNU libgcj $GIJ_VERSION Documentation" || \
      [ 0$(find %{buildroot}%{_javadocdir}/%{name} | wc -l) -gt 3800 ]
# (anssi) if over 3800 docfiles are created, consider it a success enough
popd
%endif

%ifarch x86_64
cd %{buildroot}%{_jvmdir}/%{jredir}/lib && \
ln -s %{_arch} amd64
%endif

# install operating system include directory
install -dm 755 %{buildroot}%{_jvmdir}/%{sdkdir}/include/linux

# install libjvm.so directories
install -dm 755 %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/client
install -dm 755 %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/server

# install native_threads directory
mkdir -p %{buildroot}%{_jvmdir}/%{jredir}/lib/%{_arch}/native_threads

# install tools.jar directory
install -dm 755 %{buildroot}%{_jvmdir}/%{sdkdir}/lib

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
install -dm 755 %{buildroot}%{_jvmdir}/%{sdkdir}/include/linux/gcj
ln -s $(gcj%{gccsuffix} -print-file-name=include/gcj/libgcj-config.h) %{buildroot}%{_jvmdir}/%{sdkdir}/include/linux/gcj/libgcj-config.h

# (anssi) Normally there is no need to do -I$JAVA_HOME/include/linux when
# building with gcj. Therefore some software (OOo) may assume it is not
# needed, thus these compatibility symlinks.
ln -s linux/gcj %{buildroot}%{_jvmdir}/%{sdkdir}/include/gcj
ln -s linux/jni_md.h %{buildroot}%{_jvmdir}/%{sdkdir}/include/jni_md.h
ln -s linux/jawt_md.h %{buildroot}%{_jvmdir}/%{sdkdir}/include/jawt_md.h

pushd %{buildroot}%{_jvmdir}/%{sdkdir}/jre/lib
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
%{_sbindir}/update-alternatives \
	--install %{_javadir}/jaxp_parser_impl.jar \
	jaxp_parser_impl %{_javadir}/libgcj-%{gccver}.jar 20

# jaxp_transform_impl
%{_sbindir}/update-alternatives \
	--install %{_javadir}/jaxp_transform_impl.jar \
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

