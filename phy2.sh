#!/bin/bash
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
elif type lsb_release >/dev/null 2>&1; then
    OS=$(lsb_release -si | tr '[:upper:]' '[:lower:]')
else
    echo "无法检测到系统类型."
    exit 1
fi

case $OS in
    ubuntu|debian)
        PACKAGE_MANAGER='apt'
        ;;
    centos|rocky|fedora)
        PACKAGE_MANAGER='dnf'
        ;;
    *)
        echo "不支持的操作系统: $OS"
        exit 1
        ;;
esac

$PACKAGE_MANAGER update
$PACKAGE_MANAGER install -y python3 python3-pip

pip3 install requests

echo "安装完成."