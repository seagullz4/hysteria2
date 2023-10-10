#!/bin/bash

# ANSI escape sequence that generates random colors
random_color() {
  colors=("31" "32" "33" "34" "35" "36" "37")
  echo -e "\e[${colors[$((RANDOM % 7))]}m$1\e[0m"
}

line_animation() {
  lines=0
  while [ $lines -lt 8 ]; do
    echo -e "$(random_color '********************************************************************************')"
    sleep 0.375  # Sleep for 0.375 seconds each time (3 seconds total time / 8 lines)
    lines=$((lines + 1))
  done
}

welcome() {
  clear

  echo "████████████████████████████████████████████████████████████"
  echo "█     █     ███   ████   █   ████  █   █   ███   █   █   ███"
  echo "█  ████  ████   ████   █   ████  █   █   ███   █   █   ███"
  echo "你好，有缘人，欢迎你使用hy2一键安装脚本"
  echo "█  ████  ████   ████   █   ████  █   █   ███   █   █   ███"
  echo "█  ████  ████   ████   █   ████  █   █   ███   █   █   ███"
  echo "█     █          █       █       █       █       █       █"
  echo "问君能有几多愁？恰似一江春水向东流。"
  echo "████████████████████████████████████████████████████████████"
  echo "
  "
}

welcome

 
# Prompt user to select an action
echo "$(random_color '选择一个操作，宝宝(ง ื▿ ื)ว：')"
echo "1. 安装(世界和谐)"
echo "2. 重装(世界进步)"
echo "3. 卸载(世界美好)"
echo "4. 启动hy2(穿越时空)"
echo "5. 退出脚本(回到未来)"

read -p "输入操作编号 (1/2/3/4/5): " choice

case $choice in
   1)
     # Default installation operation
     ;;
   2)
     # Reinstall and clear configuration operations
     echo "执行重装并清除配置操作..."

     # Find the Hysteria server process and kill it
     process_name="hysteria-linux-amd64"
     pid=$(pgrep -f "$process_name")

     if [ -n "$pid" ]; then
       echo "找到 $process_name 进程 (PID: $pid)，正在杀死..."
       kill "$pid"
       echo "$process_name 进程已被杀死。"
     else
       echo "未找到 $process_name 进程。"
     fi
     
     rm -f ~/hy3/hysteria-linux-amd64 
     rm -f ~/hy3/config.yaml 
     echo "删除配置文件成功"
     # Perform operations such as deleting configuration files here
     ;;
   3)
#!/bin/bash

# 停止 Hysteria 服务器服务（根据实际的服务名称来替换"my_hysteria.service"）
sudo systemctl stop my_hysteria.service

# 禁用 Hysteria 服务器服务的自启动（根据实际的服务名称来替换"my_hysteria.service"）
sudo systemctl disable my_hysteria.service

# 删除 Hysteria 服务器服务文件（根据实际的服务文件路径来替换"/etc/systemd/system/my_hysteria.service"）
if [ -f "/etc/systemd/system/my_hysteria.service" ]; then
  sudo rm "/etc/systemd/system/my_hysteria.service"
  echo "Hysteria 服务器服务文件已删除。"
else
  echo "Hysteria 服务器服务文件不存在。"
fi

# 查找并杀死 Hysteria 服务器进程
process_name="hysteria-linux-amd64"
pid=$(pgrep -f "$process_name")

if [ -n "$pid" ]; then
  echo "找到 $process_name 进程 (PID: $pid)，正在杀死..."
  kill "$pid"
  echo "$process_name 进程已被杀死。"
else
  echo "未找到 $process_name 进程。"
fi

# 删除 Hysteria 服务器二进制文件和配置文件（根据实际文件路径来替换）
if [ -f "/root/hy3/hysteria-linux-amd64" ]; then
  rm -f "/root/hy3/hysteria-linux-amd64"
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
rm -r /root/hy3
systemctl stop ipppp.service
systemctl disable ipppp.service
rm /etc/systemd/system/ipppp.service

echo "卸载完成(ง ื▿ ื)ว."

# 退出脚本
exit
     ;;

   5)
     # Exit script
     exit
     ;;
   4)
    cd /root/hy3/
    nohup ./hysteria-linux-amd64 server &
    echo "启动成功"
    exit
    ;;

   *)
     echo "$(random_color '无效的选择，退出脚本。')"
     exit
     ;;
esac

# The following is the default installation operation, you can add installation code here

line_animation

# Create hy3 folder and enter
mkdir -p ~/hy3
cd ~/hy3

# Download the Hysteria binary and grant highest permissions
if wget -O hysteria-linux-amd64 https://github.com/apernet/hysteria/releases/download/app/v2.0.4/hysteria-linux-amd64; then
  chmod +x hysteria-linux-amd64
else
  echo "$(random_color '下载 Hysteria 二进制文件失败，退出脚本。')"
  exit 1
fi

# Get current username
current_user=$(whoami)

# Create a config.yaml file and write default content
cat <<EOL > config.yaml
listen: :443

acme:
  domains:
    - your.domain.net
  email: your@email.com

auth:
  type: password
  password: Se7RAuFZ8Lzg

masquerade:
  type: proxy
  proxy:
    url: https://news.ycombinator.com/
    rewriteHost: true

bandwidth:
  up: 99 gbps
  down: 99 gbps

udpIdleTimeout: 90s

ignoreClientBandwidth: false

quic:
  initStreamReceiveWindow: 8388608 
  maxStreamReceiveWindow: 8388608 
  initConnReceiveWindow: 20971520 
  maxConnReceiveWindow: 20971520 
  maxIdleTimeout: 90s 
  maxIncomingStreams: 1500 
  disablePathMTUDiscovery: false 
EOL


