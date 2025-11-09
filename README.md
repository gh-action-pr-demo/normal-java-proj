# Spring Boot 依赖安全检查项目

这是一个演示项目，展示如何使用 OWASP Dependency-Check 和 GitHub Actions 在 PR 时自动检查依赖安全漏洞。

## 功能特性

- ✅ 自动依赖安全扫描（OWASP Dependency-Check）
- ✅ PR 时自动检查，发现高风险漏洞阻止合并
- ✅ 支持自定义抑制规则（忽略特定依赖或 CVE）
- ✅ 依赖版本更新检查（versions-maven-plugin）
- ✅ 详细的 HTML 和 JSON 报告
- ✅ 支持组织级集中配置（可重用 workflow）

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

## 分支保护设置

**重要**：为了确保 PR 必须通过安全检查才能合并，必须配置分支保护规则。

### 快速配置

1. 进入 **Settings → Branches**
2. 添加分支保护规则（针对 `main` 或 `master` 分支）
3. 启用 **"Require status checks to pass before merging"**
4. 启用 **"Require branches to be up to date before merging"**
5. 在状态检查列表中选择：**`Dependency Security Check / OWASP Dependency Check`**

> **注意**：状态检查名称格式为 `{workflow名称} / {job名称}`

### 详细配置指南

请参考 [.github/BRANCH_PROTECTION_SETUP.md](.github/BRANCH_PROTECTION_SETUP.md) 获取详细的配置步骤和常见问题解答。

### 验证配置

配置完成后：
- ✅ Actions 运行期间，Merge 按钮会被禁用
- ✅ 检查失败时，无法合并 PR
- ✅ 只有所有必需检查通过后，才能合并

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

