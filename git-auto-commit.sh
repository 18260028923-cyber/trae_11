#!/bin/bash

# ============================================
# 智能 Git 自动提交脚本
# 用于快速提交AI生成的内容和普通代码
# ============================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 函数：打印分隔线
print_separator() {
    echo -e "${CYAN}============================================${NC}"
}

# 函数：打印标题
print_title() {
    print_separator
    echo -e "${PURPLE}   $1${NC}"
    print_separator
    echo ""
}

# 函数：打印成功信息
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 函数：打印错误信息
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 函数：打印警告信息
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 函数：打印信息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 函数：检测文件类型
detect_file_type() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        html|htm) echo "网页" ;;
        css) echo "样式" ;;
        js|ts|tsx|jsx) echo "脚本" ;;
        py) echo "Python" ;;
        md|txt) echo "文档" ;;
        json) echo "配置" ;;
        sh) echo "脚本" ;;
        gitignore|gitattributes) echo "Git配置" ;;
        *) echo "文件" ;;
    esac
}

# 函数：自动生成提交类型
auto_detect_commit_type() {
    local modified_files="$1"
    local has_new=false
    local has_modified=false
    local has_deleted=false
    local has_docs=false
    local has_code=false
    local has_config=false
    
    while IFS= read -r line; do
        status="${line:0:1}"
        file="${line:3}"
        
        case "$status" in
            A|?) has_new=true ;;
            M) has_modified=true ;;
            D) has_deleted=true ;;
        esac
        
        # 检测文件类型
        case "$file" in
            *.md|*.txt|*.rst) has_docs=true ;;
            *.html|*.css|*.js|*.ts|*.py|*.sh) has_code=true ;;
            *.json|*.yml|*.yaml|*.toml|*.gitignore|*.gitattributes) has_config=true ;;
        esac
    done <<< "$modified_files"
    
    # 确定提交类型
    if $has_new; then
        if $has_docs && ! $has_code; then
            echo "docs"
        elif $has_config && ! $has_code && ! $has_docs; then
            echo "chore"
        else
            echo "feat"
        fi
    elif $has_modified; then
        if $has_docs && ! $has_code; then
            echo "docs"
        elif $has_config && ! $has_code && ! $has_docs; then
            echo "chore"
        else
            echo "feat"
        fi
    elif $has_deleted; then
        echo "chore"
    else
        echo "feat"
    fi
}

# 函数：生成提交描述
auto_generate_description() {
    local modified_files="$1"
    local descriptions=()
    
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            continue
        fi
        
        status="${line:0:1}"
        file="${line:3}"
        file_type=$(detect_file_type "$file")
        filename=$(basename "$file")
        
        case "$status" in
            A) descriptions+=("新增$file_type: $filename") ;;
            M) descriptions+=("修改$file_type: $filename") ;;
            D) descriptions+=("删除$file_type: $filename") ;;
            ?) descriptions+=("新增$file_type: $filename") ;;
            *) descriptions+=("更新$file_type: $filename") ;;
        esac
    done <<< "$modified_files"
    
    # 合并描述
    if [ ${#descriptions[@]} -eq 0 ]; then
        echo "更新代码"
    elif [ ${#descriptions[@]} -eq 1 ]; then
        echo "${descriptions[0]}"
    elif [ ${#descriptions[@]} -le 3 ]; then
        local IFS="、"
        echo "${descriptions[*]}"
    else
        echo "${descriptions[0]} 等 ${#descriptions[@]} 个文件"
    fi
}

# 函数：显示状态
show_status() {
    echo ""
    print_info "当前Git状态："
    git status --short
    echo ""
}

# 函数：交互式选择提交类型
select_commit_type() {
    local auto_type="$1"
    
    echo ""
    print_info "请选择提交类型："
    echo ""
    
    local types=("feat: 新功能" "fix: 修复Bug" "docs: 文档更新" "style: 代码格式" "refactor: 重构" "perf: 性能优化" "test: 测试" "chore: 构建/工具" "取消")
    
    select opt in "${types[@]}"; do
        case $REPLY in
            1) echo "feat"; return ;;
            2) echo "fix"; return ;;
            3) echo "docs"; return ;;
            4) echo "style"; return ;;
            5) echo "refactor"; return ;;
            6) echo "perf"; return ;;
            7) echo "test"; return ;;
            8) echo "chore"; return ;;
            9) echo ""; return ;;
            *) print_warning "无效选择，请重试"; continue ;;
        esac
    done
}

# 函数：主流程
main() {
    print_title "智能 Git 自动提交脚本"
    
    # 检查是否在Git仓库中
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        print_error "当前目录不是Git仓库！"
        exit 1
    fi
    
    # 检查当前分支
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    print_info "当前分支: $current_branch"
    
    # 检查是否有未提交的更改
    local status=$(git status --porcelain)
    if [ -z "$status" ]; then
        print_warning "没有未提交的更改！"
        exit 0
    fi
    
    # 显示状态
    show_status
    
    # 自动检测
    local commit_type=$(auto_detect_commit_type "$status")
    local description=$(auto_generate_description "$status")
    
    print_info "自动检测结果："
    echo -e "   类型: ${GREEN}$commit_type${NC}"
    echo -e "   描述: ${GREEN}$description${NC}"
    echo ""
    
    # 确认是否使用自动检测的类型
    read -p "是否使用自动检测的类型？(y/n/选择类型): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        # 让用户选择类型
        commit_type=$(select_commit_type)
        if [ -z "$commit_type" ]; then
            print_info "已取消提交"
            exit 0
        fi
    elif [[ ! $REPLY =~ ^[Yy]$ ]]; then
        # 用户输入了其他内容，让他们选择
        commit_type=$(select_commit_type)
        if [ -z "$commit_type" ]; then
            print_info "已取消提交"
            exit 0
        fi
    fi
    
    # 让用户确认或修改描述
    echo ""
    read -p "请输入提交描述（直接回车使用: $description）: " user_description
    if [ -n "$user_description" ]; then
        description="$user_description"
    fi
    
    # 显示最终的提交信息
    echo ""
    print_info "最终提交信息："
    echo -e "   ${YELLOW}$commit_type: $description${NC}"
    echo ""
    
    # 确认提交
    read -p "确认提交？(y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消提交"
        exit 0
    fi
    
    # 执行提交
    echo ""
    print_info "正在添加所有更改..."
    git add -A
    
    print_info "正在提交..."
    git commit -m "$commit_type: $description"
    
    if [ $? -eq 0 ]; then
        print_success "提交成功！"
        
        # 询问是否推送
        echo ""
        read -p "是否推送到远程仓库？(y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "正在推送到 origin/$current_branch..."
            git push origin "$current_branch"
            
            if [ $? -eq 0 ]; then
                print_success "推送成功！"
            else
                print_error "推送失败，请检查网络或权限"
            fi
        fi
    else
        print_error "提交失败！"
        exit 1
    fi
    
    echo ""
    print_separator
    print_success "操作完成！"
    print_separator
}

# 运行主程序
main
