#!/bin/bash
################################
# 用于配置启动好的 Live 环境
################################
# 卸载安装程序
sudo apt purge calamares -y
sudo apt purge deepin-installer -y
# 强制关闭进程
sudo killall calamares deepin-installer -9
