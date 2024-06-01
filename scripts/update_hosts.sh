#!/bin/bash
# Hosts file path
hosts_file="/etc/hosts"

# Line to add to hosts file
host_line="127.0.0.1 localhost api.localhost docs.localhost"

# Backup hosts file
cp $hosts_file ./backup_hosts.txt

# Check if line exists
if ! grep -Fxq "$host_line" $hosts_file
then
  # If not, add it
  echo "$host_line" | sudo tee -a $hosts_file
fi