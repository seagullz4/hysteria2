#!/bin/bash

install_dependencies() {
    local package_manager=$1
    local debian_packages=(
        curl sudo openssl qrencode net-tools procps iptables ca-certificates 
        python3 python3-pip python3-requests  # 直接通过系统仓库安装核心Python包
    )
    local redhat_packages=(
        curl sudo openssl qrencode net-tools procps iptables ca-certificates 
        python3 python3-pip
    )

    echo "正在使用 $package_manager 安装依赖..."
    if [ "$package_manager" == "apt" ]; then
        apt update && apt install -y "${debian_packages[@]}"
        # 禁用Debian的pip保护机制（需要管理员确认风险）
        rm -f /etc/python3.*/EXTERNALLY-MANAGED 2>/dev/null
    elif [ "$package_manager" == "dnf" ]; then
        dnf install -y epel-release
        dnf install -y "${redhat_packages[@]}"
    fi

    # 全局安装额外Python依赖（强制模式）
    python3 -m pip install --break-system-packages -q requests 2>/dev/null
}

check_linux_system() {
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
