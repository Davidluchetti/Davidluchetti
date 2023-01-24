@echo off
pushd %~dp0
set PRG_DIR=%cd%

set CLASSPATH=%PRG_DIR%
set CLASSPATH=%CLASSPATH%;%PRG_DIR%\runAJobCli.jar
set CLASSPATH=%CLASSPATH%;%PRG_DIR%\lib\*

java -cp "%CLASSPATH%" -Duser.dir="%PRG_DIR%" com.informatica.saas.RestClient %*

popd
@echo on
