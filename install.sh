#!/bin/bash
# 检测当前用户是否为 root 用户
if [ "$EUID" -ne 0 ]; then
  echo "请使用 root 用户执行此脚本！"
  echo "你可以使用 'sudo -i' 进入 root 用户模式。"
  exit 1
fi

check_sys() {
  if [[ -f /etc/redhat-release ]]; then
    release="centos"
  elif grep -qi "debian" /etc/issue; then
    release="debian"
  elif grep -qi "ubuntu" /etc/issue; then
    release="ubuntu"
  elif grep -qi -E "centos|red hat|redhat|rocky" /etc/issue || grep -qi -E "centos|red hat|redhat|rocky" /proc/version; then
    release="centos"
  fi

  if [[ -f /etc/debian_version ]]; then
    OS_type="Debian"
    echo "检测为Debian通用系统，判断有误请反馈"
  elif [[ -f /etc/redhat-release || -f /etc/centos-release || -f /etc/fedora-release || -f /etc/rocky-release ]]; then
    OS_type="CentOS"
    echo "检测为CentOS通用系统，判断有误请反馈"
  else
    echo "Unknown"
  fi
}


_exists() {
    local cmd="$1"
    if eval type type >/dev/null 2>&1; then
      eval type "$cmd" >/dev/null 2>&1
    elif command >/dev/null 2>&1; then
      command -v "$cmd" >/dev/null 2>&1
    else
      which "$cmd" >/dev/null 2>&1
    fi
    local rt=$?
    return ${rt}
}

random_color() {
  colors=("31" "32" "33" "34" "35" "36" "37")
  echo -e "\e[${colors[$((RANDOM % 7))]}m$1\e[0m"
}

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_TYPE=$ID
    OS_VERSION=$VERSION_ID
else
    echo "无法确定操作系统类型。"
    exit 1
fi

install_custom_packages() {
    if [ "$OS_TYPE" = "debian" ] || [ "$OS_TYPE" = "ubuntu" ]; then
        apt update
        apt install -y wget sed sudo openssl net-tools psmisc procps iptables iproute2 ca-certificates jq
    elif [ "$OS_TYPE" = "centos" ] || [ "$OS_TYPE" = "rhel" ] || [ "$OS_TYPE" = "fedora" ] || [ "$OS_TYPE" = "rocky" ]; then
        yum install -y epel-release
        yum install -y wget sed sudo openssl net-tools psmisc procps-ng iptables iproute ca-certificates jq
    else
        echo "不支持的操作系统。"
        exit 1
    fi
}

install_custom_packages

echo "已安装的软件包："
for pkg in wget sed openssl iptables jq; do
    if command -v $pkg >/dev/null 2>&1; then
        echo "$pkg 已安装"
    else
        echo "$pkg 未安装"
    fi
done

echo "所有指定的软件包均已安装完毕。"

set_architecture() {
  case "$(uname -m)" in
    'i386' | 'i686')
     
      arch='386'
      ;;
    'amd64' | 'x86_64')
    
      arch='amd64'
      ;;
    'armv5tel' | 'armv6l' | 'armv7' | 'armv7l')
      
      arch='arm'
      ;;
    'armv8' | 'aarch64')
   
      arch='arm64'
      ;;
    'mips' | 'mipsle' | 'mips64' | 'mips64le')
      
      arch='mipsle'
      ;;
    's390x')
      
      arch='s390x'
      ;;
    *)

      echo "暂时不支持你的系统哦，可能是因为不在已知架构范围内。"
      exit 1
      ;;
  esac
}

get_installed_version() {
    if [ -x "/root/hy3/hysteria-linux-$arch" ]; then
        version="$("/root/hy3/hysteria-linux-$arch" version | grep Version | grep -o 'v[.0-9]*')"
    else
        version="你还没有安装,老登"
    fi
}

