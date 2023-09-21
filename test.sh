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
    local ssh_log="/var/log/auth.log"
    local ssh_failed_logins=0
    local ssh_login_successful=false

    if grep -qE "^ *PermitRootLogin" "$ssh_config" && grep -qE "^ *PasswordAuthentication" "$ssh_config"; then
        read -p "Enter a custom root password: " mima

        if [[ -n $mima ]]; then
            echo "root:$mima" | chpasswd root
            sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' "$ssh_config"
            sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' "$ssh_config"
            service ssh restart
            echo "SSH settings updated. Root password: $mima"
        else
            echo "No input provided. Disabling or changing root password failed."
        fi
    else
        echo "Root login or password authentication is not configurable or supported on this system."
    fi

    # Monitor SSH login failures, but only if successful login hasn't occurred yet
    while ! $ssh_login_successful; do
        if [[ -f "$ssh_log" ]]; then
            local failed_attempts=$(grep "sshd.*Failed password" "$ssh_log" | wc -l)
            
            if [[ $failed_attempts -ge 3 ]]; then
                echo "SSH login failed 3 times. Reverting to original SSH settings."
                sed -i 's/^PermitRootLogin.*/#PermitRootLogin/' "$ssh_config"
                sed -i 's/^PasswordAuthentication.*/#PasswordAuthentication/' "$ssh_config"
                service ssh restart
                break
            fi
        fi
        sleep 60 # Check every minute
    done
}

# Main script
add_to_hosts
configure_ssh

# Clean up the script
rm -f "$0"