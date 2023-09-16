#!/bin/bash

# Define commands to install
commands=("wget" "netstat" "sed" "openssl")

# Function to install missing commands
install_missing_commands() {
  for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &>/dev/null; then
      echo "Installing $cmd..."
      if [ "$(id -u)" -ne 0 ]; then
        sudo_cmd="sudo"
      else
        sudo_cmd=""
      fi

      if [ -x "$(command -v apt)" ]; then
        # Ubuntu/Debian
        $sudo_cmd apt update
        $sudo_cmd apt install -y "$cmd"
      elif [ -x "$(command -v yum)" ]; then
        # CentOS/RHEL
        $sudo_cmd yum install -y "$cmd"
      else
        echo "Unsupported package manager."
        exit 1
      fi

      if [ $? -eq 0 ]; then
        echo "$cmd installed successfully."
      else
        echo "Failed to install $cmd."
      fi
    else
      echo "$cmd is already installed."
    fi
  done
}

# Install missing commands
install_missing_commands

echo "Command installation complete."

# Detect system architecture
echo "正在识别系统架构中，请稍候……"
arch=$(uname -m)

if [ "$arch" == "x86_64" ] || [ "$arch" == "amd64" ]; then
  echo "识别成功！为 x86_64/amd64 架构，正在运行对应命令……"
  script_url="https://github.com/seagullz4/hysteria2/raw/main/hy2amd.sh"
elif [ "$arch" == "aarch64" ]; then
  echo "识别成功！为 arm64 架构，正在运行对应命令……"
  script_url="https://github.com/seagullz4/hysteria2/raw/main/hy2arm.sh"
else
  echo "不支持的架构: $arch"
  exit 1
fi

# Download the script
if wget -O hysteria2-install-script.sh "$script_url"; then
  chmod +x hysteria2-install-script.sh
  echo "下载并授予脚本执行权限成功。"
else
  echo "下载脚本失败。退出。"
  exit 1
fi

# Execute the downloaded script with elevated privileges
if sudo chmod +777 hysteria2-install-script.sh && sudo ./hysteria2-install-script.sh; then
  echo "脚本执行成功。"
else
  echo "脚本执行失败。"
  exit 1
fi