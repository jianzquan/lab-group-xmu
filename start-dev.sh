#!/bin/bash

# Hugo本地调试启动脚本
# 用于DeepLIT Group网站的本地开发

echo "🚀 启动Hugo开发服务器..."
echo "📍 项目：厦门大学DeepLIT研究组网站"
echo ""

# 检查Hugo是否安装
if ! command -v hugo &> /dev/null; then
    echo "❌ Hugo未安装，请先安装Hugo："
    echo "   brew install hugo"
    exit 1
fi

# 检查网络连接到GitHub
echo "🌐 检查网络连接..."
if ! curl -s --head https://github.com | head -n 1 | grep -q "200 OK"; then
    echo "⚠️  无法连接到GitHub，将使用本地模块模式"
    
    # 创建themes目录结构
    mkdir -p themes/hugoblox
    
    # 复制本地模块到themes目录（如果不存在）
    if [ ! -d "themes/hugoblox/modules" ]; then
        echo "📦 设置本地主题..."
        cp -r "v5@v5.9.8-0.20241012174104-661cadc17327"/* themes/hugoblox/
    fi
    
    # 使用本地主题启动
    echo "🎯 使用本地主题启动开发服务器..."
    hugo server -D --theme hugoblox --port 1313 --bind 127.0.0.1
else
    echo "✅ 网络连接正常"
    echo "🎯 启动开发服务器..."
    hugo server -D --port 1313 --bind 127.0.0.1
fi
