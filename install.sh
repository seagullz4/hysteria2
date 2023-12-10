#!/bin/bash

# 检测当前用户是否为 root 用户
if [ "$EUID" -ne 0 ]; then
  echo "请使用 root 用户执行此脚本！"
  echo "你可以使用 'sudo -i' 进入 root 用户模式。"
  exit 1
fi



# Define commands to install
commands=("wget" "sed" "openssl" "net-tools" "psmisc" "procps" )
package_manager=""
install_command=""

# Determine the package manager and install command
if [ -x "$(command -v apt)" ]; then
  package_manager="apt"
  install_command="sudo apt install -y"
elif [ -x "$(command -v yum)" ]; then
  package_manager="yum"
  install_command="sudo yum install -y"
else
  echo "Unsupported package manager."
  exit 1
fi

# Function to install missing commands
install_missing_commands() {
  for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &>/dev/null; then
      echo "Installing $cmd..."
      $install_command "$cmd"
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

# Call the function to install missing commands
install_missing_commands

# Detect system architecture
echo "正在识别系统架构中，请稍候……"
arch=$(uname -m)

case $arch in
  x86_64|amd64)
    echo "识别成功！为 x86_64/amd64 架构，正在运行对应命令……"
    script_url="https://github.com/seagullz4/hysteria2/raw/main/hy2amd.sh"
    ;;
  aarch64)
    echo "识别成功！为 arm64 架构，正在运行对应命令……"
    script_url="https://github.com/seagullz4/hysteria2/raw/main/hy2arm.sh"
    ;;
  *)
    echo "不支持的架构: $arch"
    exit 1
    ;;
esac

# Download the script
if wget -O hy2.sh "$script_url"; then
  chmod +x hy2.sh  # 授予下载的脚本执行权限
  echo "下载并授予脚本执行权限成功。"
else
  echo "下载脚本失败。退出。"
  exit 1
fi


# Execute the downloaded script with elevated privileges
if bash hy2.sh; then
  echo "而你，我的朋友，你是恋爱脑里的常青树，Joker里的顶梁柱，麦当劳的吉祥物，哥谭市的大头目，扑克牌的最大数，蝙蝠侠的大客户……"
  echo "

家人们,由于我是傻鸟,脚本有问题请尽快提出来,很可能因为我的粗心导致脚本不能使用,这是经常发生的,请大家谅解,谢谢"
else
  echo "脚本执行失败。"
  exit 1
fi