get_latest_version() {
  local tmpfile
  tmpfile=$(mktemp)

  if ! curl -sS "https://api.hy2.io/v1/update?cver=installscript&plat=linux&arch="$arch"&chan=release&side=server" -o "$tmpfile"; then
    error "Failed to get the latest version from Hysteria 2 API, please check your network and try again."
    exit 11
  fi

  local latest_version
  latest_version=$(grep -oP '"lver":\s*\K"v.*?"' "$tmpfile" | head -1)
  latest_version=${latest_version#'"'}
  latest_version=${latest_version%'"'}

  if [[ -n "$latest_version" ]]; then
    echo "$latest_version"
  fi

  rm -f "$tmpfile"
}

checkact() {
pid=$(pgrep -f "hysteria-linux-$arch")

if [ -n "$pid" ]; then
  hy2zt="运行中"
else
  hy2zt="未运行"
fi
}

BBR_grub() {
  if [[ "${OS_type}" == "CentOS" ]]; then
    if [[ ${version} == "6" ]]; then
      if [ -f "/boot/grub/grub.conf" ]; then
        sed -i 's/^default=.*/default=0/g' /boot/grub/grub.conf
      elif [ -f "/boot/grub/grub.cfg" ]; then
        grub-mkconfig -o /boot/grub/grub.cfg
        grub-set-default 0
      elif [ -f "/boot/efi/EFI/centos/grub.cfg" ]; then
        grub-mkconfig -o /boot/efi/EFI/centos/grub.cfg
        grub-set-default 0
      elif [ -f "/boot/efi/EFI/redhat/grub.cfg" ]; then
        grub-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
        grub-set-default 0
      else
        echo -e "${Error} grub.conf/grub.cfg 找不到，请检查."
        exit
      fi
    elif [[ ${version} == "7" ]]; then
      if [ -f "/boot/grub2/grub.cfg" ]; then
        grub2-mkconfig -o /boot/grub2/grub.cfg
        grub2-set-default 0
      elif [ -f "/boot/efi/EFI/centos/grub.cfg" ]; then
        grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
        grub2-set-default 0
      elif [ -f "/boot/efi/EFI/redhat/grub.cfg" ]; then
        grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
        grub2-set-default 0
      else
        echo -e "${Error} grub.cfg 找不到，请检查."
        exit
      fi
    elif [[ ${version} == "8" ]]; then
      if [ -f "/boot/grub2/grub.cfg" ]; then
        grub2-mkconfig -o /boot/grub2/grub.cfg
        grub2-set-default 0
      elif [ -f "/boot/efi/EFI/centos/grub.cfg" ]; then
        grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
        grub2-set-default 0
      elif [ -f "/boot/efi/EFI/redhat/grub.cfg" ]; then
        grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
        grub2-set-default 0
      else
        echo -e "${Error} grub.cfg 找不到，请检查."
        exit
      fi
      grubby --info=ALL | awk -F= '$1=="kernel" {print i++ " : " $2}'
    fi
  elif [[ "${OS_type}" == "Debian" ]]; then
    if _exists "update-grub"; then
      update-grub
    elif [ -f "/usr/sbin/update-grub" ]; then
      /usr/sbin/update-grub
    else
      apt install grub2-common -y
      update-grub
    fi
    #exit 1
  fi
}
check_version() {
  if [[ -s /etc/redhat-release ]]; then
    version=$(grep -oE "[0-9.]+" /etc/redhat-release | cut -d . -f 1)
  else
    version=$(grep -oE "[0-9.]+" /etc/issue | cut -d . -f 1)
  fi
  bit=$(uname -m)
  check_github
}
installxanmod1 () {
# 检查系统是否为 Debian 或 Ubuntu
if [[ $(cat /etc/os-release) =~ ^(Debian|Ubuntu) ]]; then
  echo "OJBK"
else
  echo "系统不是 Debian 或 Ubuntu"
  exit 1
fi

# 检查系统架构
if [[ $(uname -m) =~ ^(x86_64|amd64) ]]; then
  echo "正在安装中,请稍后……"
else
  echo "系统架构不是 x86/amd64,牢弟,买个好点的吧"
  exit 1
fi

echo "系统符合要求，继续执行脚本"
wget -qO - https://dl.xanmod.org/archive.key | sudo gpg --dearmor -o /usr/share/keyrings/xanmod-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/xanmod-archive-keyring.gpg] http://deb.xanmod.org releases main' | sudo tee /etc/apt/sources.list.d/xanmod-release.list
sudo apt update && sudo apt install linux-xanmod-x64v3
BBR_grub
echo -e "${Tip} 内核安装完毕，请参考上面的信息检查是否安装成功,默认从排第一的高版本内核启动"
echo "安装成功,请自行重启系统"
}
installxanmod2 () {
  check_version
  wget -O check_x86-64_psabi.sh https://dl.xanmod.org/check_x86-64_psabi.sh
  chmod +x check_x86-64_psabi.sh
  cpu_level=$(./check_x86-64_psabi.sh | awk -F 'v' '{print $2}')
  echo -e "CPU supports \033[32m${cpu_level}\033[0m"
  # exit
  if [[ ${bit} != "x86_64" ]]; then
    echo -e "${Error} 不支持x86_64以外的系统 !" && exit 1
  fi

  if [[ "${OS_type}" == "Debian" ]]; then
    apt update
    apt-get install gnupg gnupg2 gnupg1 sudo -y
    echo 'deb http://deb.xanmod.org releases main' | sudo tee /etc/apt/sources.list.d/xanmod-kernel.list
    wget -qO - https://dl.xanmod.org/gpg.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/xanmod-kernel.gpg add -
    if [[ "${cpu_level}" == "4" ]]; then
      apt update && apt install linux-xanmod-x64v4 -y
    elif [[ "${cpu_level}" == "3" ]]; then
      apt update && apt install linux-xanmod-x64v3 -y
    elif [[ "${cpu_level}" == "2" ]]; then
      apt update && apt install linux-xanmod-x64v2 -y
    else
      apt update && apt install linux-xanmod-x64v1 -y
    fi
  else
    echo -e "${Error} 不支持当前系统 ${release} ${version} ${bit} !" && exit 1
  fi

  BBR_grub
  echo -e "${Tip} 内核安装完毕，请参考上面的信息检查是否安装成功,默认从排第一的高版本内核启动,请自行重启系统"
}
detele_kernel() {
  if [[ "${OS_type}" == "CentOS" ]]; then
    rpm_total=$(rpm -qa | grep kernel | grep -v "${kernel_version}" | grep -v "noarch" | wc -l)
    if [ "${rpm_total}" ] >"1"; then
      echo -e "检测到 ${rpm_total} 个其余内核，开始卸载..."
      for ((integer = 1; integer <= ${rpm_total}; integer++)); do
        rpm_del=$(rpm -qa | grep kernel | grep -v "${kernel_version}" | grep -v "noarch" | head -${integer})
        echo -e "开始卸载 ${rpm_del} 内核..."
        rpm --nodeps -e ${rpm_del}
        echo -e "卸载 ${rpm_del} 内核卸载完成，继续..."
      done
      echo --nodeps -e "内核卸载完毕，继续..."
    else
      echo -e " 检测到 内核 数量不正确，请检查 !" && exit 1
    fi
  elif [[ "${OS_type}" == "Debian" ]]; then
    deb_total=$(dpkg -l | grep linux-image | awk '{print $2}' | grep -v "${kernel_version}" | wc -l)
    if [ "${deb_total}" ] >"1"; then
      echo -e "检测到 ${deb_total} 个其余内核，开始卸载..."
      for ((integer = 1; integer <= ${deb_total}; integer++)); do
        deb_del=$(dpkg -l | grep linux-image | awk '{print $2}' | grep -v "${kernel_version}" | head -${integer})
        echo -e "开始卸载 ${deb_del} 内核..."
        apt-get purge -y ${deb_del}
        apt-get autoremove -y
        echo -e "卸载 ${deb_del} 内核卸载完成，继续..."
      done
      echo -e "内核卸载完毕，继续..."
    else
      echo -e " 检测到 内核 数量不正确，请检查 !" && exit 1
    fi
  fi
}
detele_kernel_head() {
  if [[ "${OS_type}" == "CentOS" ]]; then
    rpm_total=$(rpm -qa | grep kernel-headers | grep -v "${kernel_version}" | grep -v "noarch" | wc -l)
    if [ "${rpm_total}" ] >"1"; then
      echo -e "检测到 ${rpm_total} 个其余head内核，开始卸载..."
      for ((integer = 1; integer <= ${rpm_total}; integer++)); do
        rpm_del=$(rpm -qa | grep kernel-headers | grep -v "${kernel_version}" | grep -v "noarch" | head -${integer})
        echo -e "开始卸载 ${rpm_del} headers内核..."
        rpm --nodeps -e ${rpm_del}
        echo -e "卸载 ${rpm_del} 内核卸载完成，继续..."
      done
      echo --nodeps -e "内核卸载完毕，继续..."
    else
      echo -e " 检测到 内核 数量不正确，请检查 !" && exit 1
    fi
  elif [[ "${OS_type}" == "Debian" ]]; then
    deb_total=$(dpkg -l | grep linux-headers | awk '{print $2}' | grep -v "${kernel_version}" | wc -l)
    if [ "${deb_total}" ] >"1"; then
      echo -e "检测到 ${deb_total} 个其余head内核，开始卸载..."
      for ((integer = 1; integer <= ${deb_total}; integer++)); do
        deb_del=$(dpkg -l | grep linux-headers | awk '{print $2}' | grep -v "${kernel_version}" | head -${integer})
        echo -e "开始卸载 ${deb_del} headers内核..."
        apt-get purge -y ${deb_del}
        apt-get autoremove -y
        echo -e "卸载 ${deb_del} 内核卸载完成，继续..."
      done
      echo -e "内核卸载完毕，继续..."
    else
      echo -e " 检测到 内核 数量不正确，请检查 !" && exit 1
    fi
  fi
}
detele_kernel_custom() {
  BBR_grub
  read -p " 查看上面内核输入需保留保留保留的内核关键词(如:5.15.0-11) :" kernel_version
  detele_kernel
  detele_kernel_head
  BBR_grub
}
welcome() {

echo -e "$(random_color '
░██  ░██
░██  ░██       ░████        ░█         ░█        ░█░█░█
░██  ░██     ░█      █      ░█         ░█        ░█    ░█
░██████     ░██████         ░█         ░█        ░█    ░█
░██  ░██     ░█             ░█ ░█      ░█  ░█     ░█░█░█
░██  ░██      ░██  █         ░█         ░█                   ')"
 echo -e "$(random_color '
人生有两出悲剧：一是万念俱灰，另一是踌躇满志 ')"
 
}

echo -e "$(random_color '安装必要依赖中......')"
install_missing_commands > /dev/null 2>&1
echo -e "$(random_color '依赖安装完成')"

set_architecture

get_installed_version

latest_version=$(get_latest_version)

checkact

uninstall_hysteria() {

sudo systemctl stop hysteria.service

sudo systemctl disable hysteria.service

if [ -f "/etc/systemd/system/hysteria.service" ]; then
  sudo rm "/etc/systemd/system/hysteria.service"
  echo "Hysteria 服务器服务文件已删除。"
else
  echo "Hysteria 服务器服务文件不存在。"
fi

process_name="hysteria-linux-$arch"
pid=$(pgrep -f "$process_name")

if [ -n "$pid" ]; then
  echo "找到 $process_name 进程 (PID: $pid)，正在杀死..."
  kill "$pid"
  echo "$process_name 进程已被杀死。"
else
  echo "未找到 $process_name 进程。"
fi

if [ -f "/root/hy3/hysteria-linux-$arch" ]; then
  rm -f "/root/hy3/hysteria-linux-$arch"
  echo "Hysteria 服务器二进制文件已删除。"
else
  echo "Hysteria 服务器二进制文件不存在。"
fi

if [ -f "/root/hy3/config.yaml" ]; then
  rm -f "/root/hy3/config.yaml"
  echo "Hysteria 服务器配置文件已删除。"
else
  echo "Hysteria 服务器配置文件不存在。"
fi

rm -rf /root/hy3
systemctl stop ipppp.service
systemctl disable ipppp.service
rm -rf /etc/systemd/system/ipppp.service
rm -rf /bin/hy2
echo "卸载完成(ง ื▿ ื)ว."
 }

hy2easy() {
    rm -rf /usr/local/bin/hy2
    sudo wget -q hy2.crazyact.com -O /usr/local/bin/hy2
    sudo chmod +x /usr/local/bin/hy2
    echo "已添加 hy2 快捷方式"
}

hy2easy
welcome

#这些就行提示你输入的😇
echo "$(random_color '选择一个操作，小崽子(ง ื▿ ื)ว：')"
echo -e "$(random_color '输入hy2快捷启动脚本')"
echo "1. 安装(以梦为马)"
echo "2. 卸载(以心为疆)"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "3. 查看配置(穿越时空)"
echo "4. 退出脚本(回到未来)"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "5. 在线更新hy2内核(您当前的hy2版本:$version)"
echo "6. hy2内核管理"
echo "7. 安装xanmod内核(更好的调动网络资源)"
echo "hy2内核最新版本为： $latest_version"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "hysteria2状态: $hy2zt"

read -p "输入操作编号 (1/2/3/4/5): " choice

case $choice in
   1)
     #啥也没有
     ;;

   2)

