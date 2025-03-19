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

def agree_treaty():       #此函数作用为：用户是否同意此条款
    file_agree = Path(r"/etc/hy2config/agree.txt")  # 提取文件名
    if file_agree.exists():       #.exists()判断文件是否存在，存在则为true跳过此步骤
        print("你已经同意过谢谢")
    else:
        while True:
            choose_1 = input("是否同意并阅读安装hysteria2相关条款? [y/n] ：")
            if choose_1 == "y":
                print("我同意使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责。")
                check_file = subprocess.run("mkdir /etc/hy2config && touch /etc/hy2config/agree.txt && touch /etc/hy2config/hy2_url_scheme.txt",shell = True)
                print(check_file)    #当用户同意安装时创建该文件，下次自动检查时跳过此步骤
                hy2_shortcut = Path(r"/usr/local/bin/hy2")  # 创建快捷方式
                hy2_shortcut.write_text("#!/bin/bash\nwget -O hy2.py py.crazyact.com && python3 hy2.py")  # 写入内容
                hy2_shortcut.chmod(0o755)
                break
            elif choose_1 == "n":
                print("清同意此条款进行安装")
                sys.exit()
            else:
                print("\033[91m请输入正确选项！\033[m")
 
def check_linux_system():    #检查Linux系统为哪个进行对应的安装
    sys_version = Path(r"/etc/os-release")    #获取Linux系统版本
    if "ubuntu" in sys_version.read_text().lower() or "debian" in sys_version.read_text().lower():
        check_file = subprocess.run("apt update && apt install -y curl sudo openssl qrencode net-tools procps iptables ca-certificates",shell = True)   #安装依赖
        print(check_file)
    elif "rocky" in sys_version.read_text().lower() or "centos" in sys_version.read_text().lower() or "fedora" in sys_version.read_text().lower():
        check_file = subprocess.run("dnf install -y epel-release curl sudo openssl qrencode net-tools procps iptables-services ca-certificates",shell=True)
        print(check_file)
    else:
        print("\033[91m暂时不支持该系统，推荐使用Debian 11/Ubuntu 22.04 LTS/Rocky Linux 8/CentOS Stream 8/Fedora 37 更高以上的系统\033[m")

