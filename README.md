# GXDE 本地应急急救系统
支持将 GXDE 的安装镜像部署至本地，以便在主系统崩溃时可以在 grub 引导菜单切换到应急系统进行系统恢复、数据备份等，无需使用启动盘  
（注：目前只支持命令操作，后续将会在控制中心添加快捷入口）  

## 命令
```bash
gxde-live-local --help  # 查看帮助
gxde-live-local set GXDE ISO 路径  # 从 ISO 提取 live 镜像
gxde-live-local del  # 移除安装到本地的 live 镜像
gxde-live-local check  # 检测是否已经安装到本地
```