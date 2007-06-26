%bcond_with             bootstrap
%bcond_with             classpathtools
%bcond_with             plugin

%define section		free

%{!?custom:	%global custom 0}
%{!?gcjprefix: 	%global gcjprefix %{nil}}
%{!?origin:	%global origin gcj%{gccsuffix}}
%define gccsuffix	%{nil}
%define gccsoversion	7
%define priority	1420
%define	javaver		1.4.2
%define buildver	0
# the version-release string for the gcj rpms we require
%define gccver		4.1.2
%define jgcver		1.0.68
%define jar		%{_bindir}/fastjar

%define cname           java-%{javaver}-%{origin}

%define	sdklnk		java-%{javaver}-%{origin}
%define	jrelnk		jre-%{javaver}-%{origin}
%define	sdkdir		%{cname}-%{version}
%define	jredir		%{sdkdir}/jre
%define sdkbindir	%{_jvmdir}/%{sdklnk}/bin
%define jrebindir	%{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{cname}-%{version}

%if %with plugin
%define plugindir       %{_libdir}/mozilla/plugins
%endif

Name:		java-%{javaver}-%{origin}-compat
Version:	%{javaver}.%{buildver}
Release:	%mkrel 40.111.4
Epoch:		0
Summary:	JPackage runtime scripts for GCJ

Group:		Development/Java
License:	GPL
URL:		ftp://sources.redhat.com/pub/rhug/
Source0:	ftp://sources.redhat.com/pub/rhug/java-gcj-compat-%{jgcver}.tar.bz2
Source1:	ecj.sh.in
Source2:	native2ascii
Source3:	Native2ASCII.java
Patch0:		java-1.4.2-gcj-compat-no-gjdoc.patch
Patch1:		java-1.4.2-gcj-compat-aot-compile-rpm.patch
# (anssi) fix --exclude when buildroot contains ending slash:
Patch2:		java-1.4.2-gcj-compat-aotcompile-normpath.patch
Patch3:		java-1.4.2-gcj-compat-no-hardcoded-jar-versions.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	jpackage-utils >= 0:1.6, sed
BuildRequires:	gcc%{gccsuffix}-java >= 0:%{gccver}
Requires:	gcj%{gccsuffix}-tools
%if %without bootstrap
BuildRequires:	gjdoc
BuildRequires:	libgcj%{gccsoversion}-src >= 0:%{gccver}
BuildRequires:	python-devel
Requires:	gjdoc
Requires:	bouncycastle
Requires:	jpackage-utils >= 0:1.6.6
Requires:	gcj%{gccsuffix}-tools
Requires(post):	jpackage-utils >= 0:1.6.6
Requires(postun): jpackage-utils >= 0:1.6.6
Requires(post):	gcj%{gccsuffix}-tools
Requires(postun): gcj%{gccsuffix}-tools
%endif
Provides:	jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:	jre-%{origin} = %{epoch}:%{version}-%{release}
Provides:	jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{javaver}
Provides:	java-%{origin} = %{epoch}:%{version}-%{release}
Provides:	java = %{epoch}:%{javaver}
Provides:	jaxp_parser_impl
Provides:	jndi, jdbc-stdext = 0:2.0, jaas, jsse, jta
Provides:	java-gcj-compat = %{epoch}:%{jgcver}
Provides:	jaxp_transform_impl
# SASL and JCE are provided by libgcj.
Provides:	java-sasl
Provides:	jce
%if %without bootstrap
BuildRequires:	gjdoc
BuildRequires:	unzip
%endif
%if %{custom}
# prevent autogeneration of libjawt.so dependencies
AutoReqProv:    no
%endif
Obsoletes:      java-1.4.2-gcj-compat-bootstrap

%description
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible runtime environment with GCJ.

%package devel
Summary:	JPackage development scripts for GCJ
Group:		Development/Java
Requires:	%{_sbindir}/update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides:	java-sdk-%{javaver}
Provides:       java-sdk-%{origin} = %{epoch}:%{version}
Provides:	java-sdk = %{epoch}:%{javaver}
Provides:       java-%{javaver}-devel
Provides:	java-devel-%{origin} = %{epoch}:%{version}
Provides:       java-devel = %{epoch}:%{javaver}
Provides:	java-gcj-compat-devel = %{epoch}:%{jgcver}
Requires:	%{name} = %{epoch}:%{version}-%{release}
%if %without bootstrap
Requires:	eclipse-ecj
%else
Requires:	ecj-bootstrap
%endif
%if %without bootstrap
%if %with classpathtools
Requires(post): classpath
Requires: classpath
%endif
Requires:	gjdoc
# FIXME: This is a workaround for various other problems (alternatives)
Requires:	xalan-j2
Requires:	xerces-j2
%endif
Requires:	python
Requires:	gcc%{gccsuffix}-java >= 0:%{gccver}
Requires:	%{_lib}gcj%{gccsoversion}-devel >= 0:%{gccver}
Requires(post):	gcc%{gccsuffix}-java >= 0:%{gccver}
Requires(postun): gcc%{gccsuffix}-java >= 0:%{gccver}
Requires(post): %{_lib}gcj%{gccsoversion}-devel >= 0:%{gccver}
Requires(postun): %{_lib}gcj%{gccsoversion}-devel >= 0:%{gccver}

Obsoletes:      java-1.4.2-gcj-compat-bootstrap-devel

%description devel
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible development environment with
GCJ.

%package src
Summary:	Source files for libgcj
Group:		Development/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgcj%{gccsoversion}-src >= 0:%{gccver}
Requires(post):	 gcc%{gccsuffix}-java >= 0:%{gccver}
Requires(postun): gcc%{gccsuffix}-java >= 0:%{gccver}
Requires(post): libgcj%{gccsoversion}-src >= 0:%{gccver}
Requires(postun): libgcj%{gccsoversion}-src >= 0:%{gccver}
Obsoletes:      java-1.4.2-gcj-compat-bootstrap-src

%description src
This package installs a versionless src.zip symlink that points to a
specific version of the libgcj sources.

%if %without bootstrap
%package javadoc
Summary:       API documentation for libgcj
Group:         Development/Java
Requires:      %{name} = %{epoch}:%{version}-%{release}
Provides:      java-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
This package installs Javadoc API documentation for libgcj.
%endif

%if %with plugin
%package plugin
Summary:       Web browser plugin that handles applets
Group:         Development/Java
Provides:       java-plugin = %{javaver}, java-%{javaver}-plugin = %{version}
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:       %{_sbindir}/update-alternatives
Requires(post):       %{_sbindir}/update-alternatives
Requires(postun):     %{_sbindir}/update-alternatives
Requires:	%{_lib}gcj%{gccsoversion} >= 0:%{gccver}
Requires(post): %{_lib}gcj%{gccsoversion} >= 0:%{gccver}
Requires(postun): %{_lib}gcj%{gccsoversion} >= 0:%{gccver}

%description plugin
This package installs gcjwebplugin, a Mozilla plugin for applets.
%endif

%prep
%setup -q -n java-gcj-compat-%{jgcver}
%if %with bootstrap
%patch0 -p1 -b .no-gjdoc
%endif
%patch1 -p1 -b .aot-compile-rpm
%patch2 -p1
%patch3 -p1
%{__perl} -pi -e 's/^find/find -L/' rebuild-gcj-db.in
%{__mkdir_p} src/gnu/classpath/tools/native2ascii
%{__install} -m 644 %{SOURCE3} src/gnu/classpath/tools/native2ascii/Native2ASCII.java 

%build
aclocal
automake
autoconf
export CLASSPATH=
export JAR=%{jar}
%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif
%configure2_5x --disable-symlinks --with-arch-directory=%{_arch} \
  --with-os-directory=linux \
%if %{custom}
  --with-origin-name=%{origin} \
%endif
  --with-classpath-security=%{_prefix}/lib/security/classpath.security \
  --with-security-directory=%{_sysconfdir}/java/security/security.d
%{__make}
(cd src && %{javac} gnu/classpath/tools/native2ascii/Native2ASCII.java)

%if %{custom}
cp -a %{SOURCE1} eclipse-ecj-%{cname}.jar
sed 's:@JAVADIR@:%{_javadir}:g' < %{SOURCE1} > ecj-1
sed 's:eclipse-ecj.jar:eclipse-ecj-%{cname}.jar:g' < ecj-1 > ecj-2
LIBGCJ_JAR="%{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar"
sed "s,compiler.batch.Main,compiler.batch.Main -bootclasspath $LIBGCJ_JAR,g" < ecj-2 > ecj-%{cname}
%endif

# the python compiler encodes the source file's timestamp in the .pyc
# and .pyo headers.  since aotcompile.py is generated by configure,
# its timestamp will differ from build to build.  this causes multilib
# conflicts.  we work around this by setting aotcompile.py's timestamp
# to equal aotcompile.py.in's timestamp. (205216)
touch --reference=aotcompile.py.in aotcompile.py

%install
%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%if %{custom}
rm -f $RPM_BUILD_ROOT%{_bindir}/aot-compile-rpm
rm -f $RPM_BUILD_ROOT%{_bindir}/rebuild-gcj-db
rm -f $RPM_BUILD_ROOT%{_bindir}/aot-compile
rm -rf $RPM_BUILD_ROOT%{python_sitelib}
%endif

%if %{custom}
ln -sf %{_bindir}/ecj-%{cname} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/bin/javac
%endif

# create extensions symlinks
# jessie
%if %without bootstrap
%{__mkdir_p} $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib
ln -s %{_javadir}/jsse.jar $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/jsse.jar
%else
rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/bin/javadoc
%endif

# extensions handling
install -dm 755 $RPM_BUILD_ROOT%{jvmjardir}
pushd $RPM_BUILD_ROOT%{jvmjardir}
   ln -s %{_jvmdir}/%{jredir}/lib/jaas.jar jaas-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/jdbc-stdext.jar jdbc-stdext-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/jndi.jar jndi-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/jta.jar jta-%{version}.jar
%if %without bootstrap
   ln -s %{_jvmdir}/%{jredir}/lib/jsse.jar jsse-%{version}.jar
%endif
   for jar in *-%{version}.jar ; do
     ln -sf ${jar} $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
     ln -sf ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

# security directories
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security

# versionless symlinks
pushd $RPM_BUILD_ROOT%{_jvmdir}
   ln -s %{jredir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

pushd $RPM_BUILD_ROOT%{_jvmjardir}
   ln -s %{sdkdir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

# generate file lists
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' >  %{name}-%{version}-all.files
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | sed 's|'$RPM_BUILD_ROOT'||'      >> %{name}-%{version}-all.files

cat %{name}-%{version}-all.files \
  > %{name}-%{version}.files

find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/bin -type f -o -type l \
  | sed "s|^$RPM_BUILD_ROOT||"      > %{name}-%{version}-sdk-bin.files

# classmap database directory
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/gcj

%if %{custom}
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m644 eclipse-ecj-%{cname}.jar $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m755 ecj-%{cname} $RPM_BUILD_ROOT%{_bindir}
%endif

%{__mkdir_p} %{buildroot}%{sdkbindir}
%{__install} -m 755 %{SOURCE2} %{buildroot}%{sdkbindir}/native2ascii

(cd src && %{jar} uMf %{buildroot}%{_jvmdir}/%{sdklnk}/lib/tools.jar gnu/classpath/tools/native2ascii/Native2ASCII.class)

%if %without bootstrap
# build and install api documentation
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
#touch $RPM_BUILD_ROOT%{_javadocdir}/{%{name},java}
mkdir docsbuild
pushd docsbuild
# work around ppc64 file system corruption
  if unzip -tq %{_javadir}/src-%{gccver}.zip
  then
    %{jar} xf %{_javadir}/src-%{gccver}.zip
    rm -rf gnu
    find ./ -name \*.java | xargs -n 1 dirname | sort | uniq | sed -e "s/\.\///" | sed -e "s/\//\./" | \
      sed -e "s/\//\./" | sed -e "s/\//\./" | sed -e "s/\//\./" | sed -e "s/\//\./" | \
      xargs gjdoc -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} -encoding UTF-8 -breakiterator -licensetext \
        -linksource -splitindex -doctitle "GNU libgcj `gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`" \
        -windowtitle "GNU libgcj `gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'` Documentation"
    # work around apparent gjdoc/libgcj rounding error that causes a
    # multilib conflict in Double.html
    sed -i 's/2.147483647/2.147483648/g' $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/java/lang/Double.html
  else
    touch $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/package-list
  fi
popd
%endif

%ifarch x86_64
cd %{buildroot}%{_jvmdir}/%{jredir}/lib && \
%{__ln_s} %{_arch} amd64
%endif

# install libjvm.so directories
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{_arch}/client
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{_arch}/server

%if %with plugin
%{__mkdir_p} %{buildroot}%{plugindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

%{_sbindir}/update-alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre          jre          %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre       jre_exports  %{_jvmjardir}/%{jrelnk} \
%if %with classpathtools
  --slave %{_bindir}/keytool      keytool      %{jrebindir}/keytool \
%endif
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

# rt.jar
ln -sf \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/rt.jar

# jaas.jar
ln -sf \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/jaas.jar

# jsse.jar
ln -sf \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/jsse.jar

# jdbc-stdext.jar
ln -sf \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/jdbc-stdext.jar

# jndi.jar
ln -sf \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/jndi.jar

# jta.jar
ln -sf \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/jta.jar

# java.security
ln -sf \
  %{_prefix}/lib/security/classpath.security \
  %{_jvmdir}/%{cname}-%{version}/jre/lib/security/java.security

if [ -x %{_bindir}/rebuild-security-providers ]
then
  %{_bindir}/rebuild-security-providers
fi

%if %{custom}
# jaxp_parser_impl
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl \
  %{gcj_prefix}/share/java/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%else
# jaxp_parser_impl
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%endif

%if %{custom}
# jaxp_transform_impl.jar
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl \
  %{gcj_prefix}/share/java/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%else
# jaxp_transform_impl
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl \
  %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%endif

%{update_gcjdb}
{
  # libjawt.so
  ln -sf %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libjawt.so \
    %{_jvmdir}/%{jredir}/lib/%{_arch}/libjawt.so

  # libjvm.so
  ln -sf %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libjvm.so \
    %{_jvmdir}/%{jredir}/lib/%{_arch}/client/libjvm.so
  ln -sf %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libjvm.so \
    %{_jvmdir}/%{jredir}/lib/%{_arch}/server/libjvm.so
} || :

%post devel

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

%{_sbindir}/update-alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java     java_sdk          %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java  java_sdk_exports  %{_jvmjardir}/%{sdklnk} \
%if %without bootstrap
  --slave %{_bindir}/javadoc  javadoc           %{sdkbindir}/javadoc \
%endif
  --slave %{_bindir}/javah    javah             %{sdkbindir}/javah \
  --slave %{_bindir}/jar      jar               %{sdkbindir}/jar \
%if %without bootstrap
%if %with classpathtools
  --slave %{_bindir}/appletviewer        appletviewer                %{_bindir}/gappletviewer \
  --slave %{_bindir}/jarsigner        jarsigner                %{_bindir}/gjarsigner \
  --slave %{_bindir}/keytool        keytool                %{_bindir}/gkeytool \
%endif
%endif
  --slave %{_bindir}/rmic     rmic              %{sdkbindir}/rmic \
  --slave %{_bindir}/native2ascii     native2ascii              %{sdkbindir}/native2ascii

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

# jni.h
ln -sf \
  `gcj%{gccsuffix} -print-file-name=include/jni.h` \
  %{_jvmdir}/%{cname}-%{version}/include/jni.h

# jni_md.h
ln -sf \
  `gcj%{gccsuffix} -print-file-name=include/jni_md.h` \
  %{_jvmdir}/%{cname}-%{version}/include/linux/jni_md.h

# jawt.h
ln -sf \
  `gcj%{gccsuffix} -print-file-name=include/jawt.h` \
  %{_jvmdir}/%{cname}-%{version}/include/jawt.h

# jawt_md.h
ln -sf \
  `gcj%{gccsuffix} -print-file-name=include/jawt_md.h` \
  %{_jvmdir}/%{cname}-%{version}/include/linux/jawt_md.h

%post src

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

# src.zip
ln -sf \
  %{_javadir}/src-`gcj%{gccsuffix} --version | head -n 1 | awk '{ print $3 }'`.zip \
  %{_jvmdir}/%{cname}-%{version}/src.zip

%post javadoc
{
  rm -f %{_javadocdir}/%{name} %{_javadocdir}/java
  ln -sf %{name}-%{version} %{_javadocdir}/%{name}
  ln -sf %{name}-%{version} %{_javadocdir}/java
} || :

%if %with plugin
%post plugin
[ -d %{plugindir} ] || %{__mkdir_p} %{plugindir}
%{_sbindir}/update-alternatives --install %{plugindir}/libjavaplugin.so \
    libjavaplugin.so %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libgcjwebplugin.so %{priority}
%endif

%postun
if [ $1 -eq 0 ] ; then

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

   %{_sbindir}/update-alternatives --remove java %{jrebindir}/java
   %{_sbindir}/update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk}
   %{_sbindir}/update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
%if %{custom}
   %{_sbindir}/update-alternatives --remove jaxp_parser_impl \
     %{gcj_prefix}/share/java/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar
%else
   %{_sbindir}/update-alternatives --remove jaxp_parser_impl \
     %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar
%endif
%if %{custom}
   %{_sbindir}/update-alternatives --remove jaxp_transform_impl \
     %{gcj_prefix}/share/java/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar
%else
   %{_sbindir}/update-alternatives --remove jaxp_transform_impl \
     %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar
%endif
fi

if [ -x %{_bindir}/rebuild-security-providers ]
then
  %{_bindir}/rebuild-security-providers
fi

if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%postun devel
if [ $1 -eq 0 ] ; then

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

   %{_sbindir}/update-alternatives --remove javac %{sdkbindir}/javac
   %{_sbindir}/update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
   %{_sbindir}/update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi


%triggerin -- libgcj%{gccsuffix} > %{gccver}
{

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

  # rt.jar
  ln -sf \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
    %{_jvmdir}/%{cname}-%{version}/jre/lib/rt.jar

  # jaas.jar
  ln -sf \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
    %{_jvmdir}/%{cname}-%{version}/jre/lib/jaas.jar

  # jsse.jar
  ln -sf \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
    %{_jvmdir}/%{cname}-%{version}/jre/lib/jsse.jar

  # jdbc-stdext.jar
  ln -sf \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
    %{_jvmdir}/%{cname}-%{version}/jre/lib/jdbc-stdext.jar

  # jndi.jar
  ln -sf \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
    %{_jvmdir}/%{cname}-%{version}/jre/lib/jndi.jar

  # jta.jar
  ln -sf \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar \
    %{_jvmdir}/%{cname}-%{version}/jre/lib/jta.jar

%if %{custom}
  # jaxp_parser_impl
  %{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
    jaxp_parser_impl \
    %{gcj_prefix}/share/java/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%else
  # jaxp_parser_impl
  %{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
    jaxp_parser_impl \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%endif

%if %{custom}
  # jaxp_transform_impl
  %{_sbindir}/update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
    jaxp_transform_impl \
    %{gcj_prefix}/share/java/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%else
  # jaxp_transform_impl
  %{_sbindir}/update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
    jaxp_transform_impl \
    %{_javadir}/libgcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`.jar 20
%endif

  # libjawt.so
  ln -sf %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libjawt.so \
    %{_jvmdir}/%{jredir}/lib/%{_arch}/libjawt.so

  # libjvm.so
  ln -sf %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libjvm.so \
    %{_jvmdir}/%{jredir}/lib/%{_arch}/client/libjvm.so
  ln -sf %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libjvm.so \
    %{_jvmdir}/%{jredir}/lib/%{_arch}/server/libjvm.so

} || :

# gcc-java requires libgcj-devel which provides jni.h
%triggerin devel -- gcc%{gccsuffix}-java > 0:%{gccver}
{

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

  # jni.h
  ln -sf \
    `gcj%{gccsuffix} -print-file-name=include/jni.h` \
    %{_jvmdir}/%{cname}-%{version}/include/jni.h

  # jni_md.h
  ln -sf \
    `gcj%{gccsuffix} -print-file-name=include/jni_md.h` \
    %{_jvmdir}/%{cname}-%{version}/include/jni_md.h

  # jawt.h
  ln -sf \
    `gcj%{gccsuffix} -print-file-name=include/jawt.h` \
    %{_jvmdir}/%{cname}-%{version}/include/jawt.h

  # jawt_md.h
  ln -sf \
    `gcj%{gccsuffix} -print-file-name=include/jawt_md.h` \
    %{_jvmdir}/%{cname}-%{version}/include/linux/jawt_md.h
} || :

%triggerin src -- libgcj%{gccsoversion}-src >= 0:%{gccver}
{

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

  ln -sf \
    %{_javadir}/src-`gcj%{gccsuffix} --version | head -n 1 | awk '{ print $3 }'`.zip \
    %{_jvmdir}/%{cname}-%{version}/src.zip
} || :

%if %with plugin
%postun plugin
if [ $1 -eq 0 ] ; then
   %{_sbindir}/update-alternatives --remove libjavaplugin.so %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libgcjwebplugin.so
fi

%triggerin plugin -- libgcj%{gccsuffix} > %{gccver}
{

%if %{custom}
export PATH=%{gcj_prefix}/bin:$PATH
%endif

  # plugin
  %{_sbindir}/update-alternatives --install %{plugindir}/libjavaplugin.so \
    libjavaplugin.so %{_libdir}/gcj-`gij%{gccsuffix} --version | head -n 2 | tail -n 1 | awk '{ print $5 }'`/libgcjwebplugin.so %{priority}
} || :
%endif

%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%dir %{_libdir}/gcj
%doc AUTHORS ChangeLog COPYING INSTALL README
%dir %{_jvmdir}/%{sdkdir}
%dir %{jvmjardir}
%if ! %{custom}
%{_bindir}/rebuild-gcj-db
%{_bindir}/aot-compile
%{python_sitelib}/*
%endif
%{jvmjardir}/*.jar
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
# %{_jvmprivdir}/*
%if ! %{custom}
#%{_sysconfdir}/java/security/security.d/1000-gnu.java.security.provider.Gnu
%endif
%ifarch x86_64
%{_jvmdir}/%{jredir}/lib/amd64
%endif
%{_jvmdir}/%{jredir}/lib/%{_arch}/client
%{_jvmdir}/%{jredir}/lib/%{_arch}/server

%files devel -f %{name}-%{version}-sdk-bin.files
%defattr(-,root,root)
%doc
%dir %{_jvmdir}/%{sdkdir}/bin
%{_jvmdir}/%{sdkdir}/bin/native2ascii
%if ! %{custom}
%{_bindir}/aot-compile-rpm
%endif
%{_jvmdir}/%{sdkdir}/lib
%{_jvmdir}/%{sdkdir}/include
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%if %{custom}
%{_bindir}/ecj-%{cname}
%{_javadir}/eclipse-ecj-%{cname}.jar
%endif

%files src
%defattr(-,root,root)

%if %without bootstrap
%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
#%ghost %doc %{_javadocdir}/%{name}
#%ghost %doc %{_javadocdir}/java
%endif

%if %with plugin
%files plugin
%defattr(-,root,root)
%ghost %{plugindir}
%endif


