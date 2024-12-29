# hysteria2  一键安装脚本
import sys
import subprocess
import urllib.request
import time
import requests
import re
import os
from urllib import parse
from pathlib import Path

def check_root():
    # 获取当前用户的 UID
    uid = os.getuid()

    if uid != 0:
        print("请以 root 用户权限运行此脚本。")
        sys.exit(1)  # 非 root 用户退出程序
    else:
        print("你好同学")

def agree_treaty():       #此函数作用为：用户是否同意此条款
    file_agree = Path(r"/root/hy2config/agree.txt")  # 提取文件名
    if file_agree.exists():       #.exists()判断文件是否存在，存在则为true跳过此步骤
        print("你已经同意过谢谢")
    else:
        while True:
            choose_1 = input("是否同意并阅读安装hysteria2相关条款? (y/n) ：")
            if choose_1 == "y":
                print("我同意使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责")
                check_file = subprocess.run("mkdir /root/hy2config && touch /root/hy2config/agree.txt && touch /root/hy2config/hy2_url_scheme.txt",shell = True)
                print(check_file)    #当用户同意安装时创建该文件，下次自动检查时跳过此步骤
                break
            elif choose_1 == "n":
                print("清同意此条款进行安装")
                sys.exit()
            else:
                print("\033[91m请输入正确选项！\033[m")
 
def check_linux_system():    #检查Linux系统为哪个进行对应的安装
    sys_version = Path(r"/etc/os-release")    #获取Linux系统版本
    if "ubuntu" in sys_version.read_text().lower() or "debian" in sys_version.read_text().lower():
        check_file = subprocess.run("apt update && apt install -y wget sudo openssl qrencode net-tools procps iptables ca-certificates",shell = True)   #安装依赖
        print(check_file)
    elif "rocky" in sys_version.read_text().lower() or "centos" in sys_version.read_text().lower() or "fedora" in sys_version.read_text().lower():
        check_file = subprocess.run("dnf install -y epel-release wget sudo openssl qrencode net-tools procps iptables ca-certificates",shell=True)
        print(check_file)
    else:
        print("\033[91m暂时不支持该系统，推荐使用Debian 11/Ubuntu 22.04 LTS/Rocky Linux 8/CentOS Stream 8/Fedora 37 更高以上的系统\033[m")

def hysteria2_install():    #安装hysteria2
    while True:
        choice_1 = input("是否安装hysteria2 (y/n) ：")
        if choice_1 == "y":
            print("1. 默认安装最新版本\n2. 安装指定版本")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                hy2_install = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/)",shell = True,executable="/bin/bash")  # 调用hy2官方脚本进行安装
                print(hy2_install)
                print("hysteria2安装完成")
                print("\033[91m请手动返回进行配置一键修改\033[m")
                time.sleep(2)
                break
            elif choice_2 == "2":
                version_1 = input("请输入您需要安装的版本号(直接输入版本号数字即可，不需要加v，如2.6.0)：")
                hy2_install_2 = subprocess.run(f"bash <(curl -fsSL https://get.hy2.sh/) --version v{version_1}",shell=True,executable="/bin/bash")  # 进行指定版本进行安装
                print(hy2_install_2)
                print(f"hysteria2指定{version_1}版本安装完成")
                print("\033[91m请手动返回进行配置一键修改\033[m")
                time.sleep(2)
                break
            else:
                print("\033[91m输入错误，请重新输入\033[m")
        elif choice_1 == "n":
            print("已取消安装hysteria2")
            break
        else:
            print("\033[91m输入错误，请重新输入\033[m")

def hysteria2_uninstall():   #卸载hysteria2
    while True:
        choice_1 = input("是否进行卸载hysteria2 (y/n) ：")
        if choice_1 == "y":
            hy2_uninstall_1 = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/) --remove",shell = True,executable="/bin/bash")   #调用hy2官方脚本进行卸载
            print(hy2_uninstall_1)
            hy2_uninstall_1_2 = subprocess.run("rm -rf /etc/hysteria && userdel -r hysteria && rm -f /etc/systemd/system/multi-user.target.wants/hysteria-server.service && rm -f /etc/systemd/system/multi-user.target.wants/hysteria-server@*.service && systemctl daemon-reload && rm -rf /etc/ssl/private/ && rm -rf /root/hy2config",shell=True)  # 删除禁用systemd服务
            print(hy2_uninstall_1_2)
            print("卸载hysteria2完成")
            sys.exit()
        elif choice_1 == "n":
            print("已取消卸载hysteria2")
            break
        else:
            print("\033[91m输入错误，请重新输入\033[m")

