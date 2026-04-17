# Git 使用规范与标准流程

本文档记录了项目的 Git 使用规范，方便团队协作和后续维护。

---

## 一、当前项目配置

### 1. 仓库信息
- **远程仓库**: `https://github.com/18260028923-cyber/trae_11.git`
- **当前分支**: `main` (唯一主分支)

### 2. 本地用户配置
```bash
# 查看当前配置
git config --global user.name
git config --global user.email

# 修改配置
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

### 3. 快速配置脚本
项目根目录下有 `git-config.sh` 脚本，可以一键配置 Git：
```bash
# 运行配置脚本
chmod +x git-config.sh
./git-config.sh
```

---

## 二、分支管理策略

### 采用策略：简单直接（仅 main 分支）

**适用场景**: 个人开发、小型项目、快速迭代

**优点**: 
- 简单直观，学习成本低
- 减少分支管理的复杂性
- 适合个人独立开发

**工作流程**:
```
main:  ──○───○───○───○───▶
        提交  提交  提交  提交
```

### 常用分支命令

```bash
# 查看所有分支
git branch -a

# 查看当前分支
git branch

# 创建新分支（如果需要临时开发）
git checkout -b feature-xxx

# 切换到 main 分支
git checkout main

# 合并分支到 main
git checkout main
git merge feature-xxx

# 删除已合并的分支
git branch -d feature-xxx

# 强制删除分支（未合并）
git branch -D feature-xxx
```

---

## 三、提交信息规范 (Conventional Commits)

### 规范格式

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Type 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | feat: 添加用户登录功能 |
| `fix` | 修复 Bug | fix: 修复登录页面崩溃问题 |
| `docs` | 文档更新 | docs: 更新 README 文档 |
| `style` | 代码格式（不影响功能） | style: 格式化代码，修复缩进 |
| `refactor` | 重构（既不新增功能也不修复 Bug） | refactor: 重构用户认证模块 |
| `perf` | 性能优化 | perf: 优化首页加载速度 |
| `test` | 添加或修改测试 | test: 添加用户登录单元测试 |
| `chore` | 构建/工具相关 | chore: 更新依赖包版本 |
| `ci` | CI 配置 | ci: 添加 GitHub Actions 配置 |
| `revert` | 回滚提交 | revert: 回滚到上一个版本 |

### 好的提交示例

✅ **推荐**:
```bash
# 新功能
git commit -m "feat: 新增UI设计师作品集页面

- 添加响应式布局
- 实现滚动动画效果
- 集成模态框组件"

# 修复 Bug
git commit -m "fix: 修复移动端菜单点击无响应问题

问题原因: 事件绑定在动态生成的元素上
解决方案: 使用事件委托绑定到父元素"

# 文档
git commit -m "docs: 添加 Git 使用规范文档

- 分支管理策略
- 提交信息规范
- 常用命令速查"
```

❌ **不推荐**:
```bash
git commit -m "更新了一些东西"
git commit -m "修复bug"
git commit -m "哈哈哈"
git commit -m "tmp"
```

---

## 四、标准工作流程

### 日常开发流程

```bash
# 1. 确保在 main 分支
git checkout main

# 2. 拉取最新代码
git pull origin main

# 3. 开发（修改文件）
# ... 编写代码 ...

# 4. 查看修改状态
git status

# 5. 添加修改到暂存区
git add .                    # 添加所有修改
# 或
git add 文件名               # 添加指定文件

# 6. 提交代码（使用规范的提交信息）
git commit -m "feat: 添加某某功能

- 功能描述1
- 功能描述2"

# 7. 推送到远程
git push origin main
```

### 临时分支开发流程（如果需要）

```bash
# 1. 从 main 创建功能分支
git checkout main
git checkout -b feature-xxx

# 2. 开发并提交
git add .
git commit -m "feat: xxx功能开发"

# 3. 切换到 main 并拉取最新
git checkout main
git pull origin main

# 4. 合并功能分支
git merge feature-xxx

# 5. 解决冲突（如果有）
# ... 解决冲突 ...
git add .
git commit -m "merge: 合并feature-xxx分支"

# 6. 推送并删除本地分支
git push origin main
git branch -d feature-xxx
```

---

## 五、常用命令速查

### 基础命令

```bash
# 初始化仓库
git init

# 克隆远程仓库
git clone https://github.com/用户名/仓库名.git

# 查看状态
git status

# 查看差异
git diff              # 工作区 vs 暂存区
git diff --staged     # 暂存区 vs 版本库
git diff HEAD         # 工作区 vs 版本库

# 添加到暂存区
git add 文件名
git add .
git add -A            # 添加所有（包括删除的文件）

