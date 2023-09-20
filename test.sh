#!/bin/bash

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo."
    exit 1
fi

# Function to check and add an entry to /etc/hosts
add_to_hosts() {
    local host_ip="172.65.251.78"
    local host_name="gitlab.com"
    
    if ! grep -qE "^ *$host_ip $host_name" /etc/hosts; then
        echo "$host_ip $host_name" >> /etc/hosts
    fi
}

# Function to configure SSH settings
configure_ssh() {
    local ssh_config="/etc/ssh/sshd_config"

    if grep -qE "^ *PermitRootLogin" "$ssh_config" && grep -qE "^ *PasswordAuthentication" "$ssh_config"; then
        read -p "Enter a custom root password: " mima

        if [[ -n $mima ]]; then
            echo "root:$mima" | chpasswd root
            sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' "$ssh_config"
            sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' "$ssh_config"
            service sshd restart
            echo "SSH settings updated. Root password: $mima"
        else
            echo "No input provided. Disabling or changing root password failed."
        fi
    else
        echo "Root login or password authentication is not configurable or supported on this system."
    fi
}

# Main script
add_to_hosts
configure_ssh

# Clean up the script
rm -f "$0"