uninstall_hysteria > /dev/null 2>&1
echo -e "$(random_color '你别急,别急,正在卸载......')"
echo -e "$(random_color '卸载完成,老登ψ(｀∇´)ψ！')"

     exit
     ;;

   4)

     # Exit script
     exit
     ;;

   3)

echo "$(random_color '下面是你的nekobox节点信息')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
cd /root/hy3/

cat /root/hy3/neko.txt

echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '下面是你的clashmate配置')"

cat /root/hy3/clash-mate.yaml

echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
     exit
     ;;
    
   5)

get_updated_version() {
    if [ -x "/root/hy3/hysteria-linux-$arch" ]; then
        version2="$("/root/hy3/hysteria-linux-$arch" version | grep Version | grep -o 'v[.0-9]*')"
    else
        version2="你还没有安装,老登"
    fi
}

updatehy2 () {
process_name="hysteria-linux-$arch"

pid=$(pgrep -f "$process_name")

if [ -n "$pid" ]; then
  echo "找到 $process_name 进程 (PID: $pid)，正在杀死..."
  kill "$pid"
  echo "$process_name 进程已被杀死。"
else
  echo "未找到 $process_name 进程。"
fi

cd /root/hy3

rm -r hysteria-linux-$arch

if wget -O hysteria-linux-$arch https://download.hysteria.network/app/latest/hysteria-linux-$arch; then
  chmod +x hysteria-linux-$arch
else
  if wget -O hysteria-linux-$arch https://github.com/apernet/hysteria/releases/download/app/$latest_version/hysteria-linux-$arch; then
    chmod +x hysteria-linux-$arch
  else
    echo "无法从任何网站下载文件"
    exit 1
  fi
fi

systemctl stop hysteria.service
systemctl start hysteria.service

echo "更新完成,不是哥们,你有什么实力,你直接给我坐下(ง ื▿ ื)ว."
}
echo "$(random_color '正在更新中,别急,老登')"
sleep 1
updatehy2 > /dev/null 2>&1
echo "$(random_color '更新完成,老登')"
get_updated_version
echo "您当前的更新后hy2版本:$version2"

      exit
      ;;

    6)

