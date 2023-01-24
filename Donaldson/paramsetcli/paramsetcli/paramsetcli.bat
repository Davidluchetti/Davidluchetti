@echo off
pushd %~dp0
set PRG_DIR=%cd%

set CLASSPATH=%PRG_DIR%
set CLASSPATH=%CLASSPATH%;%PRG_DIR%\com.activee.rt.hub.tf.paramset.cli.jar


java -cp "%CLASSPATH%" -Duser.dir="%PRG_DIR%" com.activee.rt.hub.tf.paramset.cli.AeParamSetCliApp %*

popd
@echo on
