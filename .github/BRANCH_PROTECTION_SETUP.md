# 分支保护规则配置指南

为了确保 PR 必须通过依赖安全检查才能合并，需要在 GitHub 仓库中配置分支保护规则。

## 配置步骤

### 1. 进入仓库设置

1. 打开你的 GitHub 仓库
2. 点击 **Settings**（设置）标签
3. 在左侧菜单中找到 **Branches**（分支）

### 2. 添加分支保护规则

1. 点击 **Add rule**（添加规则）或 **Add branch protection rule**（添加分支保护规则）
2. 在 **Branch name pattern**（分支名称模式）中输入：
   - `main` 或 `master`（根据你的默认分支名称）

### 3. 配置必需的状态检查

1. 勾选 **Require status checks to pass before merging**（合并前必须通过状态检查）
2. 勾选 **Require branches to be up to date before merging**（合并前分支必须是最新的）
3. 在 **Status checks that are required**（必需的状态检查）中，搜索并勾选：
   - `Dependency Security Check / OWASP Dependency Check`
   
   > **注意**：状态检查名称格式为 `{workflow名称} / {job名称}`
   > - Workflow 名称：`Dependency Security Check`（来自 workflow 文件的 `name` 字段）
   > - Job 名称：`OWASP Dependency Check`（来自 job 的 `name` 字段）

### 4. 其他推荐设置

- ✅ **Require pull request reviews before merging**（合并前需要 PR 审查）
- ✅ **Require conversation resolution before merging**（合并前需要解决对话）
- ✅ **Do not allow bypassing the above settings**（不允许绕过上述设置）

### 5. 保存设置

点击页面底部的 **Create**（创建）或 **Save changes**（保存更改）

## 验证配置

配置完成后，当你创建 PR 时：

1. ✅ PR 页面会显示 "Required" 标签，表示这是必需的状态检查
2. ✅ 在 Actions 完成之前，**Merge** 按钮会被禁用
3. ✅ 如果检查失败，**Merge** 按钮会显示错误提示
4. ✅ 只有所有必需检查通过后，才能合并 PR

## 状态检查名称说明

如果找不到状态检查，可以：

1. 先提交一次 PR，让 workflow 运行一次
2. 运行完成后，在 PR 页面的检查列表中查看完整的状态检查名称
3. 然后在分支保护规则中使用这个确切的名称

## 常见问题

### Q: 为什么 Merge 按钮仍然可以点击？

**A:** 可能的原因：
1. 分支保护规则未正确配置
2. 状态检查名称不匹配（需要完全一致）
3. 你是仓库管理员且允许绕过保护规则
4. workflow 还没有运行完成（需要等待第一次运行）

### Q: 如何查看状态检查的确切名称？

**A:** 
1. 创建一个测试 PR
2. 等待 workflow 运行
3. 在 PR 页面的检查部分，查看状态检查的完整名称
4. 复制这个名称到分支保护规则中

### Q: 可以配置多个必需的状态检查吗？

**A:** 可以。在分支保护规则中，可以勾选多个状态检查，所有检查都必须通过才能合并。

## 组织级配置

如果你的组织有多个仓库，可以考虑：

1. 在组织级别设置默认的分支保护规则
2. 使用 GitHub API 批量配置
3. 使用 Terraform 等基础设施即代码工具管理配置

## 参考链接

- [GitHub 分支保护规则文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions 状态检查文档](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/using-workflow-run-logs)

