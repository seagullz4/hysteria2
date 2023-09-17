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
echo "4. 退出脚本(回到未来)"

read -p "输入操作编号 (1/2/3/4): " choice

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
     rm -rf ~/hy3
     echo "删除配置文件成功"
     # Perform operations such as deleting configuration files here
     ;;
   3)
     # Uninstallation operation
     echo "执行卸载操作请稍等..."

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

     # Remove the Hysteria binary and configuration files (adjust file paths as needed)
     rm -f ~/hy3/hysteria-linux-amd64
     rm -f ~/hy3/config.yaml
     rm -rf ~/hy3
     echo "卸载完成(ง ื▿ ื)ว."

     # Exit script after uninstallation
     exit
     ;;

   4)
     # Exit script
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
if wget -O hysteria-linux-amd64 https://github.com/apernet/hysteria/releases/download/app/v2.0.2/hysteria-linux-amd64; then
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
EOL

while true; do
  echo "$(random_color '请输入端口号（留空默认443，输入0随机2000-60000，你可以输入1-65630指定端口号）: ')"
  read -p "" port

  # If the port number is empty, it defaults to 443
  if [ -z "$port" ]; then
    port=443
  elif [ "$port" -eq "0" ]; then
    # Randomly generate a port number between 2000-60000
    port=$((RANDOM % 58001 + 2000))
  elif ! [[ "$port" =~ ^[0-9]+$ ]]; then
    echo "$(random_color '端口号必须是数字，请重新输入端口号：')"
    continue
  fi

  # Check if the entered port is in use
  while netstat -tuln | grep -q ":$port "; do
    echo "$(random_color '端口已被占用，请重新输入端口号：')"
    read -p "" port
  done

  # Replace the port number in the configuration file
  if sed -i "s/443/$port/" config.yaml; then
    echo "$(random_color '端口号已设置为：')" $port
    break
  else
    echo "$(random_color '替换端口号失败，退出脚本。')"
    exit 1
  fi
done

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

line_animation

# Output Hysteria link
echo -e "$(random_color '

这是你的Hysteria2节点链接，请注意保存哦宝宝: 

')hy2://$password@$domain:$port/?sni=$domain#Hysteria2"

# Output installation success information
echo -e "$(random_color '

Hysteria2安装成功，请合理使用哦。')"
