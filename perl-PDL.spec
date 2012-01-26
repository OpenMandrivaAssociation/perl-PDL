%define	module	PDL
%define	upstream_version 2.4.9

%define Werror_cflags %nil
%define _provides_exceptions perl(Inline)
%define _requires_exceptions perl(\\(PDL\\|PGPLOT\\|Inline\\))

Name:		perl-%{module}
Version:	%perl_convert_version %{upstream_version}
Release:	5
Epoch:		1

Summary:	PerlDL, an efficient numerical language for scientific computing
License:	GPL
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{module}/
Source0:	ftp://ftp.cpan.org/pub/perl/CPAN/modules/by-module/PDL/%{module}-%{upstream_version}_995.tar.gz
Source1:	PDL-convert-doc.pl.bz2
Patch1:		PDL-2.4.4-fpic.patch
Patch2:		PDL-2.4.4-handle-INSTALLDIRS-vendor.patch
Patch4:		PDL-2.4.0-fix-gimp.patch
Patch5:		PDL-2.4.2-makemakerfix.patch

BuildRequires:	perl(Astro::FITS::Header)
BuildRequires:	perl(Convert::UU)
BuildRequires:	perl(Data::Dumper) >= 2.121.0
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec) >= 0.600.0
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Filter::Util::Call)
BuildRequires:	perl(Inline) >= 0.430.0
BuildRequires:	perl(OpenGL) >= 0.630.0
BuildRequires:	perl(Pod::Parser)
BuildRequires:	perl(Pod::Select)
BuildRequires:	perl(Storable) >= 1.30.0
BuildRequires:	perl(Text::Balanced)
BuildRequires:	gcc-gfortran
BuildRequires:	libgsl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	pkgconfig(glut)
BuildRequires:	ncurses-devel
BuildRequires:	perl-devel
BuildRequires:	perl-ExtUtils_F77 >= 1.14-11mdk
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxi-devel
BuildRequires:	libxmu-devel
# if installed, requires f2c-devel,
# but it is a contrib package
BuildConflicts:	f2c

Provides:	perl(PDL::PP::CType)  
Provides:	perl(PDL::PP::Dims)  
Provides:	perl(PDL::PP::PDLCode)
Provides:	perl(PDL::PP::SymTab)
Provides:	perl(PDL::PP::XS)
Provides:	perl(PDL::Config)
Provides:	perl(PDL::Graphics::OpenGL)
Provides:	perl(PDL::Graphics::OpenGLQ)
Provides:	perl(PDL::Graphics::TriD::GL)
Provides:	perl(PDL::Graphics::TriD::Objects)
Provides:	perl(PDL::Lite)
Provides:	perl(PDL::LiteF)

%rename		PDL

%package	doc
Summary:	PerlDL documentation package
Group:		Books/Computer books
Requires:	perl-PDL

%description
The perlDL project aims to turn perl into an efficient numerical language for
scientific computing. The PDL module gives standard perl the ability to
COMPACTLY store and SPEEDILY manipulate the large N-dimensional data sets which
are the bread and butter of scientific computing. e.g. C<$a=$b+$c> can add two
2048x2048 images in only a fraction of a second.

The aim is to provide tons of useful functionality for
scientific and numeric analysis.

%description	doc
The perlDL project aims to turn perl into an efficient numerical language for
scientific computing. The PDL module gives standard perl the ability to
COMPACTLY store and SPEEDILY manipulate the large N-dimensional data sets which
are the bread and butter of scientific computing. e.g. C<$a=$b+$c> can add two
2048x2048 images in only a fraction of a second.

The aim is to provide tons of useful functionality for
scientific and numeric analysis.

This is the documentation package.

%prep
%setup -q -n %{module}-%{upstream_version}_995
%patch1 -p1 -b .pic
%patch2 -p1 -b .vendor
%patch4 -p0 -b .gimp
%patch5 -p0 -b .mm

%build
echo | %{__perl} Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix} OPTIMIZE="%{optflags} -fpermissive"

# -Wformat -Werror=format-security is inherited from something, remove it.
# note. it builds just fine on a real system but NOT in the build system. it gives:
# [...]
# GD.xs: In function 'pdl_write_png_readdata':
# GD.xs:241:5: error: format not a string literal and no format arguments [-Werror=format-security]
# GD.xs:256:9: error: format not a string literal and no format arguments [-Werror=format-security]
# [...]

find Makefile | xargs perl -pi -e "s|-Wformat||g"
find Makefile | xargs perl -pi -e "s|-Werror=format-security||g"

make
#DISPLAY="" make test

# first generate blib/lib/PDL/pdldoc.db
make doctest
# 

%install
%makeinstall PREFIX="%{buildroot}/%{_prefix}"

# create /usr/bin if it doesn't already exist
%{__mkdir_p} %{buildroot}%{_bindir}

# fix installed documentation
%{__bzip2} -dc %{SOURCE1} | %{__perl} - "%{buildroot}"

%files
%doc COPYING Changes DEPENDENCIES Known_problems
%doc README DEVELOPMENT INSTALL TODO BUGS META.yml
%{_bindir}/*
%{_mandir}/*/*
%{perl_vendorarch}/PDL.pm
%{perl_vendorarch}/PDL
%{perl_vendorarch}/auto/PDL
%{perl_vendorarch}/Inline
%exclude %{perl_vendorarch}/PDL/*.pod
%exclude %{perl_vendorarch}/PDL/HtmlDocs

%files doc
%doc COPYING
%{perl_vendorarch}/PDL/*.pod
%{perl_vendorarch}/PDL/HtmlDocs
