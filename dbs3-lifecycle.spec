### RPM cms dbs3-lifecycle 3.1.9
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES
## INITENV SET DBS3_LIFECYCLE_ROOT %i/
%define tag %(echo %{realversion} | sed 's/[.]/_/g; s/^/DBS_/')
Source0: git://github.com/giffels/DBS.git?obj=master/HEAD&export=LifeCycleTests-%{realversion}&output=/LifeCycleTests-%{realversion}.tar.gz
Requires: python dbs3-client lifecycle-dataprovider PHEDEX-lifecycle py2-cjson
BuildRequires: py2-sphinx

%prep
%setup -b 0 -n LifeCycleTests-%{realversion}

%build
python setup.py build_system -s LifeCycleTests

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s LifeCycleTests --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
