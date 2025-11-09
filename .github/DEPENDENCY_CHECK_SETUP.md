# 依赖安全检查完整配置指南

本文档提供完整的依赖安全检查配置和使用指南，包含所有配置步骤、预期效果和常见问题解答。

## 📋 目录

1. [功能概述](#功能概述)
2. [快速开始](#快速开始)
3. [详细配置步骤](#详细配置步骤)
4. [预期效果](#预期效果)
5. [高级功能](#高级功能)
6. [常见问题](#常见问题)
7. [故障排除](#故障排除)

---

## 功能概述

### 核心功能

- ✅ **自动依赖安全扫描**：使用 OWASP Dependency-Check 检测已知安全漏洞（CVE）
- ✅ **PR 时自动检查**：提交 PR 时自动触发安全检查
- ✅ **强制通过检查**：配置分支保护规则后，必须通过检查才能合并
- ✅ **详细报告**：生成 HTML 和 JSON 格式的详细报告
- ✅ **依赖更新检查**：检查依赖是否有新版本可用
- ✅ **灵活控制**：支持跳过检查（配置文件或 PR 评论）

### 解决的问题

- ❌ **问题**：PR 提交后，即使 Actions 还在运行，Merge 按钮仍然可以点击
- ✅ **解决**：配置分支保护规则后，Actions 运行期间 Merge 按钮会被禁用

- ❌ **问题**：Actions 失败后，Merge 按钮仍然可以点击
- ✅ **解决**：配置分支保护规则后，Actions 失败时 Merge 按钮会被禁用

- ❌ **问题**：无法强制要求通过安全检查才能合并
- ✅ **解决**：通过分支保护规则强制要求状态检查通过

---

## 快速开始

### 1. 项目已包含的配置

项目已经包含了以下配置：
- ✅ `.github/workflows/dependency-check.yml` - GitHub Actions workflow
- ✅ `pom.xml` - Maven 配置（包含 OWASP Dependency-Check 插件）
- ✅ `dependency-check-suppression.xml` - 抑制规则配置

### 2. 必须配置的分支保护规则

**⚠️ 重要**：必须配置分支保护规则才能实现强制检查功能。

#### 快速配置步骤

1. 进入仓库 **Settings → Branches**
2. 添加分支保护规则（针对 `main` 或 `master`）
3. **必须勾选**：`Require status checks to pass before merging`
4. **必须添加**：状态检查 `Dependency Security Check / OWASP Dependency Check`
5. **强烈建议勾选**：`Do not allow bypassing the above settings`
6. 保存设置

#### 详细配置指南

请参考：[分支保护规则配置指南](BRANCH_PROTECTION_SETUP.md)

---

## 详细配置步骤

### 步骤 1：验证项目配置

确认以下文件存在且配置正确：

```bash
# 检查 workflow 文件
ls -la .github/workflows/dependency-check.yml

# 检查 Maven 配置
grep -A 10 "dependency-check-maven" pom.xml

# 检查抑制规则文件
ls -la dependency-check-suppression.xml
```

### 步骤 2：配置分支保护规则

这是**最关键**的步骤，必须正确配置才能阻止在 Actions 完成前或失败时合并 PR。

#### 详细步骤

1. **进入仓库设置**
   - 打开 GitHub 仓库
   - 点击 **Settings** → **Branches**

2. **添加分支保护规则**
   - 点击 **Add rule** 或 **Add branch protection rule**
   - 在 **Branch name pattern** 中输入：`main` 或 `master`

3. **配置必需的状态检查**（**关键步骤**）
   - ✅ 勾选 **"Require status checks to pass before merging"**
   - ✅ 勾选 **"Require branches to be up to date before merging"**
   - ✅ 在状态检查列表中添加：**`Dependency Security Check / OWASP Dependency Check`**
   - ⚠️ **注意**：状态检查名称必须完全匹配（包括大小写和空格）

4. **其他推荐设置**
   - ✅ 勾选 **"Do not allow bypassing the above settings"**
   - （可选）配置 PR 审查要求

5. **保存设置**
   - 点击 **Create** 或 **Save changes**

### 步骤 3：验证配置

创建一个测试 PR，验证以下行为：

- ✅ Actions 运行期间，**Merge pull request** 按钮被禁用（灰色）
- ✅ Actions 失败时，**Merge pull request** 按钮被禁用，显示错误提示
- ✅ 所有检查通过后，**Merge pull request** 按钮变为可点击状态

---

## 预期效果

### 1. PR 提交后的行为

#### Actions 运行期间

- **Merge pull request** 按钮状态：**禁用（灰色）**
- 按钮提示：`Waiting for status checks to pass`
- 无法点击合并

#### Actions 失败时

- **Merge pull request** 按钮状态：**禁用（灰色）**
- 按钮提示：`Required status check failed`
- PR 评论中会显示详细的失败信息（见下方）
- 无法点击合并

#### Actions 成功时

- **Merge pull request** 按钮状态：**可点击**
- 按钮提示：`All checks have passed`
- 可以正常合并

### 2. PR 评论内容

#### 检查失败时的评论

当检查失败时，会在 PR 中自动添加评论，包含：

- 🔒 失败标题和说明
- 📋 检查结果摘要
- 🚨 发现的高风险漏洞列表（表格格式）
- 📊 详细报告链接（Artifacts）
- 💡 修复建议
- 📝 原始检查结果（Markdown 代码块）

#### 检查成功时的行为

- 不会添加评论（避免噪音）
- 状态检查显示为通过
- 可以正常合并

### 3. 报告位置

检查完成后，可以在以下位置查看报告：

- **GitHub Actions Artifacts**：`dependency-check-reports`
  - HTML 报告：`dependency-check-report.html`
  - JSON 报告：`dependency-check-report.json`
  - 依赖更新：`dependency-updates.txt`（Markdown 格式）

- **本地运行**（如果使用本地脚本）：
  - HTML：`target/dependency-check-reports/dependency-check-report.html`
  - JSON：`target/dependency-check-reports/dependency-check-report.json`

---

## 高级功能

### 1. 跳过检查功能

在某些情况下，你可能需要跳过依赖安全检查。支持两种方式：

#### 方式 1：配置文件控制

在项目根目录创建 `.github/dependency-check-skip` 文件：

```bash
# 创建跳过检查文件
touch .github/dependency-check-skip
```

如果此文件存在，workflow 会自动跳过检查并标记为成功。

#### 方式 2：PR 评论控制

在 PR 中添加评论，包含以下关键字之一：

- `[skip dependency check]`
- `[skip-dependency-check]`
- `[skip dependency-check]`
- `[skip-dependency check]`

**示例评论**：
```
[skip-dependency-check] 本次 PR 不涉及依赖变更，跳过检查
```

**注意**：
- 关键字不区分大小写
- 必须由具有写权限的用户评论
- **评论后会自动触发 workflow 重新运行**
- 如果检测到跳过关键字，检查会被跳过并标记为成功
- 如果后续有新的 commit，将重新执行检查（忽略之前的 skip 评论）

**重要提示**：
- 确保 workflow 文件位于 `.github/workflows/` 目录下
- 确保仓库的 Actions 权限已启用
- 如果评论后没有触发 workflow，请检查：
  1. 仓库 Settings → Actions → General → 确保 "Allow all actions and reusable workflows" 已启用
  2. 确保评论是在 PR 上，而不是在普通的 Issue 上
  3. 可以尝试手动触发：Actions → Dependency Security Check → Run workflow

### 2. 自定义 CVSS 阈值

在 `pom.xml` 中修改 CVSS 阈值：

```xml
<configuration>
    <failBuildOnCVSS>7.0</failBuildOnCVSS>  <!-- 修改为你需要的阈值 -->
</configuration>
```

### 3. 自定义抑制规则

编辑 `dependency-check-suppression.xml` 文件，添加需要忽略的依赖或 CVE：

```xml
<!-- 忽略特定的 CVE -->
<suppress>
    <notes>忽略特定的 CVE</notes>
    <cve>CVE-2024-12345</cve>
</suppress>

<!-- 忽略特定依赖包的所有漏洞 -->
<suppress>
    <notes>忽略特定依赖包的所有漏洞</notes>
    <packageUrl regex="true">pkg:maven/com\.example/.*@.*</packageUrl>
</suppress>
```

### 4. 依赖更新检查格式

依赖更新检查结果会以 Markdown 表格格式输出，方便在 PR 评论中查看。

---

## 常见问题

### Q1: 为什么 Merge 按钮仍然可以点击？（即使 Actions 还在运行或已失败）

**A:** 这是最常见的问题，可能的原因：

1. **分支保护规则未正确配置** ⚠️ **最常见**
   - 检查是否勾选了 "Require status checks to pass before merging"
   - 检查是否添加了正确的状态检查名称

2. **状态检查名称不匹配** ⚠️ **很常见**
   - 状态检查名称必须完全匹配：`Dependency Security Check / OWASP Dependency Check`
   - 包括大小写和空格

3. **workflow 还没有运行完成**
   - 首次配置时，需要先让 workflow 运行一次
   - GitHub 才能识别状态检查

**解决方法**：参考 [分支保护规则配置指南](BRANCH_PROTECTION_SETUP.md)

### Q2: 如何查看状态检查的确切名称？

**A:** 
1. 创建一个测试 PR
2. 等待 workflow 运行（至少开始运行）
3. 在 PR 页面的 "Checks" 部分查看完整的状态检查名称
4. 复制这个确切的名称到分支保护规则中

### Q3: 可以跳过检查吗？

**A:** 可以，支持两种方式：
1. 创建 `.github/dependency-check-skip` 文件
2. 在 PR 中添加评论：`[skip dependency check]`

详见 [跳过检查功能](#1-跳过检查功能)

### Q4: 如何修改 CVSS 阈值？

**A:** 在 `pom.xml` 中修改 `failBuildOnCVSS` 配置：

```xml
<failBuildOnCVSS>7.0</failBuildOnCVSS>  <!-- 修改为你需要的阈值 -->
```

### Q5: GitHub 评论区可以渲染 HTML 吗？

**A:** GitHub 的 PR 评论不支持直接渲染 HTML，但支持：
- Markdown 格式（表格、代码块、链接等）
- 依赖更新检查结果已优化为 Markdown 表格格式
- 安全检查结果以 Markdown 表格和代码块格式展示

### Q6: 如何查看详细的检查报告？

**A:** 
1. 在 PR 页面的 Actions 运行结果中下载 Artifacts
2. 解压后查看 `dependency-check-report.html`（浏览器打开）
3. 或查看 `dependency-check-report.json`（程序化处理）

---

## 故障排除

### 问题 1：找不到状态检查

**症状**：在分支保护规则中找不到状态检查

**解决方法**：
1. 先创建一个测试 PR，让 workflow 运行一次
2. 运行完成后，在 PR 页面的检查部分查看完整的状态检查名称
3. 复制这个确切的名称到分支保护规则中

### 问题 2：Actions 被禁用

**症状**：看到 "GitHub Actions hosted runners are disabled" 错误

**解决方法**：
- 参考 [GitHub Actions 被禁用时的解决方案](GITHUB_ACTIONS_DISABLED.md)
- 或使用本地检查脚本：`./scripts/check-dependencies.sh`

### 问题 3：检查时间过长

**症状**：依赖检查运行时间很长

**解决方法**：
- 这是正常现象，OWASP Dependency-Check 需要下载漏洞数据库
- 首次运行会更慢，后续运行会使用缓存
- 可以考虑使用自托管运行器或增加缓存配置

### 问题 4：误报的漏洞

**症状**：检查报告了误报的漏洞

**解决方法**：
- 在 `dependency-check-suppression.xml` 中添加抑制规则
- 参考 [自定义抑制规则](#3-自定义抑制规则)

---

## 参考文档

- [分支保护规则配置指南](BRANCH_PROTECTION_SETUP.md)
- [分支保护规则检查清单](BRANCH_PROTECTION_CHECKLIST.md)
- [GitHub Actions 被禁用时的解决方案](GITHUB_ACTIONS_DISABLED.md)
- [README.md](../README.md)

## 相关链接

- [OWASP Dependency-Check 文档](https://jeremylong.github.io/DependencyCheck/)
- [GitHub 分支保护规则文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

**最后更新**：2024年

**维护者**：项目团队

