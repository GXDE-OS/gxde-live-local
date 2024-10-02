#!/usr/bin/env python3
import os
import sys
import pycdlib
import subprocess


class LiveISO:
    m_iso = pycdlib.PyCdlib()
    m_vmlinuzInitrdSearchPath = "/LIVE/"
    def __init__(self, isoPath):
        self.m_iso.open(isoPath)

    def showList(self, iso_path: str):
        file_list = []
        for i in self.m_iso.list_children(iso_path=iso_path):
            name = str(i.file_identifier(), encoding = "utf-8")
            if (name == ".." or
                name == "."):
                continue
            file_list.append(name)
        return file_list
    
    def vmlinuzPath(self):
        liveList = self.showList(self.m_vmlinuzInitrdSearchPath)
        for i in liveList:
            if ("VMLINU" in i):
                return self.m_vmlinuzInitrdSearchPath + i
        return None
    
    def initrdPath(self):
        liveList = self.showList(self.m_vmlinuzInitrdSearchPath)
        for i in liveList:
            if ("INITRD" in i):
                return self.m_vmlinuzInitrdSearchPath + i
        return None
    
    def filesystemPath(self):
        liveList = self.showList(self.m_vmlinuzInitrdSearchPath)
        for i in liveList:
            if ("FILESYSTEM" in i):
                return self.m_vmlinuzInitrdSearchPath + i
        return None
            
    def extractVmlinuz(self, extractPath):
        vmlinuzPath = self.vmlinuzPath()
        self.extractFile(vmlinuzPath, extractPath)
        

    def extractInitrd(self, extractPath):
        initrdPath = self.initrdPath()
        self.extractFile(initrdPath, extractPath)

    def extractFilesystem(self, extractPath):
        filesystemPath = self.filesystemPath()
        self.extractFile(filesystemPath, extractPath)

    def extractFile(self, iso_path, local_path):
        file = open(local_path, "wb+")
        # 分块读取写入以减少内存使用
        with self.m_iso.open_file_from_iso(iso_path=iso_path) as infp:
            while True:
                data = infp.read(10 * 1024 * 1024)
                if (data == b''):
                    break
                file.write(data)
        file.close()

def RootChecked():
    if (subprocess.getoutput("whoami") != "root"):
        print("请使用 root 运行或者使用 sudo")
        exit(1)

def ShowHelp():
    print(f"{sys.argv[0]} GXDE OS ISO 路径")

def UpdateGrub():
    os.system("update-grub")

if (len(sys.argv) <= 1):
    print("参数不足")
    ShowHelp()
    exit(1)

# 权限检测
RootChecked()

livePath = sys.argv[1]
bootInstallPath = "/boot/gxde/"
liveDiskInstallPath = "/recovery_live"

# 新建所需文件夹（如果不存在）
if (not os.path.exists(bootInstallPath)):
    os.makedirs(bootInstallPath)
if (not os.path.exists(liveDiskInstallPath)):
    os.makedirs(liveDiskInstallPath)

iso = LiveISO(sys.argv[1])
print("提取 vmlinuz")
iso.extractVmlinuz(f"{bootInstallPath}/vmlinuz-gxde")
print("提取 initrd.img")
iso.extractInitrd(f"{bootInstallPath}/initrd.img-gxde")
print("提取 filesystem.squashfs")
iso.extractFilesystem(f"{liveDiskInstallPath}/filesystem.squashfs")
print("提取完成！加载 grub")
UpdateGrub()
print("完成！重启后即可在 grub 寻找入口")