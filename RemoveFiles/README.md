# rm

## 简介
替换rm命令, 使rm的文件放到用户的.Trash目录下, 避免由于rm误删文件

## 安装

``` bash
chmod +x RemoveFiles.py
ln RemoveFiles.py /usr/local/bin/RemoveFiles
```

在.bashrc 或 .zshrc添加
``` bash
alias rm=RemoveFiles
```
