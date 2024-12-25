# hysteria2  一键安装脚本  完全免费开源  禁止用于商业用途 请在当地法律允许下使用
import sys
import subprocess   #可以用来执行外部命令
import urllib
from urllib import parse
from pathlib import Path

print("\033[91mHELLO HYSTERIA2 !\033[m")    # 其中 print("\033[91m你需要输入的文字\033[0m") 为ANSI转义码 输出红色文本

def agree_treaty():       #此函数作用为：用户是否同意此条款
    file_agree = Path(r"agree.txt")  # 提取文件名
    if file_agree.exists():       #.exists()判断文件是否存在，存在则为true跳过此步骤
        print("你已经同意过谢谢")
    else:
        while True:
            choose_1 = input("是否同意并阅读安装hysteria2相关条款? (y/n) ：")
            if choose_1 == "y":
                print("我同意使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责")
                check_file = subprocess.run("mkdir /root/hy2config && touch /root/hy2config/agree.txt",shell = True)
                print(check_file)    #当用户同意安装时创建该文件，下次自动检查时跳过此步骤
                break
            elif choose_1 == "n":
                print("清同意此条款进行安装")
                sys.exit()
            else:
                print("请输入正确选项！")
 
def check_linux_system():    #检查Linux系统为哪个进行对应的安装
    sys_version = Path(r"/etc/os-release")    #获取Linux系统版本
    if "ubuntu" in sys_version.read_text().lower() or "debian" in sys_version.read_text().lower():
        check_file = subprocess.run("apt update && apt install -y wget sudo openssl net-tools psmisc procps iptables iproute2 ca-certificates",shell = True)   #安装依赖
        print(check_file)
    elif "rocky" in sys_version.read_text().lower() or "centos" in sys_version.read_text().lower() or "fedora" in sys_version.read_text().lower():
        check_file = subprocess.run("dnf install -y epel-release wget sudo openssl net-tools psmisc procps iptables iproute2 ca-certificates",shell=True)
        print(check_file)
    else:
        print("\033[91m暂时不支持该系统，推荐使用Debian 11/Ubuntu 22.04 LTS/Rocky Linux 8/CentOS Stream 8/Fedora 37 更高以上的系统\033[m")

def hysteria2_install():    #安装hysteria2
    while True:
        choice_1 = input("是否安装hysteria2 (y/n) ：")
        if choice_1 == "y":
            print("1. 默认安装最新版本")
            print("2. 安装指定版本")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                hy2_install = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/)",shell = True,executable="/bin/bash")  # 调用hy2官方脚本进行安装
                print(hy2_install)
                print("hysteria2安装完成")
                break
            elif choice_2 == "2":
                version_1 = input("请输入您需要安装的版本号(直接输入版本号数字即可，不需要加v，如2.6.0)：")
                hy2_install_2 = subprocess.run(f"bash <(curl -fsSL https://get.hy2.sh/) --version v{version_1}",shell=True,executable="/bin/bash")  # 进行指定版本进行安装
                print(hy2_install_2)
                break
            else:
                print("输入错误，请重新输入")
        elif choice_1 == "n":
            print("已取消安装hysteria2")
            break
        else:
            print("输入错误，请重新输入")

def hysteria2_uninstall():   #卸载hysteria2
    while True:
        choice_1 = input("是否进行卸载hysteria2 (y/n) ：")
        if choice_1 == "y":
            hy2_uninstall_1 = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/) --remove",shell = True,executable="/bin/bash")   #调用hy2官方脚本进行卸载
            print(hy2_uninstall_1)
            hy2_uninstall_1_2 = subprocess.run("rm -rf /etc/hysteria && userdel -r hysteria && rm -f /etc/systemd/system/multi-user.target.wants/hysteria-server.service && rm -f /etc/systemd/system/multi-user.target.wants/hysteria-server@*.service && systemctl daemon-reload",shell=True)  # 删除禁用systemd服务
            print(hy2_uninstall_1_2)
            print("卸载hysteria2完成")
            sys.exit()
        elif choice_1 == "n":
            print("已取消卸载hysteria2")
            break
        else:
            print("输入错误，请重新输入")

def server_manage():   #hysteria2服务管理
    while True:
            print("1. 启动服务(自动设置为开机自启动)\n2. 停止服务\n3. 重启服务\n4. 查看服务状态\n5. 返回")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                hy2_start = subprocess.run("systemctl enable --now hysteria-server.service",shell=True)
                print(hy2_start)
            elif choice_2 == "2":
                hy2_stop = subprocess.run("systemctl stop hysteria-server.service",shell=True)
                print(hy2_stop)
            elif choice_2 == "3":
                hy2_restart = subprocess.run("systemctl restart hysteria-server.service",shell=True)
                print(hy2_restart)
            elif choice_2 == "4":
                hy2_status = subprocess.run("systemctl status hysteria-server.service",shell=True)
                print(hy2_status)
            elif choice_2 == "5":
                break
            else:
                print("输入错误，请重新输入")

