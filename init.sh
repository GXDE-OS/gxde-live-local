#!/bin/bash
################################
# 用于配置启动好的 Live 环境
################################
# 卸载安装程序
apt purge calamares -y
apt purge deepin-installer -y
# 强制关闭进程
killall calamares deepin-installer -9
exec init