def hysteria2_install():    #安装hysteria2
    while True:
        choice_1 = input("是否安装/更新hysteria2 [y/n] ：")
        if choice_1 == "y":
            print("1. 默认安装最新版本\n2. 安装指定版本")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                hy2_install = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/)",shell = True,executable="/bin/bash")  # 调用hy2官方脚本进行安装
                print(hy2_install)
                print("hysteria2安装完成,请进行配置一键修改")
                hysteria2_config()
                break
            elif choice_2 == "2":
                version_1 = input("请输入您需要安装的版本号(直接输入版本号数字即可，不需要加v，如2.6.0)：")
                hy2_install_2 = subprocess.run(f"bash <(curl -fsSL https://get.hy2.sh/) --version v{version_1}",shell=True,executable="/bin/bash")  # 进行指定版本进行安装
                print(hy2_install_2)
                print(f"hysteria2指定{version_1}版本安装完成,请进行配置一键修改")
                hysteria2_config()
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
        choice_1 = input("是否进行卸载hysteria2 [y/n] ：")
        if choice_1 == "y":
            hy2_uninstall_1 = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/) --remove",shell = True,executable="/bin/bash")   #调用hy2官方脚本进行卸载
            print(hy2_uninstall_1)
            hy2_uninstall_1_2 = subprocess.run("rm -rf /etc/hysteria; rm -rf /etc/systemd/system/multi-user.target.wants/hysteria-server.service; rm -rf /etc/systemd/system/multi-user.target.wants/hysteria-server@*.service; systemctl daemon-reload; /etc/hy2config/jump_port_back.sh; rm -rf /etc/ssl/private/; rm -rf /etc/hy2config; rm -rf /usr/local/bin/hy2",shell=True)  # 删除禁用systemd服务
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
    hy2_url_scheme = Path(r"/etc/hy2config/hy2_url_scheme.txt")  # 配置文件路径
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
                hy2_url = input("请输入您需要伪装成的域名(请在前面加上https://)：\n")
                while True:
                    hy2_brutal = input("是否开启Brutal模式(默认不推荐开启)？[y/n]：")
                    if hy2_brutal == "y":
                        brutal_mode = "false"
                        break
                    elif hy2_brutal == "n":
                        brutal_mode = "true"
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    hy2_obfs = input("是否开启混淆模式(默认不推荐开启，开启将会失去伪装能力)？[y/n]：")
                    if hy2_obfs == "y":
                        obfs_passwd = input("请输入您的混淆密码：\n")
                        obfs_mode = f"obfs:\n  type: salamander\n  \n  salamander:\n    password: {obfs_passwd}"
                        obfs_scheme = f"&obfs=salamander&obfs-password={obfs_passwd}"
                        break
                    elif hy2_obfs == "n":
                        obfs_mode = ""
                        obfs_scheme = ""
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    hy2_sniff = input("是否开启协议嗅探 (Sniff)[y/n]：")
                    if hy2_sniff == "y":
                        sniff_mode = "sniff:\n  enable: true\n  timeout: 2s\n  rewriteDomain: false\n  tcpPorts: 80,443,8000-9000\n  udpPorts: all"
                        break
                    elif hy2_sniff == "n":
                        sniff_mode = ""
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    jump_port_choice = input("是否开启端口跳跃(y/n)：")
                    if jump_port_choice == "y":
                        try:
                            first_port = int(input("请输入起始端口号："))
                            last_port = int(input("请输入结束端口号："))
                            if first_port <= 0 or first_port >= 65536:
                                print("起始端口号范围为1~65535，请重新输入")
                            elif last_port <= 0 or last_port >= 65536:
                                print("结束端口号范围为1~65535，请重新输入")
                            elif first_port > last_port:
                                print("起始端口号不能大于结束端口号，请重新输入")
                            else:
                                def jump_port_v6 ():
                                    while True:
                                        jump_port_ipv6 = input("是否开启ipv6端口跳跃(y/n)：")
                                        if jump_port_ipv6 == "y":
                                            hy2_jump_port_ipv6 = f"ip6tables -t nat -A PREROUTING -i eth0 -p udp --dport {first_port}:{last_port} -j REDIRECT --to-ports {hy2_port}"
                                            os.system(hy2_jump_port_ipv6)
                                            break
                                        elif jump_port_ipv6 == "n":
                                            pass
                                            break
                                        else:
                                            print("\033[91m输入错误请重新输入\033[m")
                                jump_port_v6()
                                os.system(f"iptables -t nat -A PREROUTING -i eth0 -p udp --dport {first_port}:{last_port} -j REDIRECT --to-ports {hy2_port}")
                                os.system("touch /etc/hy2config/jump_port_back.sh")
                                jump_port_back = Path(r"/etc/hy2config/jump_port_back.sh")
                                jump_port_back.write_text(f"#!/bin/sh\niptables -t nat -D PREROUTING -i eth0 -p udp --dport {first_port}:{last_port} -j REDIRECT --to-ports {hy2_port}")
                                os.system("chmod 777 /etc/hy2config/jump_port_back.sh")
                                jump_ports_neko = f"mport={hy2_port},{first_port}-{last_port}&"
                                jump_ports_v2ray = f"&mport={first_port}-{last_port}"
                                break
                        except ValueError:  # 收集错误，判断用户是否输入为数字，上面int已经转换为数字，输入小数点或者其他字符串都会引发这个报错
                            print("端口号只能为数字且不能包含小数点，请重新输入")
                    elif jump_port_choice == "n":
                        jump_ports_neko = ""
                        jump_ports_v2ray = ""
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    print("1. 自动申请域名证书\n2. 使用自签证书(不需要域名)\n3. 手动选择证书路径")
                    choice_2 = input("请输入您选项：")
                    if choice_2 == "1":
                        hy2_domain = input("请输入您自己的域名：\n")
                        hy2_email = input("请输入您的邮箱：\n")
                        while True:
                            choice_acme = input("是否设置acme dns配置(如果不知道是什么请不要选择) [y/n]:")
                            if choice_acme == 'y':
                                while True:
                                    os.system('clear')
                                    dns_name = input("dns名称:\n1.Cloudflare\n2.Duck DNS\n3.Gandi.net\n4.Godaddy\n5.Name.com\n6.Vultr\n请输入您的选项：")
                                    if dns_name == '1':
                                        dns_token = input("请输入Cloudflare的Global api_token:")
                                        acme_dns = f"type: dns\ndns:\n  name: cloudflare\n  config:\n    cloudflare_api_token: {dns_token}"
                                        break
                                    elif dns_name == '2':
                                        dns_token = input("请输入Duck DNS的api_token:")
                                        override_domain = input("请输入Duck DNS的override_domain:")
                                        acme_dns = f"type: dns\ndns:\n  name: duckdns\n  config:\n    duckdns_api_token: {dns_token}\n    duckdns_override_domain: {override_domain}"
                                        break
                                    elif dns_name == '3':
                                        dns_token = input("请输入Gandi.net的api_token:")
                                        acme_dns = f"type: dns\ndns:\n  name: gandi\n  config:\n    gandi_api_token: {dns_token}"
                                        break
                                    elif dns_name == '4':
                                        dns_token = input("请输入Godaddy的api_token:")
                                        acme_dns = f"type: dns\ndns:\n  name: godaddy\n  config:\n    godaddy_api_token: {dns_token}"
                                        break
                                    elif dns_name == '5':
                                        dns_token = input("请输入Name.com的namedotcom_token:")
                                        dns_user = input("请输入Name.com的namedotcom_user:")
                                        namedotcom_server = input("请输入Name.com的namedotcom_server:")
                                        acme_dns = f"type: dns\ndns:\n  name: {dns_name}\n  config:\n    namedotcom_token: {dns_token}\n    namedotcom_user: {dns_user}\n    namedotcom_server: {namedotcom_server}"
                                        break
                                    elif dns_name == '6':
                                        dns_token = input("请输入Vultr的API Key:")
                                        acme_dns = f"type: dns\ndns:\n  name: {dns_name}\n  config:\n    vultr_api_key: {dns_token}"
                                        break
                                    else:
                                        print("输入错误，请重新输入")
                                break
                            elif choice_acme == 'n':
                                acme_dns = ""
                                break
                            else:
                                print("输入错误，请重新输入")
                        # 一长串的配置文件
                        hy2_share_neko = f"hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}/?{jump_ports_neko}sni={hy2_domain}{obfs_scheme}#{hy2_username}"
                        hy2_share_v2ray = f"hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?security=tls{obfs_scheme}&insecure=1{jump_ports_v2ray}&sni={hy2_domain}#{hy2_username}"
                        hy2_config.write_text(f"listen: :{hy2_port} \n\nacme:\n  domains:\n    - {hy2_domain} \n  email: {hy2_email} \n  {acme_dns} \n\nauth:\n  type: password\n  password: {hy2_passwd} \n\nmasquerade: \n  type: proxy\n  proxy:\n    url: {hy2_url} \n    rewriteHost: true\n\nignoreClientBandwidth: {brutal_mode}\n\n{obfs_mode}\n{sniff_mode}\n")
                        os.system("clear")
                        print("您的 nekoray|nekobox 二维码为：\n")
                        time.sleep(1)
                        os.system(f'echo "{hy2_share_neko}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的 nekoray|nekobox hy2配置链接为：\n{hy2_share_neko}\033[m")
                        os.system(f'echo "{hy2_share_neko}" | qrencode -o /etc/hy2config/hy2-neko.png')
                        time.sleep(1)
                        print("二维码已保存到当前/etc/hy2config目录")
                        print("您的 v2ray 二维码为：\n")
                        time.sleep(3)
                        os.system(f'echo "{hy2_share_v2ray}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的 v2ray hy2配置链接为：\n{hy2_share_v2ray}\033[m")
                        os.system(f'echo "{hy2_share_v2ray}" | qrencode -o /etc/hy2config/hy2-v2ray.png')
                        hy2_url_scheme.write_text(f"您的 nekoray|nekobox hy2配置链接为：{hy2_share_neko}\n您的 v2ray hy2配置链接为：{hy2_share_v2ray}")
                        print("hy2配置已写入/etc/hy2config目录")
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
                                os.system(f"chmod 666 {target_dir}/{domain_name}.key && chmod 666 {target_dir}/{domain_name}.crt && chmod 777 /etc/ssl/private/")

                                print("自签名证书和私钥已生成！")
                                print(f"证书文件已保存到 {target_dir}/{domain_name}.crt")
                                print(f"私钥文件已保存到 {target_dir}/{domain_name}.key")
                            else:
                                print("无效的域名格式，请输入有效的域名！")
                                generate_certificate()

                        generate_certificate()
                        while True:
                            ip_mode = input("1. ipv4模式\n2. ipv6模式\n请输入您的选项：")
                            if ip_mode == '1':
                                get_ipv4_info()
                                break
                            elif ip_mode == '2':
                                get_ipv6_info()
                                break
                            else:
                                print("\033[91m输入错误，请重新输入！\033[m")
                        hy2_share_neko = f"hysteria2://{hy2_passwd}@{hy2_ip}:{hy2_port}/?{jump_ports_neko}insecure=1&sni={domain_name}{obfs_scheme}#{hy2_username}"
                        hy2_share_v2ray = f"hysteria2://{hy2_passwd}@{hy2_ip}:{hy2_port}?security=tls{obfs_scheme}&insecure=1{jump_ports_v2ray}&sni={domain_name}#{hy2_username}"
                        hy2_config.write_text(f"listen: :{hy2_port} \n\ntls: \n  cert: /etc/ssl/private/{domain_name}.crt \n  key: /etc/ssl/private/{domain_name}.key \n\nauth: \n  type: password \n  password: {hy2_passwd} \n\nmasquerade: \n  type: proxy \n  proxy: \n    url: {hy2_url} \n    rewriteHost: true \n\nignoreClientBandwidth: {brutal_mode} \n\n{obfs_mode}\n{sniff_mode}\n")
                        os.system("clear")
                        print("您的nekoray|nekobox二维码为：")
                        time.sleep(1)
                        # 显示二维码
                        os.system(f'echo "{hy2_share_neko}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的 nekoray|nekobox hy2配置链接为：\n{hy2_share_neko}\033[m")
                        time.sleep(1)
                        os.system(f'echo "{hy2_share_neko}" | qrencode -o /etc/hy2config/hy2-neko.png')
                        print("二维码已保存到/etc/hy2config目录")
                        print("您的v2ray二维码为：")
                        time.sleep(3)
                        os.system(f'echo "{hy2_share_v2ray}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的 v2ray hy2配置链接为：\n{hy2_share_v2ray}\033[m")
                        time.sleep(1)
                        os.system(f'echo "{hy2_share_v2ray}" | qrencode -o /etc/hy2config/hy2-v2ray.png')
                        print("二维码已保存到/etc/hy2config目录")
                        hy2_url_scheme.write_text(f"您的 nekoray|nekobox hy2配置链接为：{hy2_share_neko}\n您的 v2ray hy2配置链接为：{hy2_share_v2ray}")
                        print("配置已写入/etc/hy2config目录")
                        os.system("systemctl enable --now hysteria-server.service")
                        os.system("systemctl restart hysteria-server.service")
                        print("hy2服务已启动")
                        break
                    elif choice_2 == "3":
                        hy2_cert = input("请输入您的证书路径：\n")
                        hy2_key = input("请输入您的密钥路径：\n")
                        hy2_domain = input("请输入您自己的域名：\n")
                        hy2_config.write_text(f"listen: :{hy2_port}\n\ntls:\n  cert: {hy2_cert}\n  key: {hy2_key}\n\nauth:\n  type: password\n  password: {hy2_passwd}\n\nmasquerade: \n  type: proxy\n  proxy:\n    url: {hy2_url}\n    rewriteHost: true\n\nignoreClientBandwidth: {brutal_mode}\n\n{obfs_mode}\n{sniff_mode}\n")
                        os.system("clear")
                        hy2_share_neko = f"hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}/?{jump_ports_neko}sni={hy2_domain}{obfs_scheme}#{hy2_username}"
                        hy2_share_v2ray = f"hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?security=tls{obfs_scheme}&insecure=1{jump_ports_v2ray}&sni={hy2_domain}#{hy2_username}"
                        os.system("clear")
                        print("您的 nekoray|nekobox 二维码为：\n")
                        time.sleep(1)
                        os.system(f'echo "{hy2_share_neko}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的 nekoray|nekobox hy2配置链接为：\n{hy2_share_neko}\033[m")
                        os.system(f'echo "{hy2_share_neko}" | qrencode -o /etc/hy2config/hy2-neko.png')
                        time.sleep(1)
                        print("二维码已保存到当前/etc/hy2config目录")
                        print("您的 v2ray 二维码为：\n")
                        time.sleep(3)
                        os.system(f'echo "{hy2_share_v2ray}" | qrencode -s 1 -m 1 -t ANSI256 -o -')
                        time.sleep(1)
                        print(f"\033[91m您的 v2ray hy2配置链接为：\n{hy2_share_v2ray}\033[m")
                        os.system(f'echo "{hy2_share_v2ray}" | qrencode -o /etc/hy2config/hy2-v2ray.png')
                        hy2_url_scheme.write_text(f"您的 nekoray|nekobox hy2配置链接为：{hy2_share_neko}\n您的 v2ray hy2配置链接为：{hy2_share_v2ray}")
                        print("hy2配置已写入/etc/hy2config目录")
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

def check_hysteria2_version():  #检查hysteria2版本
    check_version = subprocess.run("/usr/local/bin/hysteria version | grep '^Version' | grep -o 'v[.0-9]*'",shell=True)
    if check_version.returncode == 0:
        print(f"您的hysteria2版本为 {check_version}")
    else:
        print("hysteria2未安装")

#接下来写主程序
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
        check_hysteria2_version()
        server_manage()
    elif choice == "5":
        print("已退出")
        sys.exit()
    else:
        print("\033[91m输入错误，请重新输入\033[m")
        time.sleep(1)