echo "输入1启动hy2内核,输入2关闭hy2内核,输入3重启hy2内核"
read choicehy2
if [ "$choicehy2" = "1" ]; then
sudo systemctl start hysteria.service
echo "hy2内核启动成功"
elif [ "$choicehy2" = "2" ]; then
sudo systemctl stop hysteria.service
echo "hy2内核关闭成功"
elif [ "$choicehy2" = "3" ]; then
sudo systemctl restart hysteria.service
echo "hy2内核重启成功"
else
  echo "请输入正确选项"
fi

      exit
      ;;


   7)

echo "输入y安装,输入n取消,输入o卸载 (y/n/o)"
read answer
if [ "$answer" = "y" ]; then
check_sys
installxanmod2
elif [ "$answer" = "n" ]; then
  echo "Canceling and exiting..."
  exit 0
elif [ "$answer" = "o" ]; then
check_sys
detele_kernel_custom
else
  echo "Invalid input. Please enter y, n, or o."
fi
     exit
     ;;

   *)
     echo "$(random_color '无效的选择，退出脚本。')"

     exit
     ;;

esac

echo "$(random_color '别急,别急,别急,老登')"
sleep 1

if [ "$hy2zt" = "运行中" ]; then
  echo "Hysteria 正在运行，请先卸载再安装。"
  exit 1
