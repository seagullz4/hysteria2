# hysteria2
hysteria2一键安装，小白无脑冲，歇斯底里，UDP高速协议



# **介绍**
Hysteria 由定制 QUIC 协议提供支持，即使在最不可靠和有损的网络上也能提供无与伦比的性能。
hysteria2的协议旨在伪装成标准 HTTP/3 流量，因此在不造成广泛附带损害的情况下很难检测和阻止。

安装之前必须准备好域名，而且域名必须已经解析到了你的服务器ip
由于hysteria2默认是443端口，所以我就默认443端口，如果443端口被占用，请结束443端口的占用在进行执行脚本。




**安装脚本:**
```
curl -sSL https://raw.githubusercontent.com/seagullz4/hysteria2/main/hysteria2install.sh -o hysteria2install.sh && chmod +x hysteria2install.sh && sudo ./hysteria2install.sh
```



本项目原hysteria2地址请点击[hysteria](https://github.com/apernet/hysteria)


必须客户端支持hysteria2才行，否则就无用的，安卓端推荐[nekobox](https://github.com/MatsuriDayo/NekoBoxForAndroid)

如需搬运本脚本内容，请注明远处谢谢