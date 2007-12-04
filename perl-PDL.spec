%define	module	PDL
%define	name	perl-%{module}
%define	version	2.4.3
%define release	%mkrel 1
%define	epoch	1

Summary:	PerlDL, an efficient numerical language for scientific computing
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Perl
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://search.cpan.org/dist/%{module}/
Source0:	ftp://ftp.cpan.org/pub/perl/CPAN/modules/by-module/PDL/%{module}-%{version}.tar.bz2
Source1:	PDL-convert-doc.pl.bz2
Patch1:		PDL-2.3.3-pic.patch
Patch2:		PDL-2.4.0-handle-INSTALLDIRS-vendor.patch
Patch4:		PDL-2.4.0-fix-gimp.patch
Patch5:		PDL-2.4.2-makemakerfix.patch
BuildRequires:	X11-devel gcc-gfortran ncurses-devel perl-devel MesaGLU-devel
BuildRequires:	perl-ExtUtils_F77 >= 1.14-11mdk
BuildRequires:	libgsl-devel
Obsoletes:	PDL
Provides:	PDL

%define _requires_exceptions perl(PDL\\|perl(PGPLOT

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
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX="$RPM_BUILD_ROOT/%{_prefix}"

# create /usr/bin if it doesn't already exist
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}

# fix installed documentation
%{__bzip2} -dc %{SOURCE1} | %{__perl} - "$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING Changes DEPENDENCIES Known_problems README DEVELOPMENT INSTALL TODO BUGS
%{_bindir}/*
%{_mandir}/*/*
%{perl_vendorarch}/auto/PDL
%{perl_vendorarch}/PDL.pm*
%{perl_vendorarch}/Inline
%dir %{perl_vendorarch}/PDL
%{perl_vendorarch}/PDL/default.perldlrc
%{perl_vendorarch}/PDL/pdldoc.db
%{perl_vendorarch}/PDL/*.pm*
%{perl_vendorarch}/PDL/Core
%{perl_vendorarch}/PDL/Demos
%{perl_vendorarch}/PDL/Doc
%{perl_vendorarch}/PDL/Filter
%{perl_vendorarch}/PDL/Fit
%{perl_vendorarch}/PDL/Graphics
%{perl_vendorarch}/PDL/GSL
%{perl_vendorarch}/PDL/GSLSF
%{perl_vendorarch}/PDL/IO
%{perl_vendorarch}/PDL/Opt
%{perl_vendorarch}/PDL/Pod
%{perl_vendorarch}/PDL/PP
%{perl_vendorarch}/PDL/Transform

%files doc
%defattr(-,root,root)
%doc COPYING
%{perl_vendorarch}/PDL/*.pod
%{perl_vendorarch}/PDL/HtmlDocs

