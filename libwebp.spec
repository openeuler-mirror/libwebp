Name:          libwebp
Version:       1.0.0
Release:       5
URL:           https://webmproject.org/
Summary:       Library and tools for the WebP graphics format
License:       BSD
Source0:       https://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz

Patch6000:  libwebp-fix-transcode-of-loop-count-to-65535.patch
Patch6001:  libwebp-fix-invalid-check-for-buffer-size.patch
Patch6002:  libwebp-Fix-for-thread-race-heap-use-after-free.patch
Patch6003:  libwebp-fix-riff-size-checks.patch
Patch6004:  libwebp-ChunkVerifyAndAssign-validate-chunk_size.patch
Patch6005:  libwebp-fix-alpha-filtering-crash-when-image-width-is-larger-than-radius.patch
Patch6006:  libwebp-fail-on-multiple-image-chunks.patch
Patch6007:  libwebp-fix-endian-problems-in-pattern-copy.patch
Patch6008:  libwebp-Fix-VP8IoTeardownHook-being-called-twice-on-worker-sync-failure.patch
Patch6009:  libwebp-fix-read-overflow-while-parsing-VP8X-chunk.patch
Patch6010:  libwebp-Make-sure-partition0-is-read-before-VP8-data-in-IDecode.patch
Patch6011:  libwebp-fix-rescaling-rounding-inaccuracy.patch
Patch6012:  libwebp-Allow-for-a-non-initialized-alpha-decompressor-in-DoRemap.patch
Patch6013:  libwebp-fix-rounding-error.patch

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
%doc README AUTHORS
%license COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}*.so
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
* Fri Mar 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0.0-5
- fix fuzz

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0.0-4
- delete unused patch

* Wed Sep 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.0-3
- Package init

