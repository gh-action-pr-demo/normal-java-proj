# Spring Boot 依赖安全检查项目

这是一个演示项目，展示如何使用 OWASP Dependency-Check 和 GitHub Actions 在 PR 时自动检查依赖安全漏洞。

## 📚 完整配置指南

**👉 [查看完整配置指南](.github/DEPENDENCY_CHECK_SETUP.md)** - 包含所有配置步骤、预期效果和常见问题解答

## 功能特性

- ✅ 自动依赖安全扫描（OWASP Dependency-Check）
- ✅ PR 时自动检查，发现高风险漏洞阻止合并
- ✅ 支持自定义抑制规则（忽略特定依赖或 CVE）
- ✅ 依赖版本更新检查（versions-maven-plugin）
- ✅ 详细的 HTML 和 JSON 报告
- ✅ 支持组织级集中配置（可重用 workflow）
- ✅ **跳过检查功能**：支持通过配置文件或 PR 评论跳过检查
- ✅ **优化的 PR 评论**：失败时自动添加详细结果和链接

## 项目结构

```
.
├── pom.xml                                    # Maven 配置，包含 Dependency-Check 插件
├── dependency-check-suppression.xml          # 项目级抑制规则配置
├── .github/
│   └── workflows/
│       ├── dependency-check.yml              # 单项目独立 workflow（方案 B）
│       ├── reusable-dependency-check.yml     # 可重用 workflow（方案 A）
│       └── example-reusable-usage.yml        # 使用可重用 workflow 的示例
└── src/
    └── main/
        └── java/
            └── com/example/demo/
                ├── DemoApplication.java
                └── HelloController.java
```

## 快速开始

### 本地运行

```bash
# 编译项目
mvn clean compile

# 运行依赖安全检查
mvn verify

# 查看报告
open target/dependency-check-reports/dependency-check-report.html

# 检查依赖更新
mvn versions:display-dependency-updates
```

### GitHub Actions

当提交 PR 时，GitHub Actions 会自动：
1. 运行 OWASP Dependency-Check 扫描
2. 检查依赖版本更新
3. 如果发现高风险漏洞（CVSS >= 7.0），阻止 PR 合并
4. 上传详细报告到 Artifacts
5. 在 PR 中评论检查结果

## 配置说明

### CVSS 阈值

在 `pom.xml` 中配置 CVSS 阈值：

```xml
<configuration>
    <failBuildOnCVSS>7.0</failBuildOnCVSS>
</configuration>
```

### 自定义抑制规则

编辑 `dependency-check-suppression.xml` 文件，添加需要忽略的依赖或 CVE：

```xml
<suppress>
    <notes>忽略特定的 CVE</notes>
    <cve>CVE-2024-12345</cve>
</suppress>

<suppress>
    <notes>忽略特定依赖包的所有漏洞</notes>
    <packageUrl regex="true">pkg:maven/com\.example/.*@.*</packageUrl>
</suppress>
```

## 组织级集中配置（方案 A）

### 架构

1. **创建组织级配置仓库**（如 `your-org/.github`）
   - 包含可重用的 workflow
   - 包含共享的 suppression 配置文件

2. **项目级最小配置**
   - 每个项目只需添加一个简单的 workflow 文件（约 10 行）

### 使用可重用 workflow

在项目的 `.github/workflows/dependency-check.yml` 中：

