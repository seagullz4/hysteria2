#hello
#!/bin/bash
cd /root/hy3
rm -r hysteria-linux-amd64
wget -O hysteria-linux-amd64 https://github.com/apernet/hysteria/releases/download/app/v2.2.0/hysteria-linux-amd64
chmod +x hysteria-linux-amd64
nohup ./hysteria-linux-amd64 server &