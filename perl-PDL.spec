%define	module	PDL
%define	upstream_version 2.4.9

%define Werror_cflags %nil
%if %{_use_internal_dependency_generator}
%define __noautoprov 'perl\\(Inline\\)'
%define __noautoreq 'perl\\(PDL\\)|perl\\(PGPLOT\\)|perl\\(Inline\\)|perl\\(Devel::REPL::Plugin\\)|perl\\(OpenGL::Config\\)|perl\\(Win32::DDE::Client\\)'
%else
%define _provides_exceptions perl(Inline)
%define _requires_exceptions perl(\\(PDL\\|PGPLOT\\|Inline\\))
%endif

Name:		perl-%{module}
Version:	%perl_convert_version %{upstream_version}
Release:	14
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
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	perl-devel
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
echo | %__perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix} OPTIMIZE="%{optflags} -fpermissive"

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
%__mkdir_p %{buildroot}%{_bindir}

# fix installed documentation
%__bzip2 -dc %{SOURCE1} | %__perl - "%{buildroot}"

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


%changelog
* Thu Jan 26 2012 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 1:2.4.9-5
+ Revision: 769200
- fix buildrequires
- sync buildrequires with mageia
- clean up package
- svn commit -m mass rebuild of perl extension against perl 5.14.2

  + Oden Eriksson <oeriksson@mandriva.com>
    - "fix" build...
    - try a newer pre-release version
    - fix deps
    - rebuilt for perl-5.14.2
    - rebuilt for perl-5.14.x

* Fri Jun 17 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.4.9-1
+ Revision: 685795
- new version

* Wed Apr 06 2011 Sandro Cazzaniga <kharec@mandriva.org> 1:2.4.8-1
+ Revision: 650968
- remove one BR
- new version 2.4.8

  + Funda Wang <fwang@mandriva.org>
    - tighten BR

* Tue Aug 31 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1:2.4.7-2mdv2011.0
+ Revision: 574711
- extract prereqs from meta.yml

* Mon Aug 23 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1:2.4.7-1mdv2011.0
+ Revision: 572270
- update to 2.4.7

* Mon Aug 02 2010 Funda Wang <fwang@mandriva.org> 1:2.4.6-2mdv2011.0
+ Revision: 564958
- rebuild

* Sun Jan 03 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1:2.4.6-1mdv2011.0
+ Revision: 485845
- upstream ticket 40976 (wrong file perms) seems to be fixed with extutils::makemaker 1.54
- update to 2.4.6

* Fri Nov 06 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1:2.4.5-1mdv2010.1
+ Revision: 461922
- reset mkrel
- fix typo in buildrequires:
- adding missing buildrequires:
- update to 2.4.5

* Mon Aug 03 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1:2.4.4-4mdv2010.0
+ Revision: 407963
- rebuild using %%perl_convert_version

* Tue May 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.4.4-3mdv2010.0
+ Revision: 377789
- rediff patches 1 and 2
- fix format errors in C code
- drop format errors check because of XS code

* Fri Nov 21 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.4.4-2mdv2009.1
+ Revision: 305430
- fix dependencies
- new version
  fix automatic dependencies (should not provide perl(Inline))

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1:2.4.3-3mdv2009.0
+ Revision: 265431
- rebuild early 2009.0 package (before pixel changes)

* Wed Apr 16 2008 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1:2.4.3-2mdv2009.0
+ Revision: 194734
- fixing build on new perl (bug 40056)

  + Pixel <pixel@mandriva.com>
    - rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Sat May 05 2007 Olivier Thauvin <nanardon@mandriva.org> 1:2.4.3-1mdv2008.0
+ Revision: 23213
- 2.4.3


* Thu Apr 20 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1:2.4.2-5mdk
- Remove a lot of internal automatic requires

* Thu Apr 20 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1:2.4.2-4mdk
- Don't gzip modules
- Fix for rebuild with 5.8.8

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.4.2-3mdk
- Rebuild

* Tue Jun 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.4.2-2mdk
- Use gfortran instead of g77

* Tue Jan 11 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4.2-1mdk
- 2.4.2
- Drop patch 3, merged upstream

* Fri Dec 24 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.4.1-4mdk
- Removed dependency on Mesa (bug #12798)

* Mon Nov 15 2004 Götz Waschk <waschk@linux-mandrake.com> 2.4.1-3mdk
- disable parallel build
- rebuild for new perl

* Mon Jun 28 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.4.1-2mdk
- BuildRequires: libgsl-devel

* Wed Apr 21 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.4.1-1mdk
- 2.4.1
- use %%make macro
- spec cosmetics

* Fri Aug 08 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.0-4mdk
- BuildRequires: libncurses-devel, libMesaGLU-devel as any of them
  should work

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.4.0-3mdk
- drop Prefix tag, use %%{_prefix}

* Thu Jun 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.0-2mdk
- fix provides

* Thu Jun 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.0-1mdk
- new release
- rediff patch 2
- patch 4: fix build of gimp gratuitously broken by fpons_sucks
- fix unpackaged files

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.3.4-3mdk
- rebuild for new auto{prov,req}

