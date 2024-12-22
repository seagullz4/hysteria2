# hysteria2  一键安装脚本  完全免费开源  禁止用于商业用途 请在当地法律允许下使用
import sys
import subprocess   #可以用来执行外部命令
from pathlib import Path

print("\033[91mHELLO HYSTERIA2 !\033[m")    # 其中 print("\033[91m你需要输入的文字\033[0m") 为ANSI转义码 输出红色文本

def agree_treaty():       #此函数作用为：用户是否同意此条款
    file_agree = Path(r"/root/project-hy2/agree.txt")  # 提取文件名
    if file_agree.exists():       #.exists()判断文件是否存在，存在则为true跳过此步骤
        print("你已经同意过谢谢")
    else:
        while True:
            choose_1 = input("是否同意并阅读安装hysteria2相关条款? (y/n) ：")
            if choose_1 == "y":
                print("我同意使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责")
                check_file = subprocess.run("touch agree.txt",shell = True)
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
        check_file = subprocess.run("apt update && apt install -y wget sed sudo openssl net-tools psmisc procps iptables iproute2 ca-certificates jq",shell = True)   #安装依赖
        print(check_file)
    elif "rocky" in sys_version.read_text().lower() or "centos" in sys_version.read_text().lower() or "fedora" in sys_version.read_text().lower():
        check_file = subprocess.run("dnf install -y epel-release wget sed sudo openssl net-tools psmisc procps iptables iproute2 ca-certificates jq",shell=True)
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
                hy2_install = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/)", shell=True)  # 调用hy2官方脚本进行安装
                print(hy2_install)
                print("hysteria2安装完成")
                break
            elif choice_2 == "2":
                version_1 = input("请输入您需要安装的版本号(直接输入版本号数字即可，不需要加v，如2.6.0)：")
                hy2_install_2 = subprocess.run(f"bash <(curl -fsSL https://get.hy2.sh/) --version v{version_1}",shell=True)  # 进行指定版本进行安装
                print(hy2_install_2)
                break
            else:
                print("输入错误，请重新输入")
        elif choice_1 == "n":
            print("已取消安装hysteria2")
            sys.exit()
        else:
            print("输入错误，请重新输入")

def hysteria2_uninstall():   #卸载hysteria2
    while True:
        choice_1 = input("是否进行卸载hysteria2 (y/n) ：")
        if choice_1 == "y":
            hy2_uninstall_1 = subprocess.run("bash <(curl -fsSL https://get.hy2.sh/) --remove",shell = True)   #调用hy2官方脚本进行卸载
            print(hy2_uninstall_1)
            hy2_uninstall_1_2 = subprocess.run("rm -f /etc/systemd/system/multi-user.target.wants/hysteria-server.service && rm -f /etc/systemd/system/multi-user.target.wants/hysteria-server@*.service && systemctl daemon-reload",shell=True)  # 删除禁用systemd服务
            print(hy2_uninstall_1_2)
            print("卸载hysteria2完成")
            while True:
                choice_2 = input("是否删除配置文件和 ACME 证书? (y/n) ：")
                if choice_2 == "y":
                    hy2_uninstall_2 = subprocess.run("rm -rf /etc/hysteria && userdel -r hysteria", shell=True)  # 删除hysteria2配置文件和acme证书
                    print(hy2_uninstall_2)
                    print("已删除")
                elif choice_2 == "n":
                    print("已取消")
                    sys.exit()
                else:
                    print("输入错误，请重新输入")
        elif choice_1 == "n":
            print("已取消卸载hysteria2")
            sys.exit()
        else:
            print("输入错误，请重新输入")

def server_manage():   #hysteria2服务管理
    while True:
        choice_1 = input("是否进行hysteria2服务管理 (y/n) ：")
        if choice_1 == "y":
            print("1. 启动服务(自动设置为开机自启动)")
            print("2. 停止服务")
            print("3. 重启服务")
            print("4. 查看服务状态")
            print("5. 退出")
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
                sys.exit()
            else:
                print("输入错误，请重新输入")
        elif choice_1 == "n":
            print("已取消服务管理")
            sys.exit()
        else:
            print("输入错误，请重新输入")