%define	module	PDL
%define	name	perl-%{module}
%define	version	2.4.4
%define release	%mkrel 2
%define	epoch	1

%define _provides_exceptions perl(Inline)
%define _requires_exceptions perl(\\(PDL\\|PGPLOT\\|Inline\\))

Summary:	PerlDL, an efficient numerical language for scientific computing
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	ftp://ftp.cpan.org/pub/perl/CPAN/modules/by-module/PDL/%{module}-%{version}.tar.gz
Source1:	PDL-convert-doc.pl.bz2
Patch1:		PDL-2.3.3-pic.patch
Patch2:		PDL-2.4.0-handle-INSTALLDIRS-vendor.patch
Patch4:		PDL-2.4.0-fix-gimp.patch
Patch5:		PDL-2.4.2-makemakerfix.patch
BuildRequires:	X11-devel
BuildRequires:	gcc-gfortran
BuildRequires:	ncurses-devel
BuildRequires:	perl-devel
BuildRequires:	MesaGLU-devel
BuildRequires:	perl-ExtUtils_F77 >= 1.14-11mdk
BuildRequires:	libgsl-devel
# mess installed files perms
# http://rt.cpan.org/Ticket/Display.html?id=40976
BuildConflicts: perl-ExtUtils-Install
# if installed, requires f2c-devel,
# but it is a contrib package
BuildConflicts: f2c
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
Buildroot:	%{_tmppath}/%{name}-%{version}

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
%setup -q -n %{module}-%{version}
%patch1 -p1 -b .pic
%patch2 -p1 -b .vendor
%patch4 -p0 -b .gimp
%patch5 -p0 -b .mm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix}
make OPTIMIZE="$RPM_OPT_FLAGS" PREFIX=%{_prefix}
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

