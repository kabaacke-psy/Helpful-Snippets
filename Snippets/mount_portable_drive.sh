# @Authors: 
#   Kyle Baacke; kbaacke2@illinois.edu; https://github.com/kabaacke-psy
# @DateCreated: 02/07/2022
# @DateUpdated: 02/07/2022
# Description:
#   {DESCRIPTION}
# Notes and Qualifiers:
#   {NOTES}

# Use lsblk to check where the portable drive is in /dev
lsblk
# This can change when the system is rebooted

# Mount the device to an EXISTING directory
# The target directory should be in your home directory unless you want to share that path with other users.
# If you want to share the mounted fie directory, check with the sysadmin
# Example to mount to a device to a shared directory with wheel privilages
sudo mount /dev/sda2 /mnt/usb1

# You can check the contents of the device you just mounted using the ls command.
ls /mnt/usb1