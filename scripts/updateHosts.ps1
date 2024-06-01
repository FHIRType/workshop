# Read the host file content
$Content = Get-Content -Path C:\Windows\system32\drivers\etc\hosts
$HostLine = "127.0.0.1 localhost api.localhost docs.localhost"

# Backup the contents
$Content | Set-Content -Path .\backup_hosts.txt

# Check if line exists
if ($Content -notcontains $HostLine) {
    # If not, add it
    $Content += $HostLine
    # Write the modified content back to the file
    $Content | Set-Content -Path C:\Windows\system32\drivers\etc\hosts
}