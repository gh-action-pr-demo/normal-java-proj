# 分支保护规则配置指南

**重要**：为了确保 PR 必须通过依赖安全检查才能合并，**必须**配置分支保护规则。

## ⚠️ 问题说明

如果没有配置分支保护规则，会出现以下问题：
- ❌ PR 提交后，即使 Actions 还在运行，**Merge pull request** 按钮仍然可以点击
- ❌ Actions 失败后，**Merge pull request** 按钮仍然可以点击
- ❌ 无法强制要求通过安全检查才能合并

**解决方案**：配置分支保护规则，将 Actions 状态检查设置为必需检查。

## 配置步骤

### 1. 进入仓库设置

1. 打开你的 GitHub 仓库
2. 点击 **Settings**（设置）标签
3. 在左侧菜单中找到 **Branches**（分支）

### 2. 添加分支保护规则

1. 点击 **Add rule**（添加规则）或 **Add branch protection rule**（添加分支保护规则）
2. 在 **Branch name pattern**（分支名称模式）中输入：
   - `main` 或 `master`（根据你的默认分支名称）

### 3. 配置必需的状态检查（**关键步骤**）

这是最重要的步骤，必须正确配置才能阻止在 Actions 完成前或失败时合并 PR。

1. **勾选 "Require status checks to pass before merging"**（合并前必须通过状态检查）
   - 这个选项会强制要求所有必需的状态检查通过后才能合并
   - **必须勾选**，否则无法阻止合并

2. **勾选 "Require branches to be up to date before merging"**（合并前分支必须是最新的）
   - 确保 PR 基于最新的主分支代码
   - **强烈建议勾选**

3. **添加必需的状态检查**
   - 在 **"Status checks that are required"**（必需的状态检查）区域
   - 点击搜索框，输入：`Dependency Security Check`
   - 找到并勾选：**`Dependency Security Check / OWASP Dependency Check`**
   
   > **⚠️ 重要提示**：
   > - 状态检查名称格式为 `{workflow名称} / {job名称}`
   > - Workflow 名称：`Dependency Security Check`（来自 `.github/workflows/dependency-check.yml` 文件的 `name` 字段）
   > - Job 名称：`OWASP Dependency Check`（来自 job 的 `name` 字段）
   > - **名称必须完全匹配**，包括大小写和空格
   > - 如果找不到状态检查，请先让 workflow 运行一次（见下方"状态检查名称说明"）

### 4. 其他推荐设置

- ✅ **Require pull request reviews before merging**（合并前需要 PR 审查）
  - 建议至少需要 1 个审查者批准
- ✅ **Require conversation resolution before merging**（合并前需要解决对话）
  - 确保所有评论和问题都已解决
- ✅ **Do not allow bypassing the above settings**（不允许绕过上述设置）
  - **强烈建议勾选**，防止管理员绕过保护规则
  - 这样可以确保即使有管理员权限，也必须通过检查才能合并

### 5. 保存设置

点击页面底部的 **Create**（创建）或 **Save changes**（保存更改）

## 验证配置

配置完成后，当你创建 PR 时，应该看到以下行为：

### ✅ 正确配置后的表现

1. **PR 页面显示 "Required" 标签**
   - 在 PR 页面的检查部分，会显示 "Required" 标签
   - 表示这是必需的状态检查

2. **Actions 运行期间，Merge 按钮被禁用**
   - 在 Actions 完成之前，**Merge pull request** 按钮会显示为灰色/禁用状态
   - 按钮上会显示类似 "Waiting for status checks to pass" 的提示

3. **Actions 失败时，Merge 按钮被禁用**
   - 如果检查失败，**Merge pull request** 按钮会显示错误提示
   - 按钮上会显示类似 "Required status check failed" 的提示
   - **无法点击合并**

4. **只有所有检查通过后，才能合并**
   - 当所有必需的状态检查都通过后，**Merge pull request** 按钮才会变为可点击状态
   - 按钮上会显示 "All checks have passed"

### 🔍 如何验证配置是否正确

1. 创建一个测试 PR
2. 观察 PR 页面的检查部分：
   - 应该看到 "Dependency Security Check / OWASP Dependency Check" 状态检查
   - 应该显示 "Required" 标签
3. 在 Actions 运行期间：
   - **Merge pull request** 按钮应该是禁用状态（灰色）
   - 无法点击
4. 如果 Actions 失败：
   - **Merge pull request** 按钮应该仍然是禁用状态
   - 显示错误提示

## 状态检查名称说明

如果找不到状态检查，可以：

1. 先提交一次 PR，让 workflow 运行一次
2. 运行完成后，在 PR 页面的检查列表中查看完整的状态检查名称
3. 然后在分支保护规则中使用这个确切的名称

## 常见问题

### Q: 为什么 Merge 按钮仍然可以点击？（即使 Actions 还在运行或已失败）

**A:** 这是最常见的问题，可能的原因和解决方法：

1. **分支保护规则未正确配置** ⚠️ **最常见**
   - 检查是否勾选了 "Require status checks to pass before merging"
   - 检查是否添加了正确的状态检查名称
   - **解决方法**：按照上面的步骤重新配置

2. **状态检查名称不匹配** ⚠️ **很常见**
   - 状态检查名称必须完全匹配，包括大小写和空格
   - **解决方法**：
     - 先让 workflow 运行一次
     - 在 PR 页面的检查部分查看完整的状态检查名称
     - 复制这个确切的名称到分支保护规则中

3. **workflow 还没有运行完成** ⚠️ **首次配置时常见**
   - 首次配置时，需要先让 workflow 运行一次，GitHub 才能识别状态检查
   - **解决方法**：
     - 创建一个测试 PR
     - 等待 workflow 运行完成
     - 然后在分支保护规则中添加状态检查

4. **你是仓库管理员且允许绕过保护规则**
   - 如果勾选了 "Do not allow bypassing the above settings"，管理员也无法绕过
   - **解决方法**：确保勾选了 "Do not allow bypassing the above settings"

5. **分支名称不匹配**
   - 分支保护规则只对匹配的分支生效
   - **解决方法**：确保分支保护规则的分支名称模式匹配你的主分支（main 或 master）

### Q: 如何确认状态检查名称是否正确？

**A:** 按以下步骤操作：

1. 创建一个测试 PR（或使用现有的 PR）
2. 等待 workflow 运行（至少开始运行）
3. 在 PR 页面，找到 "Checks"（检查）部分
4. 查看状态检查的完整名称，应该类似：
   ```
   Dependency Security Check / OWASP Dependency Check
   ```
5. 复制这个**完整的名称**（包括空格和斜杠）
6. 在分支保护规则中，搜索并勾选这个确切的名称

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