# 提交
git commit -m "提交信息"
git commit -a -m "提交信息"  # 跳过 git add，直接提交已跟踪的文件

# 撤销操作
git restore 文件名          # 撤销工作区修改
git restore --staged 文件名 # 撤销暂存区（移回工作区）
git reset --soft HEAD~1     # 撤销最近一次提交（保留修改）
git reset --hard HEAD~1     # 撤销最近一次提交（丢弃修改）
```

### 远程操作

```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 修改远程仓库地址
git remote set-url origin 新地址

# 拉取远程代码
git pull origin main

# 推送到远程
git push origin main

# 强制推送（谨慎使用！）
git push -f origin main
```

### 日志查看

```bash
# 查看提交历史
git log
git log --oneline           # 单行显示
git log -n 5                # 显示最近5条
git log --graph             # 图形化显示
git log --stat              # 显示修改统计
git log -p                  # 显示具体修改内容

# 使用配置的别名（推荐）
git lg                      # 彩色图形化日志
git last                    # 显示最后一次提交
```

### 标签操作

```bash
# 查看标签
git tag

# 创建标签
git tag v1.0.0
git tag -a v1.0.0 -m "版本1.0.0"

# 推送标签
git push origin v1.0.0
git push origin --tags      # 推送所有标签

# 删除标签
git tag -d v1.0.0
git push origin :v1.0.0    # 删除远程标签
```

---

## 六、冲突解决

### 场景：合并时出现冲突

```bash
# 1. 合并时出现冲突
Auto-merging 文件名
CONFLICT (content): Merge conflict in 文件名
Automatic merge failed; fix conflicts and then commit the result.

# 2. 查看冲突文件
git status

# 3. 打开文件，手动解决冲突
# 冲突标记：
# <<<<<<< HEAD      当前分支的内容
# =======           分隔线
# >>>>>>> branch    要合并的分支内容

# 4. 标记为已解决
git add 文件名

# 5. 完成合并
git commit -m "merge: 解决冲突并合并分支"
```

### 场景：拉取时出现冲突

```bash
# 方法1：先暂存本地修改，拉取后恢复
git stash
git pull origin main
git stash pop

# 方法2：直接拉取，手动解决冲突
git pull origin main
# ... 解决冲突 ...
git add .
git commit -m "merge: 拉取远程代码并解决冲突"
```

---

## 七、Git 别名配置

以下别名已在 `git-config.sh` 中配置：

```bash
# 查看状态
git st          = git status

# 提交
git ci          = git commit

# 切换分支
git co          = git checkout

# 查看分支
git br          = git branch

# 查看日志（推荐）
git lg          = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# 查看最后一次提交
git last        = git log -1 HEAD

# 查看差异
git df          = git diff
```

---

## 八、最佳实践建议

### 1. 提交粒度
- **小步提交**: 每个提交只做一件事
- **频繁提交**: 不要等到功能完全完成才提交
- **可回滚**: 确保每个提交都是稳定可回滚的

### 2. 提交时机
- ✅ 完成一个小功能后
- ✅ 修复一个 Bug 后
- ✅ 重构部分代码后
- ✅ 更新文档后
- ❌ 不要在下班前一次性提交所有修改
- ❌ 不要提交包含多个不相关功能的代码

### 3. 协作注意事项
- 提交前先 `git pull` 拉取最新代码
- 遇到冲突及时沟通解决
- 不要强制推送 (`git push -f`) 到主分支
- 重要操作前先确认当前分支

### 4. 信息安全
- 永远不要提交敏感信息（密码、密钥、Token）
- 使用 `.gitignore` 忽略不需要提交的文件
- 敏感信息使用环境变量或配置文件

---

## 九、.gitignore 标准配置

项目已包含标准的 `.gitignore` 文件：

```
# 系统文件
.DS_Store
._*
Thumbs.db

# IDE
.idea/
.vscode/
*.swp

# 依赖
node_modules/
vendor/

# 构建产物
dist/
build/

# 环境变量
.env
.env.local
```

---

## 十、快速参考卡片

### 日常开发
```bash
git checkout main          # 切换到主分支
git pull origin main       # 拉取最新代码
# ... 开发 ...
git add .                  # 添加修改
git commit -m "feat: xxx"  # 提交（规范信息）
git push origin main       # 推送远程
```

### 查看状态
```bash
git st                     # 查看状态
git lg                     # 查看日志
git df                     # 查看差异
git last                   # 最后一次提交
```

### 撤销操作
```bash
git restore 文件名          # 撤销工作区修改
git restore --staged 文件名 # 撤销暂存
git reset --soft HEAD~1     # 撤销提交（保留修改）
```

---

**文档版本**: v1.0  
**最后更新**: 2026-04-17  
**维护者**: 18260028923-cyber