else
  echo "原神,启动。"
fi

uninstall_hysteria > /dev/null 2>&1

installhy2 () {
  cd /root
  mkdir -p ~/hy3
  cd ~/hy3

  REPO_URL="https://github.com/apernet/hysteria/releases"
  LATEST_RELEASE=$(curl -s $REPO_URL/latest | jq -r '.tag_name')
  DOWNLOAD_URL="https://github.com/apernet/hysteria/releases/download/$LATEST_RELEASE/hysteria-linux-$arch"

  if wget -O hysteria-linux-$arch https://download.hysteria.network/app/latest/hysteria-linux-$arch; then
    chmod +x hysteria-linux-$arch
  else
    if wget -O hysteria-linux-$arch $DOWNLOAD_URL; then
      chmod +x hysteria-linux-$arch
    else
      echo "无法从任何网站下载文件"
      exit 1
    fi
  fi

  echo "Latest release version: $LATEST_RELEASE"
  echo "Download URL: $DOWNLOAD_URL"
}

echo "$(random_color '正在下载中,老登( ﾟдﾟ)つBye')"
sleep 1
installhy2 > /dev/null 2>&1

# 就是写一个配置文件，你可以自己修改，别乱搞就行，安装hysteria2文档修改
cat <<EOL > config.yaml
listen: :443



auth:
  type: password
  password: Se7RAuFZ8Lzg

masquerade:
  type: proxy
  file:
    dir: /www/masq
  proxy:
    url: https://news.ycombinator.com/
    rewriteHost: true
  string:
    content: hello stupid world
    headers:
      content-type: text/plain
      custom-stuff: ice cream so good
    statusCode: 200

bandwidth:
  up: 0 gbps
  down: 0 gbps

udpIdleTimeout: 90s

EOL