while true; do 
    echo "$(random_color '请输入端口号（留空默认443，输入0随机2000-60000，你可以输入1-65630指定端口号）: ')" 
    read -p "" port 
  
    if [ -z "$port" ]; then 
      port=443 
    elif [ "$port" -eq 0 ]; then 
      port=$((RANDOM % 58001 + 2000)) 
    elif ! [[ "$port" =~ ^[0-9]+$ ]]; then 
      echo "$(random_color '我的朋友，请输入数字好吧，请重新输入端口号：')" 
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
  
   
    echo "$(random_color '是否要开启端口跳跃功能？如果你不知道是干啥的，就不用开启(ง ื▿ ื)ว，安卓端不支持端口跳跃（回车默认不开启，输入1开启）: ')" 
    read -p "" port_jump 
  
    if [ -z "$port_jump" ]; then 
      
      break 
    elif [ "$port_jump" -eq 1 ]; then 
    
      echo "$(random_color '请输入起始端口号(起始端口必须小于末尾端口): ')" 
      read -p "" start_port 
  
      echo "$(random_color '请输入末尾端口号(末尾端口必须大于起始端口): ')" 
      read -p "" end_port 
  
      if [ "$start_port" -lt "$end_port" ]; then 
        
        iptables -t nat -A PREROUTING -i eth0 -p udp --dport "$start_port:$end_port" -j DNAT --to-destination :"$port" 
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
  echo "iptables -t nat -A PREROUTING -i eth0 -p udp --dport $start_port:$end_port -j DNAT --to-destination :$port" >> /root/hy3/ipppp.sh 
  
 
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
# Prompt user to enter domain name
echo "$(random_color '请输入你的域名(必须是解析好的域名哦)（your.domain.net）: ')"
read -p "" domain

# Check whether the input is empty, if it is empty, prompt to re-enter
while [ -z "$domain" ]; do
  echo "$(random_color '域名不能为空，请重新输入: ')"
  read -p "" domain
done

# Replace the domain name in the configuration file
if sed -i "s/your.domain.net/$domain/" config.yaml; then
  echo "$(random_color '域名已设置为：')" $domain
else
  echo "$(random_color '替换域名失败，退出脚本。')"
  exit 1
fi

# Prompt user to enter email address
echo "$(random_color '请输入你的邮箱（默认随机邮箱）: ')"
read -p "" email

# If the mailbox is empty, generate a random mailbox in the format xxxx@gmail.com
if [ -z "$email" ]; then
  # Generate a random string of 4 characters (xxxx part)
  random_part=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 4 ; echo '')

  # Set the email variable in the format xxxx@gmail.com
  email="${random_part}@gmail.com"
fi

# Replace email in profile
if sed -i "s/your@email.com/$email/" config.yaml; then
  echo "$(random_color '邮箱已设置为：')" $email
else
  echo "$(random_color '替换邮箱失败，退出脚本。')"
  exit 1
fi

# Prompt user for password
echo "$(random_color '请输入你的密码（留空将生成随机密码，不超过20个字符）: ')"
read -p "" password

# If the password is empty, generate a random password
if [ -z "$password" ]; then
  password=$(openssl rand -base64 20 | tr -dc 'a-zA-Z0-9')
fi

# Replace password in configuration file
if sed -i "s/Se7RAuFZ8Lzg/$password/" config.yaml; then
  echo "$(random_color '密码已设置为：')" $password
else
  echo "$(random_color '替换密码失败，退出脚本。')"
  exit 1
fi

# Prompt the user to enter the disguised domain name
echo "$(random_color '请输入伪装域名（默认https://news.ycombinator.com/）: ')"
read -p "" masquerade_url

# If the disguised domain name is empty, the default value is used
if [ -z "$masquerade_url" ]; then
  masquerade_url="https://news.ycombinator.com/"
fi

# Replace the disguised domain name in the configuration file
if sed -i "s|https://news.ycombinator.com/|$masquerade_url|" config.yaml; then
  echo "$(random_color '伪装域名已设置为：')" $masquerade_url
else
  echo "$(random_color '替换伪装域名失败，退出脚本。')"
  exit 1
fi

# Grant permissions to the Hysteria binary
if sudo setcap cap_net_bind_service=+ep hysteria-linux-amd64; then
  echo "$(random_color '授予权限成功。')"
else
  echo "$(random_color '授予权限失败，退出脚本。')"
  exit 1
fi

# Running the Hysteria server in the background
if nohup ./hysteria-linux-amd64 server & then
  echo "$(random_color 'Hysteria 服务器已启动。')"
else
  echo "$(random_color '启动 Hysteria 服务器失败，退出脚本。')"
  exit 1
fi

hysteria_directory="/root/hy3/"
hysteria_executable="/root/hy3/hysteria-linux-amd64"
hysteria_service_file="/etc/systemd/system/my_hysteria.service"

create_service_file() {
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
}

echo "正在设置Hysteria服务器..."
mkdir -p "$hysteria_directory"

if [ -e "$hysteria_service_file" ]; then
  echo "服务文件已存在."
else
  create_service_file
  echo "创建服务文件成功."
fi

echo "启用并启动Hysteria服务器服务..."
systemctl enable my_hysteria.service
systemctl start my_hysteria.service

if systemctl is-active --quiet my_hysteria.service; then
  echo "Hysteria服务器服务已启用自启动."
else
  echo "Hysteria服务器服务自启动失败但可以正常使用."
fi

echo "完成。"

line_animation

# Output Hysteria link
echo -e "$(random_color '

这是你的Hysteria2节点链接信息，请注意保存哦宝宝: 

')hy2://$password@$domain:$port/?sni=$domain#Hysteria2"

# Output installation success information
echo -e "$(random_color '

Hysteria2安装成功，请合理使用哦。')"
