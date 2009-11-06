%define	upstream_name	 PDL
%define upstream_version 2.4.5

%define Werror_cflags %nil
%define _provides_exceptions perl(Inline)
%define _requires_exceptions perl(\\(PDL\\|PGPLOT\\|Inline\\))

Name:       perl-%{upstream_name}
Version:    %perl_convert_version %{upstream_version}
Release:    %mkrel 4
Epoch:		1

Summary:	PerlDL, an efficient numerical language for scientific computing
License:	GPL
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{upstream_name}/
Source0:	ftp://ftp.cpan.org/pub/perl/CPAN/modules/by-module/PDL/%{upstream_name}-%{upstream_version}.tar.gz
Source1:	PDL-convert-doc.pl.bz2
Patch0:		PDL-2.4.4-fix-format-errors.patch
Patch1:		PDL-2.4.4-fpic.patch
Patch2:		PDL-2.4.4-handle-INSTALLDIRS-vendor.patch
Patch4:		PDL-2.4.0-fix-gimp.patch
Patch5:		PDL-2.4.2-makemakerfix.patch

BuildRequires:	gcc-gfortran
BuildRequires:	libgsl-devel
BuildRequires:	MesaGLU-devel
BuildRequires:	ncurses-devel
BuildRequires:	perl-devel
BuildRequires:	perl-ExtUtils_F77 >= 1.14-11mdk
BuildRequires:	X11-devel
# mess installed files perms
# http://rt.cpan.org/Ticket/Display.html?id=40976
BuildConflicts: perl-ExtUtils-Install
# if installed, requires f2c-devel,
# but it is a contrib package
BuildConflicts: f2c

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}

Provides:       perl(PDL::PP::CType)  
Provides:       perl(PDL::PP::Dims)  
Provides:       perl(PDL::PP::PDLCode)
Provides:       perl(PDL::PP::SymTab)
Provides:       perl(PDL::PP::XS)
Provides:       perl(PDL::Config)
Provides:       perl(PDL::Graphics::OpenGL)
Provides:       perl(PDL::Graphics::OpenGLQ)
Provides:       perl(PDL::Graphics::TriD::GL)
Provides:       perl(PDL::Graphics::TriD::Objects)
Provides:       perl(PDL::Lite)
Provides:       perl(PDL::LiteF)

Obsoletes:	PDL
Provides:	PDL

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
%setup -q -n %{upstream_name}-%{upstream_version}
%patch0 -p1 -b .format
%patch1 -p1 -b .pic
%patch2 -p1 -b .vendor
%patch4 -p0 -b .gimp
%patch5 -p0 -b .mm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix} OPTIMIZE="%{optflags}"
make
#DISPLAY="" make test

# first generate blib/lib/PDL/pdldoc.db
make doctest
# 

%install
rm -rf %{buildroot}
%makeinstall PREFIX="%{buildroot}/%{_prefix}"

# create /usr/bin if it doesn't already exist
%{__mkdir_p} %{buildroot}%{_bindir}

# fix installed documentation
%{__bzip2} -dc %{SOURCE1} | %{__perl} - "%{buildroot}"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING Changes DEPENDENCIES Known_problems
%doc README DEVELOPMENT INSTALL TODO BUGS
%{_bindir}/*
%{_mandir}/*/*
%{perl_vendorarch}/PDL.pm
%{perl_vendorarch}/PDL
%{perl_vendorarch}/auto/PDL
%{perl_vendorarch}/Inline
%exclude %{perl_vendorarch}/PDL/*.pod
%exclude %{perl_vendorarch}/PDL/HtmlDocs

%files doc
%defattr(-,root,root)
%doc COPYING
%{perl_vendorarch}/PDL/*.pod
%{perl_vendorarch}/PDL/HtmlDocs
