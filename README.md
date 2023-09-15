# Hysteria2
hysteria2一键安装
宝宝们如果觉得好用，记得点个小星星⭐️哦


## 脚本优势

适用于小白一键安装，自动写入配置以及申请证书，脚本代码完全**开源**，步骤几乎和官方所差无几，支持重装和卸载配置和节点信息显示


# **hy2介绍**

## ⚡ **快如闪电**
通过魔改的 QUIC 协议驱动，Hysteria 即使在最不稳定和容易丢包的网络环境中也能提供无与伦比的性能。

## ✊ **抗封锁能力**
协议旨在伪装成标准的 HTTP/3 流量，无论中间人还是主动探测，都很难分辨和封锁。

安装之前必须准备好域名，而且域名必须已经解析到了你的服务器ip
由于hysteria2默认是443端口，所以我就默认443端口，如果443端口被占用，请结束443端口的占用在进行执行脚本。

## **😇使用教程**:

执行下面的脚本，等你安装之后会提示你输入域名，端口，密码，邮箱，伪装域名等，*域名必须是你解析到你云服务器ip的行*，端口可以默认443端口，或者随机端口或者自定义，密码可以随机也可以自己输入，邮箱可以随机也可以自己输入，伪装网页可以随机也可以自己输入，等待一切就绪后就会输出显示你的hysteria2的节点信息，推荐使用nekobox，更多客户端配置请查看[客户端配置](https://v2.hysteria.network/zh/docs/getting-started/Client/)


**🙃安装脚本:**
```
curl -sSL https://raw.githubusercontent.com/seagullz4/hysteria2/main/hysteria2install.sh -o hysteria2install.sh && chmod +x hysteria2install.sh && sudo ./hysteria2install.sh
```

**注意**: 只支持amd，x86架构服务器，后期可能会支持其他架构比如arm

本项目原hysteria2地址请点击[hysteria](https://github.com/apernet/hysteria)


必须客户端支持hysteria2才行，否则就是你安装了也无法使用，安卓端推荐**[nekobox](https://github.com/MatsuriDayo/NekoBoxForAndroid)**

### **如需搬运本脚本内容，请注明远处谢谢**