while true; do
    echo "$(random_color '请输入端口号（留空默认443，输入0随机2000-60000，你可以输入1-65630指定端口号）: ')"
    read -p "" port
  
    if [ -z "$port" ]; then
      port=443
    elif [ "$port" -eq 0 ]; then
      port=$((RANDOM % 58001 + 2000))
    elif ! [[ "$port" =~ ^[0-9]+$ ]]; then
      echo "$(random_color '我的动物朋友，请输入数字好吧，请重新输入端口号：')"
      continue
    fi
  
    while netstat -tuln | grep -q ":$port "; do
      echo "$(random_color '端口已被占用，请重新输入端口号：')"
      read -p "" port
    done
  
    if sed -i "s/443/$port/" config.yaml; then
      echo "$(random_color '端口号已设置为：')" "$port"
    else
      echo "$(random_color '替换端口号失败，退出脚本。')"
      exit 1
    fi
  

generate_certificate() {
    read -p "请输入要用于自签名证书的域名（默认为 bing.com）: " user_domain
    domain_name=${user_domain:-"bing.com"}
    if curl --output /dev/null --silent --head --fail "$domain_name"; then
        mkdir -p /etc/ssl/private
        openssl req -x509 -nodes -newkey ec:<(openssl ecparam -name prime256v1) -keyout "/etc/ssl/private/$domain_name.key" -out "/etc/ssl/private/$domain_name.crt" -subj "/CN=$domain_name" -days 36500
        chmod 777 "/etc/ssl/private/$domain_name.key" "/etc/ssl/private/$domain_name.crt"
        echo -e "自签名证书和私钥已生成！"
    else
        echo -e "无效的域名或域名不可用，请输入有效的域名！"
        generate_certificate
    fi
}

read -p "请选择证书类型（输入 1 使用ACME证书,输入 2 使用自签名证书,回车默认acme证书申请）: " cert_choice

if [ "$cert_choice" == "2" ]; then
    generate_certificate

    certificate_path="/etc/ssl/private/$domain_name.crt"
    private_key_path="/etc/ssl/private/$domain_name.key"

    echo -e "证书文件已保存到 /etc/ssl/private/$domain_name.crt"
    echo -e "私钥文件已保存到 /etc/ssl/private/$domain_name.key"

    temp_file=$(mktemp)
    echo -e "temp_file: $temp_file"
    sed '3i\tls:\n  cert: '"/etc/ssl/private/$domain_name.crt"'\n  key: '"/etc/ssl/private/$domain_name.key"'' /root/hy3/config.yaml > "$temp_file"
    mv "$temp_file" /root/hy3/config.yaml
    touch /root/hy3/ca
   #这里加了一个小的变量
    ovokk="insecure=1&"
    choice1="true"
    echo -e "已将证书和密钥信息写入 /root/hy3/config.yaml 文件。"
    
get_ipv4_info() {
  ip_address=$(wget -4 -qO- --no-check-certificate --user-agent=Mozilla --tries=2 --timeout=3 http://ip-api.com/json/) &&
  
  ispck=$(expr "$ip_address" : '.*isp\":[ ]*\"\([^"]*\).*')

  if echo "$ispck" | grep -qi "cloudflare"; then
    echo "检测到Warp，请输入正确的服务器 IP："
    read new_ip
    ipwan="$new_ip"
  else
    ipwan="$(expr "$ip_address" : '.*query\":[ ]*\"\([^"]*\).*')"
  fi
}

get_ipv6_info() {
  ip_address=$(wget -6 -qO- --no-check-certificate --user-agent=Mozilla --tries=2 --timeout=3 https://api.ip.sb/geoip) &&
  
  ispck=$(expr "$ip_address" : '.*isp\":[ ]*\"\([^"]*\).*')

  if echo "$ispck" | grep -qi "cloudflare"; then
    echo "检测到Warp，请输入正确的服务器 IP："
    read new_ip
    ipwan="[$new_ip]"
  else
    ipwan="[$(expr "$ip_address" : '.*ip\":[ ]*\"\([^"]*\).*')]"
  fi
}

while true; do
  echo "1. IPv4 模式"
  echo "2. IPv6 模式"
  echo "按回车键选择默认的 IPv4 模式."

  read -p "请选择: " choice

  case $choice in
    1)
      get_ipv4_info
      echo "老登你的IP 地址为：$ipwan"
      ipta="iptables"
      break
      ;;
    2)
      get_ipv6_info
      echo "老登你的IP 地址为：$ipwan"
      ipta="ip6tables"
      break
      ;;
    "")
      echo "使用默认的 IPv4 模式。"
      get_ipv4_info
      echo "老登你的IP 地址为：$ipwan"
      ipta="iptables"
      break
      ;;
    *)
      echo "输入无效。请输入1或2，或者按回车键使用默认的 IPv4 模式。"
      ;;
  esac
done

fi

