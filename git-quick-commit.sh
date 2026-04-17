#!/bin/bash

# ============================================
# 快速 Git 提交脚本
# 一键添加、提交、推送（使用默认信息）
# ============================================

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   快速 Git 提交脚本${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# 检查是否在Git仓库
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}❌ 错误：当前目录不是Git仓库${NC}"
    exit 1
fi

# 检查是否有更改
status=$(git status --porcelain)
if [ -z "$status" ]; then
    echo -e "${YELLOW}⚠️  没有未提交的更改${NC}"
    exit 0
fi

# 显示更改的文件
echo -e "${BLUE}ℹ️  以下文件将被提交：${NC}"
echo "$status" | while read -r line; do
    echo "   $line"
done
echo ""

# 获取当前分支
branch=$(git rev-parse --abbrev-ref HEAD)

# 默认提交信息
commit_msg="feat: 更新代码"

# 如果提供了参数，使用参数作为提交信息
if [ $# -gt 0 ]; then
    commit_msg="$*"
fi

echo -e "${YELLOW}⚠️  提交信息: $commit_msg${NC}"
echo ""

# 执行操作
echo -e "${BLUE}ℹ️  正在添加所有更改...${NC}"
git add -A

echo -e "${BLUE}ℹ️  正在提交...${NC}"
git commit -m "$commit_msg"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 提交成功！${NC}"
    
    # 询问是否推送
    read -p "是否推送到远程？(y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}ℹ️  正在推送到 origin/$branch...${NC}"
        git push origin "$branch"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ 推送成功！${NC}"
        else
            echo -e "${RED}❌ 推送失败${NC}"
        fi
    fi
else
    echo -e "${RED}❌ 提交失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   操作完成！${NC}"
echo -e "${GREEN}============================================${NC}"
