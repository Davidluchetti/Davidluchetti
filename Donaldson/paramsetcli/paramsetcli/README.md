<h1 align="center"><img src="https://www.informatica.com/content/dam/informatica-com/en/images/gl01/informatica-logo.png" alt="Informatica logo" /></h1>
A CLI tool to upload the Parameter Set to the cloud repository.

## What Is It?

Informatica's ParamSet CLI is a tool to perform these actions on a Parameter Set:
1. Upload a Parameter Set to the Cloud Repository.
2. Download the parameter Set from the Cloud Repository.
3. Delete the uploaded Parmater Set.
4. List all the Parameter Sets.

## Requirements

The following requirements exist for running Informatica's ParamSet CLI tool.

- Java Interpreter:

  A fully compliant Java Runtime Environment is required

- Java Compiler (*OPTIONAL*):

  A Java compiler is not needed since the distribution includes a
  precompiled Java binary archive.

## Installation Instructions

- Unzip the downloaded paramsetcli.zip in a suitable directory.

- The ParamSet CLI tool includes the following files:

  **restenv.properties** : Specifies login credentials.
  
  **log4j.properties** : Specifies the level of detail to return in log files.
  
  >**To customize the ParamSetCli properties, update existing restenv.properties and log4j.properties files.**

  **Login properties**

  Specify Cloud Services login credentials in the `restenv.properties` file. Or, you can include the login parameters as arguments in an action command.
  You can use a password string or an encrypted password for the password parameter value.
  
  To create an encrypted password, use one of the following commands:
  
  `./paramsetcli.sh encryptText -t <password>`
  
  `./paramsetcli.sh encryptText -text <password>`
  > **For Windows use the paramsetcli.bat**
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
  Copy the encrypted password string and replace the password in the restenv.properties file with the encrypted string, and then set the use.encryption flag to true.
  The following example shows the restenv.properties file with an encrypted password and the use.encryption flag set to true:
  ```properties                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
  baseUrl=https://dm-us.informaticacloud.com/ma
  username=dummy
  password=dummy
  ACTIVITYMONITORWAIT=2000
  PROXYHOST=
  PROXYPORT=
  RETRYCOUNT=
  use.encryption=false
  paramSetBaseUrl=https://na1.dm-us.informaticacloud.com/active-bpel
  ```

  Include the following parameters in the restenv.properties file or in action commands:
  ```properties
  Parameter         Description
  baseUrl           Base URL. Default is https://dm-us.informaticacloud.com/ma.
  username          Informatica Intelligent Cloud Services user name.
  password          Informatica Intelligent Cloud Services password or encrypted password string.
  use.encryption    Enables use of an encrypted password. To use an encrypted password, set the value to true.
  paramSetBaseUrl   ParamSet Base URL. Default is https://na1.dm-us.informaticacloud.com/active-bpel
  ```
## Running ParamSetCli

1. Change to the `paramsetcli` directory
2. To use the ParamSetCli tool, type the `runParamSetCli` command followed by arguments.
   The following string is the runParamSetCli command:
   
   `paramsetcli.bat runParamSetCli` or `paramsetcli.sh runParamSetCli`

   For each action, you must specify the action type to run.

   **Running the Cli commands:**

   The following command is an example of the syntax you can use to run an action using the action name.
   
   `paramsetcli.bat runParamSetCli -a <actionName>`                                                                                                                                                                                                                                                                                                                                                                                                         

   1. Upload a Parameter Set

        `paramsetcli.bat runParamSetCli -un <unique_name> -pf <parameter_file_name> -pd <parameter_dir> -a <action>`
        Example: `paramsetcli.bat runParamSetCli -un test -pf test.param -pd C:\\files -a upload`

   2. Download the Parameter Set

         `runParamSetCli -un <unique_name> -pf <parameter_file_name> -pd <parameter_dir> -a <action>`
         Example: `paramsetcli.bat runParamSetCli -un test -pf test.paramDownload -pd C:\\files -a download`

    3. Delete the Parameter Set

          `runParamSetCli -un <unique_name> -a <action>`
          Example: `paramsetcli.bat runParamSetCli -un test -a delete` 
          
    4. List the Parameter Sets
          `runParamSetCli -a list -page <page_number> -ps <page_size>`
          Example: `paramsetcli.bat runParamSetCli -a list -page 1 -ps 50`
          

## Thanks

**Thank you for using Informatica's Parameter Set Cli tool.**