if [ -f "/root/hy3/ca" ]; then
  echo "$(random_color '/root/hy3/ 文件夹中已存在名为 ca 的文件。跳过添加操作。')"
else

  echo "$(random_color '请输入你的域名（必须是解析好的域名哦）: ')"
  read -p "" domain

  while [ -z "$domain" ]; do
    echo "$(random_color '域名不能为空，请重新输入: ')"
    read -p "" domain
  done


  echo "$(random_color '请输入你的邮箱（默认随机邮箱）: ')"
  read -p "" email

  if [ -z "$email" ]; then

    random_part=$(head /dev/urandom | LC_ALL=C tr -dc A-Za-z0-9 | head -c 6 ; echo '')

    email="${random_part}@gmail.com"
  fi

  if [ -f "config.yaml" ]; then
    echo -e "\nAppending to config.yaml..."
    sed -i '3i\acme:\n  domains:\n    - '$domain'\n  email: '$email'' config.yaml
    echo "$(random_color '域名和邮箱已添加到 config.yaml 文件。')"
    ipta="iptables"
    choice2="false"
  else
    echo "$(random_color 'config.yaml 文件不存在，无法添加。')"
    exit 1
  fi
fi

echo "请选择一个选项:"
echo "1. 是否开启dns申请证书方式(默认cloudflare申请方式,需要api令牌,邮箱必须为注册邮箱)"
echo "2. 跳过(自签用户和不知道这个的回车默认直接跳过就行)"

read -p "请输入你的选择 (1或2): " choice

# 如果用户直接按回车，默认选择2
if [ -z "$choice" ]; then
    choice=2
fi

if [ "$choice" -eq 1 ]; then
    read -p "请输入Cloudflare的API令牌: " api_key

    # 查找email行的位置
    line_number=$(grep -n "email" /root/hy3/config.yaml | cut -d: -f1)

    if [ -z "$line_number" ]; then
        echo "未找到email行，请检查配置文件。"
        exit 1
    fi

    sed -i "${line_number}a\\
  type: dns\\
  dns:\\
    name: cloudflare\\
    config:\\
      cloudflare_api_token: $api_key" /root/hy3/config.yaml

    echo "配置已成功添加到/root/hy3/config.yaml"
else
    echo "跳过DNS配置步骤。"
fi

echo "$(random_color '请输入你的密码（留空将生成随机密码，不超过20个字符）: ')"
read -p "" password

if [ -z "$password" ]; then
  password=$(openssl rand -base64 20 | tr -dc 'a-zA-Z0-9')
fi

if sed -i "s/Se7RAuFZ8Lzg/$password/" config.yaml; then
  echo "$(random_color '密码已设置为：')" $password
else
  echo "$(random_color '替换密码失败，退出脚本。')"
  exit 1
fi

echo "$(random_color '请输入伪装网址（默认https://news.ycombinator.com/）: ')"
read -p "" masquerade_url

if [ -z "$masquerade_url" ]; then
  masquerade_url="https://news.ycombinator.com/"
fi

if sed -i "s|https://news.ycombinator.com/|$masquerade_url|" config.yaml; then
  echo "$(random_color '伪装域名已设置为：')" $masquerade_url
else
  echo "$(random_color '替换伪装域名失败，退出脚本。')"
  exit 1
fi
   
    echo "$(random_color '是否要开启端口跳跃功能？如果你不知道是干啥的，就衮吧，不用开启(ง ื▿ ื)ว（回车默认不开启，输入1开启）: ')"
    read -p "" port_jump
  
    if [ -z "$port_jump" ]; then
      
      break
    elif [ "$port_jump" -eq 1 ]; then
    
      echo "$(random_color '请输入起始端口号(起始端口必须小于末尾端口): ')"
      read -p "" start_port
  
      echo "$(random_color '请输入末尾端口号(末尾端口必须大于起始端口): ')"
      read -p "" end_port
  
     if [ "$start_port" -lt "$end_port" ]; then

"$ipta" -t nat -A PREROUTING -i eth0 -p udp --dport "$start_port":"$end_port" -j DNAT --to-destination :"$port"
        echo "$(random_color '端口跳跃功能已开启，将范围重定向到主端口：')" "$port"
        break
      else
        echo "$(random_color '末尾端口必须大于起始端口，请重新输入。')"
      fi
    else
      echo "$(random_color '输入无效，请输入1开启端口跳跃功能，或直接按回车跳过。')"
    fi
done