```yaml
name: Dependency Check

on:
  pull_request:
    branches: [main]

jobs:
  dependency-check:
    uses: your-org/.github/.github/workflows/reusable-dependency-check.yml@main
    with:
      java-version: '17'
      fail-on-cvss: '7.0'
      org-suppression-url: 'https://raw.githubusercontent.com/your-org/.github/main/configs/dependency-check-suppression.xml'
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 规则覆盖机制

- **多 suppression 文件合并**：支持同时指定多个 suppression 文件
- **优先级顺序**：项目级 suppression 文件优先于组织级
- **覆盖方式**：项目级可以添加新规则或通过更具体的规则覆盖组织级规则

## 报告说明

检查完成后，可以在以下位置查看报告：

- **HTML 报告**：`target/dependency-check-reports/dependency-check-report.html`
- **JSON 报告**：`target/dependency-check-reports/dependency-check-report.json`
- **依赖更新**：`target/dependency-updates.txt`
- **GitHub Actions**：PR 的 Artifacts 中下载完整报告

## 工具说明

### OWASP Dependency-Check

用于检测项目依赖中的已知安全漏洞（CVE）。

### versions-maven-plugin

用于检查依赖是否有新版本可用，帮助识别可能有安全修复的版本更新。

## 分支保护设置 ⚠️ **必须配置**

**⚠️ 重要**：如果不配置分支保护规则，会出现以下问题：
- ❌ PR 提交后，即使 Actions 还在运行，**Merge pull request** 按钮仍然可以点击
- ❌ Actions 失败后，**Merge pull request** 按钮仍然可以点击
- ❌ 无法强制要求通过安全检查才能合并

**解决方案**：必须配置分支保护规则，将 Actions 状态检查设置为必需检查。

> **📖 详细配置步骤**：请参考 [完整配置指南](.github/DEPENDENCY_CHECK_SETUP.md) 中的"详细配置步骤"章节

### 快速配置步骤

1. 进入 **Settings → Branches**
2. 添加分支保护规则（针对 `main` 或 `master` 分支）
3. **必须勾选**：**"Require status checks to pass before merging"**（合并前必须通过状态检查）
4. **建议勾选**：**"Require branches to be up to date before merging"**（合并前分支必须是最新的）
5. **必须添加**：在状态检查列表中选择：**`Dependency Security Check / OWASP Dependency Check`**
6. **强烈建议勾选**：**"Do not allow bypassing the above settings"**（不允许绕过上述设置）

> **⚠️ 注意**：
> - 状态检查名称格式为 `{workflow名称} / {job名称}`
> - 名称必须完全匹配，包括大小写和空格
> - 如果找不到状态检查，需要先让 workflow 运行一次（见详细配置指南）

### 详细配置指南

**强烈建议阅读**：[.github/BRANCH_PROTECTION_SETUP.md](.github/BRANCH_PROTECTION_SETUP.md)

包含：
- 📋 详细的配置步骤（带截图说明）
- ✅ 验证配置是否正确的方法
- 🔍 常见问题解答（特别是 "Merge 按钮仍然可以点击" 的问题）
- 🛠️ 故障排除指南

### 验证配置

配置完成后，当你创建 PR 时：

- ✅ **Actions 运行期间**：**Merge pull request** 按钮会被禁用（灰色），无法点击
- ✅ **Actions 失败时**：**Merge pull request** 按钮会被禁用，显示错误提示，无法合并
- ✅ **所有检查通过后**：**Merge pull request** 按钮才会变为可点击状态

如果不符合上述行为，请参考 [详细配置指南](.github/BRANCH_PROTECTION_SETUP.md) 进行故障排除。

## 高级功能

### 跳过检查功能

在某些情况下，你可能需要跳过依赖安全检查。支持两种方式：

#### 方式 1：配置文件控制

在项目根目录创建 `.github/dependency-check-skip` 文件：

```bash
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
[skip dependency check] 本次 PR 不涉及依赖变更，跳过检查
```

**注意**：
- 关键字不区分大小写
- 必须由具有写权限的用户评论
- 评论后需要重新触发 workflow（推送新提交或手动触发）

> **📖 更多高级功能**：请参考 [完整配置指南](.github/DEPENDENCY_CHECK_SETUP.md) 中的"高级功能"章节

## GitHub Actions 被禁用时的解决方案

如果你的组织禁用了 GitHub Actions 托管运行器，请参考：

- [.github/GITHUB_ACTIONS_DISABLED.md](.github/GITHUB_ACTIONS_DISABLED.md) - 详细的问题说明和解决方案

### 临时方案：本地检查

在 Actions 启用之前，可以使用本地检查脚本：

```bash
# 运行依赖安全检查
./scripts/check-dependencies.sh

# 或者直接使用 Maven
mvn verify -DskipTests
```

检查脚本会：
- ✅ 检查依赖更新
- ✅ 运行 OWASP Dependency-Check
- ✅ 生成 HTML 和 JSON 报告
- ✅ 如果发现高风险漏洞，返回错误码

## 许可证

MIT License