def hysteria2_config():     #hysteria2配置
    while True:
        choice_1 = input("1. hy2配置查看\n2. hy2配置一键修改\n3. 返回\n请输入选项：")
        if choice_1 == "1":
            while True:
                    try:
                        hy2_config = Path(r"/etc/hysteria/config.yaml")   #查看配置文件
                        print(hy2_config.read_text())
                        break
                    except FileNotFoundError:     #捕获错误，如果找不到配置文件则输出未找到配置文件
                        print("未找到配置文件")
                    break
        elif choice_1 == "2":
            try:
                while True:
                    try:
                        hy2_port = int(input("请输入端口号："))
                        if hy2_port <= 0 or hy2_port >= 65536:
                            print("端口号范围为1~65535，请重新输入")
                        else:
                            break
                    except ValueError:     #收集错误，判断用户是否输入为数字，上面int已经转换为数字，输入小数点或者其他字符串都会引发这个报错
                        print("端口号只能为数字且不能包含小数点，请重新输入")
                hy2_username = input("请输入您用户名：\n")
                hy2_username = urllib.parse.quote(hy2_username)
                while True:
                    print("1. 自动申请域名证书\n2. 使用自签证书(不需要域名)\n3. 手动选择证书路径")
                    choice_2 = input("请输入您选项：")
                    if choice_2 == "1":
                        hy2_domain = input("请输入您自己的域名：\n")
                        hy2_email = input("请输入您的邮箱：\n")
                        hy2_passwd = input("请输入您的强密码：\n")
                        hy2_url = input("请输入您需要伪装的域名：\n")
                        hy2_config = Path(r"/etc/hysteria/config.yaml")
                        hy2_write_config = f'''
    listen: :{hy2_port} 
    
    acme:
      domains:
        - {hy2_domain} 
      email: {hy2_email} 
    
    auth:
      type: password
      password: {hy2_passwd} 
    
    masquerade: 
      type: proxy
      proxy:
        url: {hy2_url} 
        rewriteHost: true
    '''
                        hy2_config.write_text(hy2_write_config)
                        print(f"您的hy2配置为：hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?sni={hy2_domain}#{hy2_username}")
                        print("配置已写入")
                        break
                    elif choice_2 == "2":    #这里需要重写一下，自动帮用户申请证书并且填入路径
                        hy2_ssl_1 = subprocess.run("bash <(curl -fsSL https://file.willloving.xyz/api/public/dl/cm7R-REl?inline=true)",shell = True,executable="/bin/bash")
                        print(hy2_ssl_1)
                        hy2_ssl_domain = input("请输入你刚才输入的自签证书域名：\n")
                        hy2_passwd = input("请输入您的强密码：\n")
                        hy2_url = input("请输入您需要伪装的域名：\n")
                        hy2_config = Path(r"/etc/hysteria/config.yaml")
                        hy2_write_config = f'''
    listen: :{hy2_port} 
    
    tls:
      cert: /etc/ssl/private/{hy2_ssl_domain}.crt
      key: /etc/ssl/private/{hy2_ssl_domain}.key 
    
    auth:
      type: password
      password: {hy2_passwd} 
    
    masquerade: 
      type: proxy
      proxy:
        url: {hy2_url} 
        rewriteHost: true
    '''
                        hy2_config.write_text(hy2_write_config)
                        print("配置已写入")
                        break
                    elif choice_2 == "3":
                        hy2_cert = input("请输入您的证书路径：\n")
                        hy2_key = input("请输入您的密钥路径：\n")
                        hy2_passwd = input("请输入您的强密码：\n")
                        hy2_url = input("请输入您需要伪装的域名：\n")
                        hy2_config = Path(r"/etc/hysteria/config.yaml")
                        hy2_write_config = f'''
    listen: :{hy2_port} 
    
    tls:
      cert: {hy2_cert} 
      key: {hy2_key} 
    
    auth:
      type: password
      password: {hy2_passwd} 
    
    masquerade: 
      type: proxy
      proxy:
        url: {hy2_url} 
        rewriteHost: true
    '''
                        hy2_config.write_text(hy2_write_config)
                        print("配置已写入")
                        break
                    else:
                        print("输入错误，请重新输入")
            except FileNotFoundError:
                print("未找到配置文件,请先安装hysteria2")
        elif choice_1 == "3":
            break

#接下来写主程序
agree_treaty()
check_linux_system()
while True:
    print("1. 安装hysteria2\n2. 卸载hysteria2\n3. hysteria2服务管理\n4. hysteria2配置\n5. 退出")
    choice = input("请输入选项：")
    if choice == "1":
        hysteria2_install()
    elif choice == "2":
        hysteria2_uninstall()
    elif choice == "3":
        server_manage()
    elif choice == "4":
        hysteria2_config()
    elif choice == "5":
        print("已退出")
        sys.exit()
    else:
        print("输入错误，请重新输入")