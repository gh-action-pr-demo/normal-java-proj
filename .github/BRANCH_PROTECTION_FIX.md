# 分支保护规则配置问题修复指南

## 问题描述

当前分支保护规则配置过于严格，导致无法推送新分支。错误信息：
```
Required status check "Dependency Security Check / OWASP Dependency Check" is expected.
```

## 原因分析

分支保护规则可能被应用到了所有分支，而不仅仅是 `main`/`master` 分支。这会导致：
- 无法创建新分支
- 无法推送代码（因为还没有运行过检查）

## 解决方案

### 方案 1：调整分支保护规则（推荐）

1. 进入 GitHub 仓库：**Settings → Branches**
2. 找到当前的分支保护规则
3. 确认 **Branch name pattern** 只匹配主分支：
   - 应该设置为：`main` 或 `master`
   - **不应该**设置为：`*`（匹配所有分支）
4. 如果规则应用到了所有分支，需要：
   - 删除或修改该规则
   - 创建一个新规则，只保护 `main` 或 `master`

### 方案 2：临时禁用规则推送代码

如果需要立即推送代码：

1. 进入 **Settings → Branches**
2. 临时禁用或删除分支保护规则
3. 推送代码到新分支
4. 创建 PR
5. 重新启用分支保护规则（只保护 main/master）

### 方案 3：通过 GitHub Web 界面创建分支

1. 在 GitHub Web 界面创建新分支
2. 通过 Web 编辑器添加文件
3. 创建 PR

## 正确的分支保护规则配置

### 应该保护的分支
- ✅ `main`
- ✅ `master`
- ✅ `release/*`（如果需要）

### 不应该保护的分支
- ❌ `*`（所有分支）
- ❌ `feature/*`（功能分支）
- ❌ `develop`（开发分支，如果需要）

### 推荐配置

**规则 1：保护主分支**
- Branch name pattern: `main` 或 `master`
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- Status check: `Dependency Security Check / OWASP Dependency Check`

**规则 2：保护发布分支（可选）**
- Branch name pattern: `release/*`
- ✅ Require status checks to pass before merging
- Status check: `Dependency Security Check / OWASP Dependency Check`

## 验证配置

配置完成后：

1. ✅ 可以创建和推送新分支
2. ✅ 创建 PR 时，Actions 会自动运行
3. ✅ PR 合并到 main 时，必须通过检查
4. ✅ 直接推送到 main 时，必须通过检查

## 当前工作流程

正确的流程应该是：

1. **创建功能分支**（不受保护）
   ```bash
   git checkout -b feature/my-feature
   ```

2. **推送代码**（不受限制）
   ```bash
   git push origin feature/my-feature
   ```

3. **创建 PR**（触发检查）
   - 在 GitHub 上创建 PR：`feature/my-feature` → `main`
   - Actions 自动运行检查
   - Merge 按钮在检查完成前被禁用

4. **合并 PR**（需要检查通过）
   - 检查通过后，Merge 按钮可用
   - 合并到 main 分支

## 下一步操作

请按照以下步骤操作：

1. 进入 GitHub 仓库的 **Settings → Branches**
2. 检查当前的分支保护规则
3. 确保规则只应用到 `main` 或 `master` 分支
4. 如果规则应用到所有分支，请修改或删除
5. 重新尝试推送代码

