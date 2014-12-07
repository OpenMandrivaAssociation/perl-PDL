%define	modname	PDL
%define	modver	2.007

%define Werror_cflags %nil
%if %{_use_internal_dependency_generator}
%define __noautoprov 'perl\\(Inline\\)'
%define __noautoreq 'perl\\(PDL\\)|perl\\(PGPLOT\\)|perl\\(Inline\\)|perl\\(Devel::REPL::Plugin\\)|perl\\(OpenGL::Config\\)|perl\\(Win32::DDE::Client\\)|perl\\(Module::Compile\\)|perl\\(PDL::Demos::Screen\\)|perl\\(PDL::Graphics::Gnuplot\\)|perl\\(Prima::MsgBox\\)'
%else
%define _provides_exceptions perl(Inline)
%define _requires_exceptions perl(\\(PDL\\|PGPLOT\\|Inline\\|Module::Compile\\|PDL::Demos::Screen\\|PDL::Graphics::Gnuplot\\|Prima::MsgBox\\))
%endif

Summary:	PerlDL, an efficient numerical language for scientific computing
Name:		perl-%{modname}
Epoch:		1
Version:	%perl_convert_version %{modver}
Release:	4
License:	GPLv2
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{modname}/
Source0:	ftp://ftp.cpan.org/pub/perl/CPAN/modnames/by-modname/PDL/%{modname}-%{modver}.tar.gz
Source1:	PDL-convert-doc.pl.bz2
Source100:	%{name}.rpmlintrc
Patch1:		PDL-2.4.4-fpic.patch
Patch2:		PDL-2.4.4-handle-INSTALLDIRS-vendor.patch
Patch4:		PDL-2.4.0-fix-gimp.patch
Patch5:		PDL-2.4.2-makemakerfix.patch
Patch6:		PDL-2.007-no-Proj.patch
BuildRequires:	perl(Astro::FITS::Header)
BuildRequires:	perl(Convert::UU)
BuildRequires:	perl(Data::Dumper) >= 2.121.0
BuildRequires:	perl(ExtUtils::F77)
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
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xmu)
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
scientific computing. The PDL modname gives standard perl the ability to
COMPACTLY store and SPEEDILY manipulate the large N-dimensional data sets which
are the bread and butter of scientific computing. e.g. C<$a=$b+$c> can add two
2048x2048 images in only a fraction of a second.

The aim is to provide tons of useful functionality for
scientific and numeric analysis.

%description	doc
The perlDL project aims to turn perl into an efficient numerical language for
scientific computing. The PDL modname gives standard perl the ability to
COMPACTLY store and SPEEDILY manipulate the large N-dimensional data sets which
are the bread and butter of scientific computing. e.g. C<$a=$b+$c> can add two
2048x2048 images in only a fraction of a second.

The aim is to provide tons of useful functionality for
scientific and numeric analysis.

This is the documentation package.

%prep
%setup -qn %{modname}-%{modver}
%patch1 -p1 -b .pic
%patch2 -p1 -b .vendor
%patch4 -p0 -b .gimp
%patch5 -p0 -b .mm
%patch6 -p1 -b .proj

%build
echo | %__perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix} OPTIMIZE="%{optflags} -fpermissive"

# -Wformat -Werror=format-security is inherited from something, remove it.
# note. it builds just fine on a real system but NOT in the build system. it gives:
# [...]
# GD.xs:	In function 'pdl_write_png_readdata':
# GD.xs:241:5:	error:	format not a string literal and no format arguments [-Werror=format-security]
# GD.xs:256:9:	error:	format not a string literal and no format arguments [-Werror=format-security]
# [...]

find Makefile | xargs perl -pi -e "s|-Wformat||g"
find Makefile | xargs perl -pi -e "s|-Werror=format-security||g"

make
#DISPLAY="" make test

%install
make install PREFIX="%{buildroot}/%{_prefix}"

# create /usr/bin if it doesn't already exist
mkdir -p %{buildroot}%{_bindir}

# fix installed documentation
bzip2 -dc %{SOURCE1} | %__perl - "%{buildroot}"

%files
%doc COPYING Changes DEPENDENCIES Known_problems
%doc README DEVELOPMENT INSTALL TODO META.yml
%{_bindir}/*
%{perl_vendorarch}/PDL.pm
%{perl_vendorarch}/PDL
%{perl_vendorarch}/auto/PDL
%{perl_vendorarch}/Inline
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{perl_vendorarch}/PDL/*.pod
%exclude %{perl_vendorarch}/PDL/HtmlDocs

%files doc
%doc COPYING
%{perl_vendorarch}/PDL/*.pod
%{perl_vendorarch}/PDL/HtmlDocs