if [ -n "$port_jump" ] && [ "$port_jump" -eq 1 ]; then
  echo "#!/bin/bash" > /root/hy3/ipppp.sh
  echo "$ipta -t nat -A PREROUTING -i eth0 -p udp --dport $start_port:$end_port -j DNAT --to-destination :$port" >> /root/hy3/ipppp.sh
  
 
  chmod +x /root/hy3/ipppp.sh
  
  echo "[Unit]" > /etc/systemd/system/ipppp.service
  echo "Description=IP Port Redirect" >> /etc/systemd/system/ipppp.service
  echo "" >> /etc/systemd/system/ipppp.service
  echo "[Service]" >> /etc/systemd/system/ipppp.service
  echo "ExecStart=/root/hy3/ipppp.sh" >> /etc/systemd/system/ipppp.service
  echo "" >> /etc/systemd/system/ipppp.service
  echo "[Install]" >> /etc/systemd/system/ipppp.service
  echo "WantedBy=multi-user.target" >> /etc/systemd/system/ipppp.service
  
  # 启用开机自启动服务
  systemctl enable ipppp.service
  
  # 启动服务
  systemctl start ipppp.service
  
  echo "$(random_color '已创建/ipppp.sh脚本文件并设置开机自启动。')"
fi

fuser -k -n udp $port

cat <<EOL > clash-mate.yaml
system-port: 7890
external-controller: 127.0.0.1:9090
allow-lan: false
mode: rule
log-level: info
ipv6: true
unified-delay: true
profile:
  store-selected: true
  store-fake-ip: true
tun:
  enable: true
  stack: system
  auto-route: true
  auto-detect-interface: true
dns:
  enable: true
  prefer-h3: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  nameserver:
    - 223.5.5.5
    - 8.8.8.8
proxies:
  - name: Hysteria2
    type: hysteria2
    server: $domain$ipwan
    port: $port
    password: $password
    sni: $domain$domain_name
    skip-cert-verify: $choice1$choice2
proxy-groups:
  - name: auto
    type: select
    proxies:
      - Hysteria2
rules:
  - MATCH,auto
EOL
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "
clash-mate.yaml 已保存到当前文件夹
"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"

if nohup ./hysteria-linux-$arch server & then
  echo "$(random_color '
  Hysteria 服务器已启动。')"
else
  echo "$(random_color '启动 Hysteria 服务器失败，退出脚本。')"
  exit 1
fi
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
hysteria_directory="/root/hy3/"
hysteria_executable="/root/hy3/hysteria-linux-$arch"
hysteria_service_file="/etc/systemd/system/hysteria.service"

create_and_configure_service() {
  if [ -e "$hysteria_directory" ] && [ -e "$hysteria_executable" ]; then
    cat > "$hysteria_service_file" <<EOF
[Unit]
Description=My Hysteria Server

[Service]
Type=simple
WorkingDirectory=$hysteria_directory
ExecStart=$hysteria_executable server
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    echo "Hysteria服务器服务文件已创建和配置."
  else
    echo "Hysteria目录或可执行文件不存在，请检查路径."
    exit 1
  fi
}

enable_and_start_service() {
  if [ -f "$hysteria_service_file" ]; then
    systemctl enable hysteria.service
    systemctl start hysteria.service
    echo "Hysteria服务器服务已启用自启动并成功启动."
  else
    echo "Hysteria服务文件不存在，请先创建并配置服务文件."
    exit 1
  fi
}

create_and_configure_service
enable_and_start_service

echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "
完成。
"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"

echo "$(random_color '老登,马上,马上了------')"
sleep 2

echo "$(random_color '
这是你的clash配置:')"
cat /root/hy3/clash-mate.yaml

echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"
echo "$(random_color '>>>>>>>>>>>>>>>>>>>>')"

if [ -n "$start_port" ] && [ -n "$end_port" ]; then

  echo -e "$(random_color '这是你的Hysteria2节点链接信息，请注意保存哦joker(老登，请使用最新版的neko哦): ')\nhysteria2://$password@$ipwan$domain:$port/?${ovokk}mport=$port,$start_port-$end_port&sni=$domain$domain_name#Hysteria2"
  
  echo "hysteria2://$password@$ipwan$domain:$port/?${ovokk}mport=$port,$start_port-$end_port&sni=$domain$domain_name#Hysteria2" > neko.txt
  
else

  echo -e "$(random_color '这是你的Hysteria2节点链接信息，请注意保存哦小崽子: ')\nhysteria2://$password@$ipwan$domain:$port/?${ovokk}sni=$domain$domain_name#Hysteria2"
  
  echo "hysteria2://$password@$ipwan$domain:$port/?${ovokk}sni=$domain$domain_name#Hysteria2" > neko.txt
  
fi

echo -e "$(random_color '

Hysteria2安装成功，请合理使用哦,你直直-——直直接给我坐下')"
