Name:          libwebp
Version:       1.3.0
Release:       1
URL:           http://www.linuxfromscratch.org/blfs/view/svn/general/libwebp.html
Summary:       Library and tools for the WebP graphics format
License:       BSD
Source0:       http://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz

Patch6000:     libwebp-freeglut.patch

BuildRequires: libjpeg-devel libpng-devel giflib-devel libtiff-devel
BuildRequires: java-devel jpackage-utils swig freeglut-devel
BuildRequires: autoconf automake libtool

%description
This is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package       tools
Summary:       The WebP command line tools

%description   tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package       devel
Summary:       Development files for libwebp
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
Development files for libwebp, a library for the WebP format

%package       java
Summary:       Java bindings for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      java-headless jpackage-utils

%description   java
Java bindings for libwebp.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -vif
%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif
%configure  --enable-libwebpmux --enable-libwebpdemux \
            --enable-libwebpdecoder --disable-neon
%make_build

cd swig
rm -rf libwebp.jar libwebp_java_wrap.c
install -d java/com/google/webp
swig -ignoremissing -I../src -java \
    -package com.google.webp  \
    -outdir java/com/google/webp \
    -o libwebp_java_wrap.c libwebp.swig

gcc %{__global_ldflags} %{optflags} -shared \
    -I/usr/lib/jvm/java/include \
    -I/usr/lib/jvm/java/include/linux \
    -I../src \
    -L../src/.libs -lwebp libwebp_java_wrap.c \
    -o libwebp_jni.so

cd java
javac com/google/webp/libwebp.java
jar cvf ../libwebp.jar com/google/webp/*.class

%install
%make_install
install -d %{buildroot}/%{_libdir}/%{name}-java
cp swig/*.jar swig/*.so %{buildroot}/%{_libdir}/%{name}-java/
%delete_la
%ldconfig_scriptlets

%files tools
%defattr(-,root,root)
%{_bindir}/*

%files -n %{name}
%defattr(-,root,root)
%doc README.md AUTHORS
%license COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}*.so
%{_libdir}/libsharpyuv.so
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*

%files java
%defattr(-,root,root)
%{_libdir}/%{name}-java/

%files help
%defattr(-,root,root)
%doc NEWS PATENTS
%{_mandir}/man*/*

%changelog
* Fri Feb 03 2023 zhouwenpei <zhouwenpei1@h-partners.com> - 1.3.0-1
- update to 1.3.0

* Wed Oct 26 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 1.2.1-2
- Rebuild for next release

* Wed Dec 01 2021 wangkerong <wangkerong@huawei.com> - 1.2.1-1
- update to 1.2.1

* Wed Dec 16 2020 hanhui <hanhui15@huawei.com> - 1.1.0-3
- modify url

* Thu Sep 10 2020 zhanzhimin <zhanzhimin@huawei.com> - 1.1.0-2
- update Source

* Wed Apr 15 2020 fengtao<fengtao40@huawei.com> - 1.1.0-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 1.1.0

* Fri Mar 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0.0-5
- fix fuzz

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0.0-4
- delete unused patch

* Wed Sep 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.0-3
- Package init
