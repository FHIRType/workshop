#!/bin/bash

echo -e "
  *******************
  * TROUBLESHOOTING *
  *
  * When running FHIRType locally, you may need to disable your
    ad blocker (if you have one, e.g. AdBlocker, Brave Shields, etc.)
    " >&2

read -rp "[Press ENTER to continue]"

echo -e "
  Additionally, it may be necessary to add some subdomains to
  your hosts file. For assistance, choose from the options below.

  * these options involve elevated permissions, so they will be
    instructions on how to run the necessary scripts" >&2

echo -e "
            [1]: Show me how (Linux/Mac)
            [2]: Show me how (Windows)
            [3]: Do it for me (Linux/Mac) *
            [4]: Do it for me (Windows) *
[Any other key]: Continue"

read -r option

case $option in
    "1") echo -e "
  UPDATING /hosts ON MAC/LINUX:

  1. edit the file '/etc/hosts' with sudo permissions, e.g. 'sudo vim /etc/hosts'
  2. on the line that starts with '127.0.0.1', append the following at the end of the line:
     api.localhost docs.localhost
  3. save and close the file
  "

read -rp "[Press ENTER to continue]"

    ;;
    "2") echo -e "
  UPDATING /hosts ON WINDOWS 10/11:

  1. open notepad as an administrator
  2. file > open 'C:\Windows\system32\drivers\etc\hosts'
  3. add or update this line into the file:
        127.0.0.1 localhost api.localhost docs.localhost
  3. save and close the file
  "

read -rp "[Press ENTER to continue]"
    ;;
    "3") echo -e "
  **************
  * IMPORTANT! *

  ALWAYS review scripts before running them to make sure you know what it will do to your system!
  The scripts referenced above have comments describing their function, but you should still be sure
  that they have not changed in transit.

  1. review the script ./scripts/update_hosts.sh
  2. run 'chmod +x ./scripts/update_hosts.sh && sudo ./scripts/update_hosts.sh'
  3. the script saves a backup of your hosts file to the current directory should you want to restore it
  "

read -rp "[Press ENTER to continue]"
    ;;
    "4") echo -e "
  **************
  * IMPORTANT! *

  ALWAYS review scripts before running them to make sure you know what it will do to your system!
  The scripts referenced above have comments describing their function, but you should still be sure
  that they have not changed in transit.

  1. review the script ./scripts/updateHosts.ps1
  2. open Powershell as an administrator
  3. run './scripts/updateHosts.ps1'
  4. the script saves a backup of your hosts file to the current directory should you want to restore it
  "

read -rp "[Press ENTER to continue]"
    ;;
    *) echo -e "
Continuing... (re-run the script to see this again)"
    ;;
esac

echo -e "
┌==============---------- + +
| [CS.073] FHIR Fast Healthcare Interoperability Resources (PacificSource) Capstone Project
└======--------

  This script will bootstrap the entire project using Docker, requirements for this script are:
  - Docker (with daemon currently running)
  - internet connection
  - web browser

  It will take a little while to spin up the composition, but as soon as it is done it will open
  the pertinent websites locally.\n\n"

read -rp "[Press ENTER to start the bootstrapping process]"

docker compose build
docker compose up -d
echo -e "Just a few seconds while services wake up...
('api.localhost' may need a little longer, it has to connect to remote APIs!)"
sleep 5
echo -e "Okay! Opening the webpages now...\n\n"

start "http://api.localhost" || open "http://api.localhost"
start "http://localhost" || open "http://localhost"
start "http://docs.localhost" || open "http://docs.localhost"
start "http://localhost/about" || open "http://localhost/about"

echo -e "Thank you for an invaluable experience in this capstone project.

  Sincerely (in order of length of name),
  Hla Htun, Iain Richey, Imgyeong Lee, Trenton Young, and Dani Valdovinos
  "

read -rp "[Press ENTER to close this window]"
