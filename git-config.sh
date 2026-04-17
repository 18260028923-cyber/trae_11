#!/bin/bash

# ============================================
# Git 快速配置脚本
# 用于快速设置 Git 用户信息和常用配置
# ============================================

echo "============================================"
echo "Git 快速配置脚本"
echo "============================================"
echo ""

# 检查是否已经配置了用户信息
CURRENT_NAME=$(git config --global user.name)
CURRENT_EMAIL=$(git config --global user.email)

echo "当前 Git 配置："
echo "  用户名: ${CURRENT_NAME:-[未配置]}"
echo "  邮箱: ${CURRENT_EMAIL:-[未配置]}"
echo ""

# 询问是否需要更新配置
read -p "是否需要更新 Git 配置？(y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 输入用户名
    read -p "请输入您的用户名: " USER_NAME
    while [ -z "$USER_NAME" ]; do
        read -p "用户名不能为空，请重新输入: " USER_NAME
    done
    
    # 输入邮箱
    read -p "请输入您的邮箱: " USER_EMAIL
    while [ -z "$USER_EMAIL" ]; do
        read -p "邮箱不能为空，请重新输入: " USER_EMAIL
    done
    
    # 配置 Git
    echo ""
    echo "正在配置 Git..."
    
    git config --global user.name "$USER_NAME"
    git config --global user.email "$USER_EMAIL"
    
    # 常用配置
    git config --global color.ui auto
    git config --global core.editor "nano"
    git config --global pull.rebase false
    git config --global init.defaultBranch main
    
    # 设置别名
    git config --global alias.st "status"
    git config --global alias.ci "commit"
    git config --global alias.co "checkout"
    git config --global alias.br "branch"
    git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
    git config --global alias.last "log -1 HEAD"
    git config --global alias.df "diff"
    
    echo ""
    echo "✅ Git 配置完成！"
    echo ""
    echo "新配置："
    echo "  用户名: $(git config --global user.name)"
    echo "  邮箱: $(git config --global user.email)"
else
    echo ""
    echo "使用现有配置。"
fi

echo ""
echo "============================================"
echo "配置完成！"
echo "============================================"
echo ""
echo "常用 Git 命令别名："
echo "  git st     = git status"
echo "  git ci     = git commit"
echo "  git co     = git checkout"
echo "  git br     = git branch"
echo "  git lg     = 彩色图形化日志"
echo "  git last   = 显示最后一次提交"
echo "  git df     = git diff"
echo ""