def server_manage():   #hysteria2服务管理
    while True:
            print("1. 启动服务(自动设置为开机自启动)\n2. 停止服务\n3. 重启服务\n4. 查看服务状态\n5. 日志查询\n6. 返回")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                print(subprocess.run("systemctl enable --now hysteria-server.service",shell=True))
            elif choice_2 == "2":
                print(subprocess.run("systemctl stop hysteria-server.service",shell=True))
            elif choice_2 == "3":
                print(subprocess.run("systemctl restart hysteria-server.service",shell=True))
            elif choice_2 == "4":
                print("\033[91m输入q退出查看\033[m")
                print(subprocess.run("systemctl status hysteria-server.service",shell=True))
            elif choice_2 == "5":
                print(subprocess.run("journalctl --no-pager -e -u hysteria-server.service",shell=True))
            elif choice_2 == "6":
                break
            else:
                print("\033[91m输入错误，请重新输入\033[m")
hy2_ip = "你很帅"   #这两个变量纯纯是为了夸奖正在观看我的代码的你
domain_name = "超级帅"
def hysteria2_config():     #hysteria2配置
    global hy2_ip,domain_name
    hy2_config = Path(r"/etc/hysteria/config.yaml")  # 配置文件路径
    hy2_url_scheme = Path(r"/root/hy2config/hy2_url_scheme.txt")  # 配置文件路径
    while True:
        choice_1 = input("1. hy2配置查看\n2. hy2配置一键修改\n3. 手动修改hy2配置\n4. 返回\n请输入选项：")
        if choice_1 == "1":
            while True:
                    try:
                        os.system("clear")
                        print("您的官方配置文件为：\n")
                        time.sleep(2)
                        print(hy2_config.read_text())
                        print(hy2_url_scheme.read_text())
                        break
                    except FileNotFoundError:     #捕获错误，如果找不到配置文件则输出未找到配置文件
                        print("\033[91m未找到配置文件\033[m")
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
                hy2_passwd = input("请输入您的强密码：\n")
                hy2_url = input("请输入您需要伪装成的域名(请在前面加上https://或者http://)：\n")
                while True:
                    hy2_brutal = input("是否开启Brutal模式(默认不推荐开启)？(y/n)：")
                    if hy2_brutal == "y":
                        brutal_mode = "false"
                        break
                    elif hy2_brutal == "n":
                        brutal_mode = "true"
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    hy2_obfs = input("是否开启混淆模式(默认不推荐开启，开启将会失去伪装能力)？(y/n)：")
                    if hy2_obfs == "y":
                        obfs_passwd = input("请输入您的混淆密码：\n")
                        obfs_mode = f"obfs:\n  type: salamander\n  \n  salamander:\n    password: {obfs_passwd}"
                        obfs_scheme = f"&obfs=salamander&obfs-password={obfs_passwd}&"
                        break
                    elif hy2_obfs == "n":
                        obfs_mode = ""
                        obfs_scheme = ""
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    print("1. 自动申请域名证书\n2. 使用自签证书(不需要域名)\n3. 手动选择证书路径")
                    choice_2 = input("请输入您选项：")
                    if choice_2 == "1":
                        hy2_domain = input("请输入您自己的域名：\n")
                        hy2_email = input("请输入您的邮箱：\n")
                        hy2_config.write_text(f"""
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
    
ignoreClientBandwidth: {brutal_mode}

{obfs_mode}
""")
                        os.system("clear")
                        print("您的二维码为：\n")
                        time.sleep(1)
                        os.system(f'echo "hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?{obfs_scheme}sni={hy2_domain}#{hy2_username}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的hy2配置为：\nhysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?{obfs_scheme}sni={hy2_domain}#{hy2_username}\033[m")
                        os.system(f'echo "hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?{obfs_scheme}sni={hy2_domain}#{hy2_username}" | qrencode -o /root/hy2config/hy2.png')
                        time.sleep(1)
                        print("二维码已保存到当前/root/hy2config目录")
                        hy2_url_scheme.write_text(f"您的hy2配置为：\nhysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?{obfs_scheme}sni={hy2_domain}#{hy2_username}")
                        print("hy2配置已写入/root/hy2config目录")
                        os.system("systemctl enable --now hysteria-server.service")
                        os.system("systemctl restart hysteria-server.service")
                        print("hy2服务已启动")
                        break
                    elif choice_2 == "2":    #获取ipv4地址
                        def get_ipv4_info():
                            global hy2_ip
                            headers = {
                                'User-Agent': 'Mozilla'
                            }
                            try:
                                response = requests.get('http://ip-api.com/json/', headers=headers, timeout=3)
                                response.raise_for_status()
                                ip_data = response.json()
                                isp = ip_data.get('isp', '')

                                if 'cloudflare' in isp.lower():
                                    new_ip = input("检测到Warp，请输入正确的服务器 IP：")
                                    hy2_ip = new_ip
                                else:
                                    hy2_ip = ip_data.get('query', '')

                                print(f"IPV4 WAN IP: {hy2_ip}")

                            except requests.RequestException as e:
                                print(f"请求失败: {e}")

                        def get_ipv6_info():    #获取ipv6地址
                            global hy2_ip
                            headers = {
                                'User-Agent': 'Mozilla'
                            }
                            try:
                                response = requests.get('https://api.ip.sb/geoip', headers=headers, timeout=3)
                                response.raise_for_status()
                                ip_data = response.json()
                                isp = ip_data.get('isp', '')

                                if 'cloudflare' in isp.lower():
                                    new_ip = input("检测到Warp，请输入正确的服务器 IP：")
                                    hy2_ip = f"[{new_ip}]"
                                else:
                                    hy2_ip = f"[{ip_data.get('ip', '')}]"

                                print(f"IPV6 WAN IP: {hy2_ip}")

                            except requests.RequestException as e:
                                print(f"请求失败: {e}")

                        def generate_certificate():      #生成自签证书
                            global domain_name
                            # 提示用户输入域名
                            user_domain = input("请输入要用于自签名证书的域名（默认为 bing.com）: ")
                            domain_name = user_domain.strip() if user_domain else "bing.com"

                            # 验证域名格式
                            if re.match(r'^[a-zA-Z0-9.-]+$', domain_name):
                                # 定义目标目录
                                target_dir = "/etc/ssl/private"

                                # 检查并创建目标目录
                                if not os.path.exists(target_dir):
                                    print(f"目标目录 {target_dir} 不存在，正在创建...")
                                    os.makedirs(target_dir)
                                    if not os.path.exists(target_dir):
                                        print(f"无法创建目录 {target_dir}，请检查权限。")
                                        exit(1)

                                # 生成 EC 参数文件
                                ec_param_file = f"{target_dir}/ec_param.pem"
                                subprocess.run(["openssl", "ecparam", "-name", "prime256v1", "-out", ec_param_file],
                                               check=True)

                                # 生成证书和私钥
                                cmd = [
                                    "openssl", "req", "-x509", "-nodes", "-newkey", f"ec:{ec_param_file}",
                                    "-keyout", f"{target_dir}/{domain_name}.key",
                                    "-out", f"{target_dir}/{domain_name}.crt",
                                    "-subj", f"/CN={domain_name}", "-days", "36500"
                                ]
                                subprocess.run(cmd, check=True)

                                # 设置文件权限
                                os.chmod(f"{target_dir}/{domain_name}.key", 0o666)
                                os.chmod(f"{target_dir}/{domain_name}.crt", 0o666)

                                print("自签名证书和私钥已生成！")
                                print(f"证书文件已保存到 {target_dir}/{domain_name}.crt")
                                print(f"私钥文件已保存到 {target_dir}/{domain_name}.key")
                            else:
                                print("无效的域名格式，请输入有效的域名！")
                                generate_certificate()

                        generate_certificate()
                        while True:
                            ip_mode = input("1. ipv4模式\n2. ipv6模式\n请输入您的选项：\n")
                            if ip_mode == '1':
                                get_ipv4_info()
                                break
                            elif ip_mode == '2':
                                get_ipv6_info()
                                break
                            else:
                                print("\033[91m输入错误，请重新输入！\033[m")
                        hy2_config.write_text(f"""
listen: :{hy2_port} 

tls:
  cert: /etc/ssl/private/{domain_name}.crt
  key: /etc/ssl/private/{domain_name}.key 

auth:
  type: password
  password: {hy2_passwd} 

masquerade: 
  type: proxy
  proxy:
    url: {hy2_url} 
    rewriteHost: true
    
ignoreClientBandwidth: {brutal_mode}

{obfs_mode}
""")
                        os.system("clear")
                        print("您的二维码为：")
                        time.sleep(1)
                        os.system(f'echo "hysteria2://{hy2_passwd}@{hy2_ip}:{hy2_port}?insecure=1&sni={domain_name}{obfs_scheme}#{hy2_username}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的hy2配置为：\nhysteria2://{hy2_passwd}@{hy2_ip}:{hy2_port}?insecure=1&sni={hy2_ip}{obfs_scheme}#{hy2_username}\033[m")
                        os.system(f'echo "hysteria2://{hy2_passwd}@{hy2_ip}:{hy2_port}?insecure=1&sni={domain_name}{obfs_scheme}#{hy2_username}" | qrencode -o /root/hy2config/hy2.png')
                        time.sleep(1)
                        print("二维码已保存到/root/hy2config目录")
                        hy2_url_scheme.write_text(f"您的hy2配置为：\nhysteria2://{hy2_passwd}@{hy2_ip}:{hy2_port}?insecure=1&sni={domain_name}{obfs_scheme}#{hy2_username}")
                        print("配置已写入/root/hy2config目录")
                        os.system("systemctl enable --now hysteria-server.service")
                        os.system("systemctl restart hysteria-server.service")
                        print("hy2服务已启动")
                        break
                    elif choice_2 == "3":
                        hy2_cert = input("请输入您的证书路径：\n")
                        hy2_key = input("请输入您的密钥路径：\n")
                        hy2_domain = input("请输入您自己的域名：\n")
                        hy2_config.write_text(f"""
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

ignoreClientBandwidth: {brutal_mode}

{obfs_mode}
""")
                        os.system("clear")
                        print("您的二维码为：")
                        time.sleep(1)
                        os.system(f'echo "hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?sni={hy2_domain}{obfs_scheme}#{hy2_username}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的hy2配置为：\nhysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?sni={hy2_domain}{obfs_scheme}#{hy2_username}\033[m")
                        os.system(f'echo "hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?sni={hy2_domain}{obfs_scheme}#{hy2_username}" | qrencode -o /root/hy2config/hy2.png')
                        time.sleep(1)
                        print("二维码已保存到/root/hy2config目录")
                        hy2_url_scheme.write_text(f"您的hy2配置为：\nhysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?sni={hy2_domain}{obfs_scheme}#{hy2_username}")
                        print("配置已写入/root/hy2config目录")
                        os.system("systemctl enable --now hysteria-server.service")
                        os.system("systemctl restart hysteria-server.service")
                        print("hy2服务已启动")
                        break
                    else:
                        print("\033[91m输入错误，请重新输入\033[m")
            except FileNotFoundError:
                print("\033[91m未找到配置文件,请先安装hysteria2\033[m")
        elif choice_1 == "3":
            print("\033[91m正在使用nano编辑器进行手动修改，输入完成后按Ctrl+X保存退出\033[m")
            print(subprocess.run("nano /etc/hysteria/config.yaml",shell=True))   #调用nano编辑器进行手动修改
            os.system("systemctl enable --now hysteria-server.service")
            os.system("systemctl restart hysteria-server.service")
            print("hy2服务已启动")
        elif choice_1 == "4":
            break
        else:
            print("\033[91m请重新输入\033[m")

#接下来写主程序
check_root()
agree_treaty()
check_linux_system()
while True:
    os.system("clear")
    print("\033[91mHELLO HYSTERIA2 !\033[m")  # 其中 print("\033[91m你需要输入的文字\033[0m") 为ANSI转义码 输出红色文本
    print("1. 安装hysteria2\n2. 卸载hysteria2\n3. hysteria2配置\n4. hysteria2服务管理\n5. 退出")
    choice = input("请输入选项：")
    if choice == "1":
        os.system("clear")
        hysteria2_install()
    elif choice == "2":
        os.system("clear")
        hysteria2_uninstall()
    elif choice == "3":
        os.system("clear")
        hysteria2_config()
    elif choice == "4":
        os.system("clear")
        server_manage()
    elif choice == "5":
        print("已退出")
        sys.exit()
    else:
        print("\033[91m输入错误，请重新输入\033[m")
        time.sleep(1)