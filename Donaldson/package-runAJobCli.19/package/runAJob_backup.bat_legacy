@echo off
set SCRIPT_DIR=%~dp0.
 
@pushd %SCRIPT_DIR%
@pushd ..\..\
@set AGENT_DIR_NAME=%cd%
@popd
@popd
 
IF EXIST "%AGENT_DIR_NAME%\apps\runAJobCli" (
  echo " Backup is required and in progress..."
  cd /d "%AGENT_DIR_NAME%\apps"
  xcopy runAJobCli runAJobCli_bak /e /y /i
  cd /d "%SCRIPT_DIR%"
) ELSE (
        echo "%AGENT_DIR_NAME%\apps\runAJobCli" "File doesn't exist:"
)
echo "Done"