#!/bin/bash
red='\033[0;31m'
bblue='\033[0;34m'
plain='\033[0m'
red(){ echo -e "\033[31m\033[01m$1\033[0m";}
green(){ echo -e "\033[32m\033[01m$1\033[0m";}
yellow(){ echo -e "\033[33m\033[01m$1\033[0m";}
white(){ echo -e "\033[37m\033[01m$1\033[0m";}
readp(){ read -p "$(yellow "$1")" $2;}
clear
green "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"           
echo -e "${bblue} ░██   ░██     ░██   ░██     ░██${plain}   ░██    ░██     ░██      ░██ ██ ${red}██${plain} "
echo -e "${bblue} ░██  ░██      ░██  ░██${plain}      ░██  ░██      ░██   ░██      ░██    ${red}░░██${plain} "            
echo -e "${bblue} ░██ ██        ░██${plain} ██        ░██ ██         ░██ ░██      ░${red}██        ${plain} "
echo -e "${bblue} ░██ ██       ${plain} ░██ ██        ░██ ██           ░██        ${red}░██    ░██ ██${plain} "
echo -e "${bblue} ░██ ░${plain}██       ░██ ░██       ░██ ░██          ░${red}██         ░██    ░░██${plain}"
echo -e "${bblue} ░${plain}██  ░░██     ░██  ░░██     ░██  ░░${red}██        ░██          ░██ ██ ██${plain} "
green "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 
white "甬哥Github项目  ：github.com/yonggekkk"
white "甬哥blogger博客 ：ygkkk.blogspot.com"
white "甬哥YouTube频道 ：www.youtube.com/@ygkkk"
yellow "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#[[ -e /etc/hosts ]] && grep -qE '^ *172.65.251.78 gitlab.com' /etc/hosts || echo -e '\n172.65.251.78 gitlab.com' >> /etc/hosts
[[ $EUID -ne 0 ]] && su='sudo' 
lsattr /etc/passwd /etc/shadow >/dev/null 2>&1
chattr -i /etc/passwd /etc/shadow >/dev/null 2>&1
chattr -a /etc/passwd /etc/shadow >/dev/null 2>&1
lsattr /etc/passwd /etc/shadow >/dev/null 2>&1
prl=`grep PermitRootLogin /etc/ssh/sshd_config`
pa=`grep PasswordAuthentication /etc/ssh/sshd_config`
if [[ -n $prl && -n $pa ]]; then
readp "自定义root密码:" mima
if [[ -n $mima ]]; then
echo root:$mima | $su chpasswd root
$su sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config;
$su sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config;
$su service sshd restart
green "VPS当前用户名：root"
green "vps当前root密码：$mima"
else
red "未输入相关字符，启用root账户或root密码更改失败" 
fi
else
red "当前vps不支持root账户或无法自定义root密码,建议先执行sudo -i 进入root账户后再执行脚本" 
fi
rm -rf root.sh