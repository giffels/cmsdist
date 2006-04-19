### RPM cms prodagent PRODAGENT_0_0_4
## INITENV +PATH PYTHONPATH %i/lib
## INITENV SET PRODAGENT_HOME %i
## INITENV SET PRODAGENT_CONFIG %i/etc/ProdAgentConfig.xml
## INITENV SET PRODAGENT_WORKDIR %i/workdir

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
Requires: python mysql py2-mysqldb dbs dls boss

%prep
%setup -n PRODAGENT
%build
%install
make PREFIX=%i install
mkdir -p %{i}/etc/profile.d
mkdir -p %i/workdir

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_ROOT/etc/profile.d/init.sh"; \
 echo "source $DLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $BOSS_ROOT/etc/profile.d/init.sh")  > %i/etc/profile.d/dependencies-setup.sh

cat << \EOF_DEPENDENCIES_SETUP_CSH > %{i}/etc/profile.d/dependencies-setup.csh
#!/bin/tcsh
source $PYTHON_ROOT/etc/profile.d/init.csh
source $MYSQL_ROOT/etc/profile.d/init.csh
source $PY2_MYSQLDB_ROOT/etc/profile.d/init.csh
source $DBS_ROOT/etc/profile.d/init.csh
source $DLS_ROOT/etc/profile.d/init.csh
source $BOSS_ROOT/etc/profile.d/init.csh
EOF_DEPENDENCIES_SETUP_CSH

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
