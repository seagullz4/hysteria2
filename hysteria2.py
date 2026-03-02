# hysteria2  一键安装脚本
import glob
import ipaddress
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib import parse

try:
    import requests
except ImportError:
    print("正在安装 requests 依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
    import requests


def agree_treaty():       #此函数作用为：用户是否同意此条款
    def hy_shortcut():   #添加hy2快捷键
        hy2_shortcut = Path(r"/usr/local/bin/hy2")  # 创建快捷方式
        hy2_shortcut.write_text("#!/bin/bash\nwget -O hy2.py https://raw.githubusercontent.com/seagullz4/hysteria2/main/hysteria2.py && chmod +x hy2.py && python3 hy2.py\n")  # 写入内容
        hy2_shortcut.chmod(0o755)
    file_agree = Path(r"/etc/hy2config/agree.txt")  # 提取文件名
    if file_agree.exists():       #.exists()判断文件是否存在，存在则为true跳过此步骤
        print("你已经同意过谢谢")
        hy_shortcut()
    else:
        while True:
            print("我同意使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责。且本程序仅供学习交流使用，不得用于任何商业用途。")
            choose_1 = input("是否同意并阅读(在上面)安装hysteria2相关条款 [y/n]：")
            if choose_1 == "y":
                # 使用 mkdir -p 防止目录已存在时命令整体失败
                subprocess.run("mkdir -p /etc/hy2config && touch /etc/hy2config/agree.txt && touch /etc/hy2config/hy2_url_scheme.txt", shell=True)
                #当用户同意安装时创建该文件，下次自动检查时跳过此步骤
                hy_shortcut()
                break
            elif choose_1 == "n":
                print("清同意此条款进行安装")
                sys.exit()
            else:
                print("\033[91m请输入正确选项！\033[m")

def hysteria2_install():    #安装hysteria2
    while True:
        choice_1 = input("是否安装/更新hysteria2 [y/n] ：")
        if choice_1 == "y":
            print("1. 默认安装最新版本\n2. 安装指定版本")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                subprocess.run("bash <(curl -fsSL https://get.hy2.sh/)", shell=True, executable="/bin/bash")  # 调用hy2官方脚本进行安装
                print("--------------")
                print("\033[91mhysteria2安装完成,请进行配置一键修改\033[m")
                print("--------------")
                hysteria2_config()
                break
            elif choice_2 == "2":
                version_1 = input("请输入您需要安装的版本号(直接输入版本号数字即可，不需要加v，如2.6.0)：")
                # 验证版本号格式，防止命令注入
                if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', version_1):
                    print("\033[91m版本号格式无效，请输入如 2.6.0 的格式\033[m")
                    continue
                subprocess.run(f"bash <(curl -fsSL https://get.hy2.sh/) --version v{version_1}", shell=True, executable="/bin/bash")  # 进行指定版本进行安装
                print("--------------")
                print(f"\033[91mhysteria2指定{version_1}版本安装完成,请输入选项进行配置一键修改！！！\033[m")
                print("--------------")
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
            subprocess.run("bash <(curl -fsSL https://get.hy2.sh/) --remove", shell=True, executable="/bin/bash")   #调用hy2官方脚本进行卸载
            # 停止并禁用iptables恢复服务
            subprocess.run(["systemctl", "stop", "hysteria-iptables.service"], stderr=subprocess.DEVNULL)
            subprocess.run(["systemctl", "disable", "hysteria-iptables.service"], stderr=subprocess.DEVNULL)
            # 清理iptables规则
            subprocess.run(["/bin/bash", "/etc/hy2config/jump_port_back.sh"], stderr=subprocess.DEVNULL)
            # 删除所有配置文件和服务
            
            # 使用glob处理通配符模式
            wildcard_paths = glob.glob("/etc/systemd/system/multi-user.target.wants/hysteria-server@*.service")
            for path in wildcard_paths:
                try:
                    Path(path).unlink(missing_ok=True)
                except Exception:
                    pass
            
            # 删除其他路径
            paths_to_remove = [
                "/etc/hysteria",
                "/etc/systemd/system/multi-user.target.wants/hysteria-server.service",
                "/etc/systemd/system/hysteria-iptables.service",
                "/etc/hy2config/iptables-rules.v4",
                "/etc/hy2config/iptables-rules.v6",
                "/etc/ssl/private/",
                "/etc/hy2config",
                "/usr/local/bin/hy2"
            ]
            for path_str in paths_to_remove:
                try:
                    path = Path(path_str)
                    if path.is_file():
                        path.unlink(missing_ok=True)
                    elif path.is_dir():
                        shutil.rmtree(path, ignore_errors=True)
                except Exception:
                    pass
            
            subprocess.run(["systemctl", "daemon-reload"])
            print("卸载hysteria2完成")
            sys.exit()
        elif choice_1 == "n":
            print("已取消卸载hysteria2")
            break
        else:
            print("\033[91m输入错误，请重新输入\033[m")

def server_manage():   #hysteria2服务管理
    while True:
            print("1. 启动服务(自动设置为开机自启动)\n2. 停止服务\n3. 重启服务\n4. 查看服务状态\n5. 日志查询\n6. 查看hy2版本具体信息\n0. 返回")
            choice_2 = input("请输入选项：")
            if choice_2 == "1":
                subprocess.run("systemctl enable --now hysteria-server.service", shell=True)
            elif choice_2 == "2":
                subprocess.run("systemctl stop hysteria-server.service", shell=True)
            elif choice_2 == "3":
                subprocess.run("systemctl restart hysteria-server.service", shell=True)
            elif choice_2 == "4":
                print("\033[91m输入q退出查看\033[m")
                subprocess.run("systemctl status hysteria-server.service", shell=True)
            elif choice_2 == "5":
                subprocess.run("journalctl --no-pager -e -u hysteria-server.service", shell=True)
            elif choice_2 == "6":
                os.system("/usr/local/bin/hysteria version")
            elif choice_2 == "0":
                break
            else:
                print("\033[91m输入错误，请重新输入\033[m")

def create_iptables_persistence_service():
    """创建systemd服务以在启动时恢复iptables规则"""
    # 创建恢复脚本，包含错误处理
    restore_script_content = """#!/bin/bash
# Hysteria2 iptables rules restoration script

set -e  # 遇到错误时退出

# 验证并恢复IPv4规则
if [ -f /etc/hy2config/iptables-rules.v4 ]; then
    if [ -s /etc/hy2config/iptables-rules.v4 ]; then
        if iptables-restore -t < /etc/hy2config/iptables-rules.v4 2>/dev/null; then
            iptables-restore < /etc/hy2config/iptables-rules.v4
            echo "IPv4 iptables规则恢复成功" | logger -t hysteria2-iptables
        else
            echo "IPv4 iptables规则文件无效，跳过恢复" | logger -t hysteria2-iptables
        fi
    fi
fi

# 验证并恢复IPv6规则
if [ -f /etc/hy2config/iptables-rules.v6 ]; then
    if [ -s /etc/hy2config/iptables-rules.v6 ]; then
        if ip6tables-restore -t < /etc/hy2config/iptables-rules.v6 2>/dev/null; then
            ip6tables-restore < /etc/hy2config/iptables-rules.v6
            echo "IPv6 ip6tables规则恢复成功" | logger -t hysteria2-iptables
        else
            echo "IPv6 ip6tables规则文件无效，跳过恢复" | logger -t hysteria2-iptables
        fi
    fi
fi

exit 0
"""
    restore_script_path = Path("/etc/hy2config/restore-iptables.sh")
    
    # 创建systemd服务
    service_content = """[Unit]
Description=Restore Hysteria2 iptables rules
After=network.target

[Service]
Type=oneshot
ExecStart=/etc/hy2config/restore-iptables.sh
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
"""
    service_path = Path("/etc/systemd/system/hysteria-iptables.service")
    try:
        # 写入恢复脚本
        restore_script_path.write_text(restore_script_content)
        restore_script_path.chmod(0o755)
        
        # 写入服务文件
        service_path.write_text(service_content)
        
        # 重新加载systemd并启用服务
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "hysteria-iptables.service"], check=True)
        print("已创建iptables持久化服务")
    except Exception as e:
        print(f"\033[91m创建iptables持久化服务失败: {e}\033[m")

