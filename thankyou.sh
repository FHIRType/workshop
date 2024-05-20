#!/bin/bash
echo -e "  [CS.073] FHIR Fast Healthcare Interoperability Resources (PacificSource) Capstone Project
  --------

  This script will bootstrap the entire project using Docker, requirements for this script are:
  - Docker
  - internet connection
  - web browser

  It will take a little while to spin up the composition, but as soon as it is done it will open the pertinent websites.\n\n"

read -p "[Press ENTER to start the bootstrapping process]"

docker compose build && \
docker compose up -d && \
echo "Just a few seconds while services wake up...\n('api.localhost' may need a little longer, it has to connect to remote APIs!)" && \
sleep 5 && \
echo -e "Okay! Opening the webpages now...\n\n"

start "http://api.localhost" || open "http://api.localhost"
start "http://localhost" || open "http://localhost"
start "http://docs.localhost" || open "http://docs.localhost"

echo -e "Thank you for an invaluable experience in this capstone project.

  Sincerely,
  Trenton Young, Imgyeong Lee, Hla Htun, Dani Valdovinos, and Iain Richey\n\n\n"

read -p "[Press ENTER to close this window]"
