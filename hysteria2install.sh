#!/bin/bash

# 生成随机颜色的 ANSI 转义序列
random_color() {
  colors=("31" "32" "33" "34" "35" "36")
  echo -e "\e[${colors[$((RANDOM % 6))]}m$1\e[0m"
}

line_animation() {
  lines=0
  while [ $lines -lt 8 ]; do
    echo -e "$(random_color '********************************************************************************')"
    sleep 0.375  # 每次休眠0.375秒 (3秒总时间 / 8行)
    lines=$((lines + 1))
  done
}

# 提示用户选择操作
echo "$(random_color '选择一个操作：')"
echo "1. 安装"
echo "2. 重装"
echo "3. 退出脚本"

read -p "输入操作编号 (1/2/3): " choice

case $choice in
  1)
    # 默认安装操作
    ;;
  2)
    # 重装并清除配置操作
    echo "执行重装并清除配置操作..."

    # 查找 Hysteria 服务器的进程并杀死它
    process_name="hysteria-linux-amd64-avx"
    pid=$(pgrep -f "$process_name")

    if [ -n "$pid" ]; then
      echo "找到 $process_name 进程 (PID: $pid)，正在杀死..."
      kill "$pid"
      echo "$process_name 进程已被杀死。"
    else
      echo "未找到 $process_name 进程。"
    fi

    # 在这里执行删除配置文件等操作
    ;;
  3)
    # 退出脚本
    exit
    ;;
  *)
    echo "无效的选择，退出脚本。"
    exit
    ;;
esac

# 以下是默认安装操作，你可以在这里添加安装代码

# 创建 hy3 文件夹并进入
mkdir -p ~/hy3
cd ~/hy3

# 下载 Hysteria 二进制文件并授予最高权限
wget -O hysteria-linux-amd64-avx https://github.com/apernet/hysteria/releases/download/app/v2.0.1/hysteria-linux-amd64-avx
chmod +x hysteria-linux-amd64-avx

# 获取当前用户名
current_user=$(whoami)

line_animation


# 创建 config.yaml 文件并写入默认内容
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

# 用户输入端口号
echo "$(random_color '请输入端口号（留空默认443，输入0随机2000-60000，输入1-65630为指定端口号）: ')"
read -p "" port

# 如果端口号为空，则默认为443
if [ -z "$port" ]; then
  port=443
elif [ "$port" -eq "0" ]; then
  # 如果端口号为0，则随机生成2000-60000之间的端口号
  port=$((RANDOM % 58001 + 2000))
elif [ "$port" -ge 1 ] && [ "$port" -le 65630 ]; then
  # 如果端口号在1-65630之间，则使用用户输入的端口号
  :
else
  echo "无效的端口号，退出脚本。"
  exit
fi

# 替换配置文件中的端口号
sed -i "s/443/$port/" config.yaml

# 提示用户输入域名
echo "$(random_color '请输入你的域名(必须是解析好的域名哦)（your.domain.net）: ')"
read -p "" domain

# 检查输入是否为空，如果为空则提示重新输入
while [ -z "$domain" ]; do
  echo "$(random_color '域名不能为空，请重新输入: ')"
  read -p "" domain
done

# 替换配置文件中的域名
sed -i "s/your.domain.net/$domain/" config.yaml

# 提示用户输入邮箱
echo "$(random_color '请输入你的邮箱（默认随机邮箱）: ')"
read -p "" email

# 如果邮箱为空，则使用随机邮箱
if [ -z "$email" ]; then
  email="your@email.com"
fi

# 替换配置文件中的邮箱
sed -i "s/your@email.com/$email/" config.yaml

# 提示用户输入密码
echo "$(random_color '请输入你的密码（留空将生成随机密码，不超过20个字符）: ')"
read -p "" password

# 如果密码为空，则生成随机密码
if [ -z "$password" ]; then
  password=$(openssl rand -base64 20 | tr -dc 'a-zA-Z0-9')
fi

# 替换配置文件中的密码
sed -i "s/Se7RAuFZ8Lzg/$password/" config.yaml

# 提示用户输入伪装域名
echo "$(random_color '请输入伪装域名（默认https://news.ycombinator.com/）: ')"
read -p "" masquerade_url

# 如果伪装域名为空，则使用默认值
if [ -z "$masquerade_url" ]; then
  masquerade_url="https://news.ycombinator.com/"
fi

# 替换配置文件中的伪装域名
sed -i "s|https://news.ycombinator.com/|$masquerade_url|" config.yaml

# 授予 Hysteria 二进制文件权限
sudo setcap cap_net_bind_service=+ep hysteria-linux-amd64-avx

# 后台运行 Hysteria 服务器
nohup ./hysteria-linux-amd64-avx server &

line_animation

# 输出 Hysteria 链接
echo -e "$(random_color '这是你的Hysteria2节点链接，请注意保存哦宝宝: ')hy2://$password@$domain:$port/?sni=$domain#Hysteria2"

# 输出安装成功信息
echo -e "$(random_color 'Hysteria2安装成功，请合理使用哦。')"