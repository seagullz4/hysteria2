#!/bin/bash

# Create a systemd service for Hysteria Server

# Define service unit file path
SERVICE_FILE="/etc/systemd/system/hysteria.service"

# Define your command and working directory
COMMAND="/root/hy3/hysteria-linux-amd64 server"
WORKING_DIR="/root/hy3/"

# Create the service unit file
cat > "$SERVICE_FILE" <<EOL
[Unit]
Description=Hysteria Server

[Service]
ExecStart=$COMMAND
WorkingDirectory=$WORKING_DIR
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Enable and start the service
systemctl daemon-reload
systemctl enable hysteria.service
systemctl start hysteria.service

echo "Hysteria Server systemd service has been created and started."