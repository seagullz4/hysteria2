# Define commands to install

commands=("wget" "netstat" "sed" "openssl")

# Function to install missing commands on CentOS
install_on_centos() {
  for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
      echo "Installing $cmd on CentOS..."
      sudo yum install -y "$cmd"
      echo "$cmd installed successfully."
    else
      echo "$cmd is already installed on CentOS."
    fi
  done
}

# Function to install missing commands on Ubuntu
install_on_ubuntu() {
  for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
      echo "Installing $cmd on Ubuntu..."
      sudo apt update
      sudo apt install -y "$cmd"
      echo "$cmd installed successfully."
    else
      echo "$cmd is already installed on Ubuntu."
    fi
  done
}

# Detect the Linux distribution
if [ -f "/etc/os-release" ]; then
  source /etc/os-release
  if [ "$ID" == "centos" ] || [ "$ID" == "rhel" ]; then
    install_on_centos
  elif [ "$ID" == "ubuntu" ]; then
    install_on_ubuntu
  else
    echo "Unsupported Linux distribution: $ID"
    exit 1
  fi
else
  echo "Unable to detect Linux distribution."
  exit 1
fi

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