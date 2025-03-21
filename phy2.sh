#!/bin/bash

install_dependencies() {
    local package_manager=$1
    local packages=(
        curl sudo openssl qrencode net-tools procps iptables ca-certificates python3 python3-pip
    )

    echo "正在使用 $package_manager 安装依赖..."
    if [ "$package_manager" == "apt" ]; then
        apt update && apt install -y "${packages[@]}"
    elif [ "$package_manager" == "dnf" ]; then
        dnf install -y epel-release  # 首先安装epel-release
        dnf install -y "${packages[@]}"  # 再安装其他包
    fi

    # 安装 Python 模块，确保pip有权限
    python3 -m pip install -q --user requests
}

check_linux_system() {
    # 读取系统信息（修复路径写法）
    local os_info=$(grep -i '^id=' /etc/os-release | cut -d= -f2- | tr -d '"')

    case $os_info in
        ubuntu|debian)
            install_dependencies "apt"
            ;;
        rocky|centos|fedora)
            install_dependencies "dnf"
            ;;
        *)
            echo -e "\033[31m不支持的Linux发行版\033[0m"
            exit 1
            ;;
    esac
}

# 调用主函数
check_linux_system