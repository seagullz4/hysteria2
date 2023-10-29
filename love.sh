function display_error {
  echo "错误：$1"
  exit 1
}

# 检查脚本是否以超级用户权限运行
if [ "$(id -u)" != "0" ]; then
  display_error "此脚本必须以超级用户或使用sudo运行。"
fi

# 参数
DNS_SERVER1="8.8.8.8"
DNS_SERVER2="1.1.1.1"
DNS_SERVER3="114.114.114.114"

netplan_config="/etc/netplan/01-custom-dns.yaml"

network_interfaces=($(ls /sys/class/net/))

echo "network:
  version: 2
  renderer: networkd
  ethernets:" > "$netplan_config"

for iface in "${network_interfaces[@]}"; do
  echo "    $iface:
      nameservers:
        addresses:
          - $DNS_SERVER1
          - $DNS_SERVER2
          - $DNS_SERVER3" >> "$netplan_config"
done

netplan apply

echo "已成功更新DNS配置为使用 $DNS_SERVER1、$DNS_SERVER2 和 $DNS_SERVER3 用于所有可用的网络接口。"

resolvectl status