def save_iptables_rules():
    """保存当前的iptables和ip6tables规则"""
    try:
        # 创建配置目录
        config_dir = Path("/etc/hy2config")
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存IPv4规则
        with open("/etc/hy2config/iptables-rules.v4", "w") as f:
            subprocess.run(["iptables-save"], stdout=f, check=True, text=True)
        print("已保存IPv4 iptables规则")
        
        # 保存IPv6规则
        with open("/etc/hy2config/iptables-rules.v6", "w") as f:
            subprocess.run(["ip6tables-save"], stdout=f, check=True, text=True)
        print("已保存IPv6 ip6tables规则")
        
        return True
    except Exception as e:
        print(f"\033[91m保存iptables规则失败: {e}\033[m")
        return False


def _validate_port(prompt_msg):
    """统一的端口号验证辅助函数，返回有效的端口号（1~65535）"""
    while True:
        try:
            port = int(input(prompt_msg))
            if 1 <= port <= 65535:
                return port
            else:
                print("端口号范围为1~65535，请重新输入")
        except ValueError:
            print("端口号只能为数字且不能包含小数点，请重新输入")


def hysteria2_config():     #hysteria2配置
    hy2_config = Path(r"/etc/hysteria/config.yaml")  # 配置文件路径
    hy2_url_scheme = Path(r"/etc/hy2config/hy2_url_scheme.txt")  # 配置文件路径
    while True:
        choice_1 = input("1. hy2配置查看\n2. hy2配置一键修改\n3. 手动修改hy2配置\n4. 性能优化(可选,推荐安装xanmod内核)\n0. 返回\n请输入选项：")
        if choice_1 == "1":
            while True:
                    try:
                        os.system("clear")
                        print("您的官方配置文件为：\n")
                        print(hy2_config.read_text())
                        print(hy2_url_scheme.read_text())
                        print("clash,surge,singbox模板在/etc/hy2config/下，请自行查看\n")
                        break
                    except FileNotFoundError:     #捕获错误，如果找不到配置文件则输出未找到配置文件
                        print("\033[91m未找到配置文件\033[m")
                    break
        elif choice_1 == "2":
            try:
                hy2_port = _validate_port("请输入端口号：")
                hy2_username = input("请输入您用户名：\n")
                hy2_username = urllib.parse.quote(hy2_username)
                hy2_passwd = input("请输入您的强密码：\n")
                hy2_url = input("请输入您需要伪装成的域名(请在前面加上https://)：\n")
                while True:
                    hy2_brutal = input("是否开启Brutal模式(默认不推荐开启)？[y/n]：")
                    if hy2_brutal == "y":
                        brutal_mode = "true"    # 修复：y=开启=ignoreClientBandwidth: true
                        break
                    elif hy2_brutal == "n":
                        brutal_mode = "false"   # 修复：n=关闭=ignoreClientBandwidth: false
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")
                while True:
                    hy2_obfs = input("是否开启混淆模式(默认不推荐开启，开启将会失去伪装能力)？[y/n]：")
                    if hy2_obfs == "y":
                        obfs_passwd = input("请输入您的混淆密码：\n")
                        obfs_mode = f"obfs:\n  type: salamander\n  \n  salamander:\n    password: {obfs_passwd}"
                        obfs_passwd = urllib.parse.quote(obfs_passwd)
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
                        print("请选择你的v4网络接口（默认eth0, 一般不是lo接口）")
                        # 显示可用网络接口
                        result = subprocess.run(["ip", "-o", "link", "show"], capture_output=True, text=True)
                        if result.returncode == 0:
                            for line in result.stdout.strip().split('\n'):
                                # 提取接口名称
                                if ':' in line:
                                    parts = line.split(':', 2)
                                    if len(parts) >= 2:
                                        print(f"  - {parts[1].strip()}")
                        interface_name = input("请输入您的网络接口名称：")
                        # 将端口输入放入循环，验证失败可重新输入
                        while True:
                            try:
                                first_port = int(input("请输入起始端口号："))
                                last_port = int(input("请输入结束端口号："))
                                if first_port < 1 or first_port > 65535:
                                    print("起始端口号范围为1~65535，请重新输入")
                                    continue
                                elif last_port < 1 or last_port > 65535:
                                    print("结束端口号范围为1~65535，请重新输入")
                                    continue
                                elif first_port > last_port:
                                    print("起始端口号不能大于结束端口号，请重新输入")
                                    continue
                                else:
                                    break  # 验证通过，跳出端口输入循环
                            except ValueError:
                                print("端口号只能为数字且不能包含小数点，请重新输入")

                        # 初始化IPv6变量
                        has_ipv6 = False
                        ipv6_interface = None

                        while True:
                            jump_port_ipv6 = input("是否开启ipv6端口跳跃(y/n)：")
                            if jump_port_ipv6 == "y":
                                print("请选择你的v6网络接口:")
                                # 显示可用网络接口
                                result = subprocess.run(["ip", "-o", "link", "show"], capture_output=True, text=True)
                                if result.returncode == 0:
                                    for line in result.stdout.strip().split('\n'):
                                        if ':' in line:
                                            parts = line.split(':', 2)
                                            if len(parts) >= 2:
                                                print(f"  - {parts[1].strip()}")
                                interface6_name = input("请输入您的v6网络接口名称：")
                                subprocess.run(["ip6tables", "-t", "nat", "-A", "PREROUTING", "-i", interface6_name,
                                              "-p", "udp", "--dport", f"{first_port}:{last_port}",
                                              "-j", "REDIRECT", "--to-ports", str(hy2_port)])
                                # 记录IPv6配置信息用于清理脚本
                                has_ipv6 = True
                                ipv6_interface = interface6_name
                                break
                            elif jump_port_ipv6 == "n":
                                has_ipv6 = False
                                ipv6_interface = None
                                break
                            else:
                                print("\033[91m输入错误请重新输入\033[m")
                        script_path = Path("/etc/hy2config/jump_port_back.sh")  #检恢复脚本是否存在
                        if script_path.exists():
                            subprocess.run(["/bin/bash", str(script_path)], stderr=subprocess.DEVNULL)
                            script_path.unlink(missing_ok=True)

                        # 应用iptables规则
                        subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-i", interface_name,
                                      "-p", "udp", "--dport", f"{first_port}:{last_port}",
                                      "-j", "REDIRECT", "--to-ports", str(hy2_port)])

                        # 创建清理脚本
                        jump_port_back = Path("/etc/hy2config/jump_port_back.sh")
                        cleanup_script = f"""#!/bin/sh
# Hysteria2 port hopping cleanup script
iptables -t nat -D PREROUTING -i {interface_name} -p udp --dport {first_port}:{last_port} -j REDIRECT --to-ports {hy2_port}
"""
                        if has_ipv6 and ipv6_interface:
                            cleanup_script += f"ip6tables -t nat -D PREROUTING -i {ipv6_interface} -p udp --dport {first_port}:{last_port} -j REDIRECT --to-ports {hy2_port}\n"

                        jump_port_back.write_text(cleanup_script)
                        jump_port_back.chmod(0o755)  # 更安全的权限设置

                        # 保存iptables规则以实现持久化
                        print("正在保存iptables规则以实现重启后自动恢复...")
                        if save_iptables_rules():
                            # 创建systemd服务以在启动时恢复规则
                            create_iptables_persistence_service()
                            print("\033[92m端口跳跃规则已配置并持久化，系统重启后将自动恢复\033[m")
                        else:
                            print("\033[91m警告：iptables规则已应用但持久化失败，系统重启后可能需要重新配置\033[m")

                        jump_ports_hy2 = f"&mport={first_port}-{last_port}"
                        break
                    elif jump_port_choice == "n":
                        jump_ports_hy2 = ""
                        break
                    else:
                        print("\033[91m输入错误请重新输入\033[m")

                # 初始化证书相关变量
                hy2_domain = ""
                domain_name = ""
                insecure = ""

                while True:
                    print("1. 自动申请域名证书\n2. 使用自签证书(不需要域名)\n3. 手动选择证书路径")
                    choice_2 = input("请输入您选项：")
                    if choice_2 == "1":
                        hy2_domain = input("请输入您自己的域名：\n")
                        domain_name = hy2_domain    # 修复：不再覆盖为空字符串
                        hy2_email = input("请输入您的邮箱：\n")
                        while True:
                            choice_acme = input("是否设置acme dns配置(如果不知道是什么请不要选择) [y/n]:")
                            if choice_acme == 'y':
                                while True:
                                    os.system('clear')
                                    dns_name = input("dns名称：\n1.Cloudflare\n2.Duck DNS\n3.Gandi.net\n4.Godaddy\n5.Name.com\n6.Vultr\n请输入您的选项：")
                                    if dns_name == '1':
                                        dns_token = input("请输入Cloudflare的Global api_token:")
                                        acme_dns = f"type: dns\n  dns:\n    name: cloudflare\n    config:\n      cloudflare_api_token: {dns_token}"
                                        break
                                    elif dns_name == '2':
                                        dns_token = input("请输入Duck DNS的api_token:")
                                        override_domain = input("请输入Duck DNS的override_domain:")
                                        acme_dns = f"type: dns\n  dns:\n    name: duckdns\n    config:\n      duckdns_api_token: {dns_token}\n    duckdns_override_domain: {override_domain}"
                                        break
                                    elif dns_name == '3':
                                        dns_token = input("请输入Gandi.net的api_token:")
                                        acme_dns = f"type: dns\n  dns:\n    name: gandi\n    config:\n      gandi_api_token: {dns_token}"
                                        break
                                    elif dns_name == '4':
                                        dns_token = input("请输入Godaddy的api_token:")
                                        acme_dns = f"type: dns\n  dns:\n    name: godaddy\n    config:\n      godaddy_api_token: {dns_token}"
                                        break
                                    elif dns_name == '5':
                                        dns_token = input("请输入Name.com的namedotcom_token:")
                                        dns_user = input("请输入Name.com的namedotcom_user:")
                                        namedotcom_server = input("请输入Name.com的namedotcom_server:")
                                        acme_dns = f"type: dns\n  dns:\n    name: {dns_name}\n    config:\n      namedotcom_token: {dns_token}\n      namedotcom_user: {dns_user}\n      namedotcom_server: {namedotcom_server}"
                                        break
                                    elif dns_name == '6':
                                        dns_token = input("请输入Vultr的API Key:")
                                        acme_dns = f"type: dns\n  dns:\n    name: {dns_name}\n    config:\n      vultr_api_key: {dns_token}"
                                        break
                                    else:
                                        print("输入错误，请重新输入")
                                break
                            elif choice_acme == 'n':
                                acme_dns = ""
                                break
                            else:
                                print("输入错误，请重新输入")
                        insecure = "&insecure=0"
                        hy2_config.write_text(f"listen: :{hy2_port}\n\nacme:\n  domains:\n    - {hy2_domain}\n  email: {hy2_email}\n  {acme_dns}\n\nauth:\n  type: password\n  password: {hy2_passwd}\n\nmasquerade:\n  type: proxy\n  proxy:\n    url: {hy2_url}\n    rewriteHost: true\n\nignoreClientBandwidth: {brutal_mode}\n\n{obfs_mode}\n{sniff_mode}\n")
                        break
                    elif choice_2 == "2":    #获取ipv4地址
                        def validate_and_get_ipv4():
                            """Helper function to get and validate IPv4 address from user"""
                            while True:
                                ip_input = input("无法自动获取IP，请手动输入服务器的IPv4地址：").strip()
                                try:
                                    # 验证是否为有效的IPv4地址
                                    ipaddress.IPv4Address(ip_input)
                                    return ip_input
                                except ipaddress.AddressValueError:
                                    print(f"\033[91m无效的IPv4地址: {ip_input}，请重新输入\033[m")
                        
                        def validate_and_get_ipv6():
                            """Helper function to get and validate IPv6 address from user"""
                            while True:
                                ip_input = input("无法自动获取IP，请手动输入服务器的IPv6地址：").strip()
                                try:
                                    # 验证是否为有效的IPv6地址
                                    ipaddress.IPv6Address(ip_input)
                                    return ip_input
                                except ipaddress.AddressValueError:
                                    print(f"\033[91m无效的IPv6地址: {ip_input}，请重新输入\033[m")
                        
                        def get_ipv4_info():
                            """获取IPv4地址，返回地址字符串"""
                            headers = {
                                'User-Agent': 'Mozilla'
                            }
                            try:
                                response = requests.get('http://ip-api.com/json/', headers=headers, timeout=3)
                                response.raise_for_status()
                                ip_data = response.json()
                                isp = ip_data.get('isp', '')

                                if 'cloudflare' in isp.lower():
                                    print("检测到Warp，请输入正确的服务器 IPv4 地址")
                                    ip = validate_and_get_ipv4()
                                else:
                                    ip = ip_data.get('query', '')

                                print(f"IPV4 WAN IP: {ip}")
                                return ip

                            except requests.RequestException as e:
                                print(f"请求失败: {e}")
                                print("尝试使用备用方法获取IP地址...")
                                # 使用备用方法获取IP地址
                                try:
                                    result = subprocess.run(['curl', '-4', '-s', 'ifconfig.me'], capture_output=True, text=True, timeout=5)
                                    if result.returncode == 0 and result.stdout.strip():
                                        ip = result.stdout.strip()
                                        # 验证IPv4格式
                                        try:
                                            ipaddress.IPv4Address(ip)
                                            print(f"IPV4 WAN IP: {ip}")
                                            return ip
                                        except ipaddress.AddressValueError:
                                            # 格式无效，让用户手动输入
                                            return validate_and_get_ipv4()
                                    else:
                                        # 如果还是失败，让用户手动输入
                                        return validate_and_get_ipv4()
                                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError, FileNotFoundError):
                                    # 如果备用方法也失败，让用户手动输入
                                    return validate_and_get_ipv4()

                        def get_ipv6_info():    #获取ipv6地址
                            """获取IPv6地址，返回带方括号的地址字符串"""
                            headers = {
                                'User-Agent': 'Mozilla'
                            }
                            try:
                                response = requests.get('https://api.ip.sb/geoip', headers=headers, timeout=3)
                                response.raise_for_status()
                                ip_data = response.json()
                                isp = ip_data.get('isp', '')

                                if 'cloudflare' in isp.lower():
                                    print("检测到Warp，请输入正确的服务器 IPv6 地址")
                                    ipv6_input = validate_and_get_ipv6()
                                    ip = f"[{ipv6_input}]"
                                else:
                                    ip = f"[{ip_data.get('ip', '')}]"

                                print(f"IPV6 WAN IP: {ip}")
                                return ip

                            except requests.RequestException as e:
                                print(f"请求失败: {e}")
                                print("尝试使用备用方法获取IP地址...")
                                # 使用备用方法获取IPv6地址
                                try:
                                    result = subprocess.run(['curl', '-6', '-s', 'ifconfig.me'], capture_output=True, text=True, timeout=5)
                                    if result.returncode == 0 and result.stdout.strip():
                                        ip = result.stdout.strip()
                                        # 验证IPv6格式
                                        try:
                                            ipaddress.IPv6Address(ip)
                                            formatted = f"[{ip}]"
                                            print(f"IPV6 WAN IP: {formatted}")
                                            return formatted
                                        except ipaddress.AddressValueError:
                                            # 格式无效，让用户手动输入
                                            ipv6_input = validate_and_get_ipv6()
                                            return f"[{ipv6_input}]"
                                    else:
                                        # 如果还是失败，让用户手动输入
                                        ipv6_input = validate_and_get_ipv6()
                                        return f"[{ipv6_input}]"
                                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError, FileNotFoundError):
                                    # 如果备用方法也失败，让用户手动输入
                                    ipv6_input = validate_and_get_ipv6()
                                    return f"[{ipv6_input}]"

                        def generate_certificate():      #生成自签证书
                            """生成自签证书，返回使用的域名"""
                            # 使用循环代替递归，避免栈溢出
                            while True:
                                # 提示用户输入域名
                                user_domain = input("请输入要用于自签名证书的域名（默认为 bing.com）: ")
                                cert_domain = user_domain.strip() if user_domain else "bing.com"

                                # 验证域名格式
                                if not re.match(r'^[a-zA-Z0-9.-]+$', cert_domain):
                                    print("无效的域名格式，请输入有效的域名！")
                                    continue  # 修复：循环重试而非递归

                                # 定义目标目录
                                target_dir = "/etc/ssl/private"

                                # 检查并创建目标目录
                                os.makedirs(target_dir, mode=0o755, exist_ok=True)

                                # 生成 EC 参数文件
                                ec_param_file = f"{target_dir}/ec_param.pem"
                                subprocess.run(["openssl", "ecparam", "-name", "prime256v1", "-out", ec_param_file],
                                               check=True)

                                # 生成证书和私钥
                                cmd = [
                                    "openssl", "req", "-x509", "-nodes", "-newkey", f"ec:{ec_param_file}",
                                    "-keyout", f"{target_dir}/{cert_domain}.key",
                                    "-out", f"{target_dir}/{cert_domain}.crt",
                                    "-subj", f"/CN={cert_domain}", "-days", "36500"
                                ]
                                subprocess.run(cmd, check=True)

                                # 设置文件权限，确保 hysteria 服务用户可读取
                                os.chmod(f"{target_dir}/{cert_domain}.key", 0o644)   # 私钥需要 hysteria 用户可读
                                os.chmod(f"{target_dir}/{cert_domain}.crt", 0o644)   # 证书所有人可读
                                os.chmod(target_dir, 0o755)                          # 目录权限
                                # 尝试将证书文件所有权交给 hysteria 用户（如果该用户存在）
                                subprocess.run(["chown", "root:hysteria",
                                               f"{target_dir}/{cert_domain}.key",
                                               f"{target_dir}/{cert_domain}.crt"],
                                              stderr=subprocess.DEVNULL)

                                print("自签名证书和私钥已生成！")
                                print(f"证书文件已保存到 {target_dir}/{cert_domain}.crt")
                                print(f"私钥文件已保存到 {target_dir}/{cert_domain}.key")
                                return cert_domain

                        domain_name = generate_certificate()
                        while True:
                            ip_mode = input("1. ipv4模式\n2. ipv6模式\n请输入您的选项：")
                            if ip_mode == '1':
                                hy2_domain = get_ipv4_info()
                                break
                            elif ip_mode == '2':
                                hy2_domain = get_ipv6_info()
                                break
                            else:
                                print("\033[91m输入错误，请重新输入！\033[m")
                        insecure = "&insecure=1"
                        hy2_config.write_text(f"listen: :{hy2_port}\n\ntls:\n  cert: /etc/ssl/private/{domain_name}.crt\n  key: /etc/ssl/private/{domain_name}.key\n\nauth:\n  type: password\n  password: {hy2_passwd}\n\nmasquerade:\n  type: proxy\n  proxy:\n    url: {hy2_url}\n    rewriteHost: true\n\nignoreClientBandwidth: {brutal_mode}\n\n{obfs_mode}\n{sniff_mode}\n")
                        break
                    elif choice_2 == "3":
                        hy2_cert = input("请输入您的证书路径：\n")
                        hy2_key = input("请输入您的密钥路径：\n")
                        hy2_domain = input("请输入您自己的域名：\n")
                        domain_name = hy2_domain    # 修复：不再覆盖为空字符串
                        insecure = "&insecure=0"
                        hy2_config.write_text(f"listen: :{hy2_port}\n\ntls:\n  cert: {hy2_cert}\n  key: {hy2_key}\n\nauth:\n  type: password\n  password: {hy2_passwd}\n\nmasquerade:\n  type: proxy\n  proxy:\n    url: {hy2_url}\n    rewriteHost: true\n\nignoreClientBandwidth: {brutal_mode}\n\n{obfs_mode}\n{sniff_mode}\n")
                        break
                    else:
                        print("\033[91m输入错误，请重新输入\033[m")

                os.system("clear")
                hy2_passwd = urllib.parse.quote(hy2_passwd)
                hy2_v2ray = f"hysteria2://{hy2_passwd}@{hy2_domain}:{hy2_port}?sni={domain_name}{obfs_scheme}{insecure}{jump_ports_hy2}#{hy2_username}"
                print("您的 v2ray 二维码为：\n")
                time.sleep(1)
                # 修复：使用 subprocess 避免命令注入
                subprocess.run(f'echo {shlex.quote(hy2_v2ray)} | qrencode -s 1 -m 1 -t ANSI256 -o -', shell=True, executable="/bin/bash")
                print(f"\n\n\033[91m您的hy2链接为: {hy2_v2ray}\n请使用v2ray/nekobox/v2rayNG/nekoray软件导入\033[m\n\n")
                hy2_url_scheme.write_text(f"您的 v2ray hy2配置链接为：{hy2_v2ray}\n")
                print("正在下载 clash,sing-box,surge 配置文件到/etc/hy2config/clash.yaml")
                hy2_v2ray_url = urllib.parse.quote(hy2_v2ray)
                url_rule = "&ua=&selectedRules=%22balanced%22&customRules=%5B%5D"
                # 修复：使用 subprocess 列表形式避免命令注入
                subprocess.run(["curl", "-o", "/etc/hy2config/clash.yaml", f"https://sub.baibaicat.site/clash?config={hy2_v2ray_url}{url_rule}"])
                subprocess.run(["curl", "-o", "/etc/hy2config/sing-box.yaml", f"https://sub.baibaicat.site/singbox?config={hy2_v2ray_url}{url_rule}"])
                subprocess.run(["curl", "-o", "/etc/hy2config/surge.yaml", f"https://sub.baibaicat.site/surge?config={hy2_v2ray_url}{url_rule}"])
                print("\033[91m \nclash,sing-box,surge配置文件已保存到 /etc/hy2config/ 目录下 ！！\n\n \033[m")
                os.system("systemctl enable --now hysteria-server.service")
                os.system("systemctl restart hysteria-server.service")

            except FileNotFoundError:
                print("\033[91m未找到配置文件,请先安装hysteria2\033[m")
        elif choice_1 == "3":
            print("\033[91m正在使用nano编辑器进行手动修改，输入完成后按Ctrl+X保存退出\033[m")
            subprocess.run("nano /etc/hysteria/config.yaml", shell=True)   #调用nano编辑器进行手动修改
            os.system("systemctl enable --now hysteria-server.service")
            os.system("systemctl restart hysteria-server.service")
            print("hy2服务已启动")
        elif choice_1 == "4":
            os.system("wget -O tcpx.sh 'https://github.com/ylx2016/Linux-NetSpeed/raw/master/tcpx.sh' && chmod +x tcpx.sh && ./tcpx.sh")
        elif choice_1 == "0":
            break
        else:
            print("\033[91m请重新输入\033[m")


def check_hysteria2_version():  # 检查hysteria2版本
    try:
        output = subprocess.check_output("/usr/local/bin/hysteria version | grep '^Version' | grep -o 'v[.0-9]*'",shell=True, stderr=subprocess.STDOUT)
        version = output.decode('utf-8').strip()

        if "v" in version:
            print(f"当前hysteria2版本为：{version}")
        else:
            print("未找到hysteria2版本")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e.output.decode('utf-8')}")

#接下来写主程序
agree_treaty()
while True:
    os.system("clear")
    print("\033[91mHELLO HYSTERIA2 !\033[m  (输入hy2快捷启动)")  # 其中 print("\033[91m你需要输入的文字\033[0m") 为ANSI转义码 输出红色文本
    print("1. 安装/更新hysteria2\n2. 卸载hysteria2\n3. hysteria2配置\n4. hysteria2服务管理\n0. 退出")
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
    elif choice == "0":
        print("已退出")
        sys.exit()
    else:
        print("\033[91m输入错误，请重新输入\033[m")
        time.sleep(1)
