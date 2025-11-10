# GitHub Actions 被禁用问题解决方案

## 问题描述

如果看到错误信息：
```
GitHub Actions hosted runners are disabled for this repository. 
For more information please contact your GitHub Enterprise Administrator.
```

这表示你的 GitHub Enterprise 组织中，GitHub Actions 的托管运行器（hosted runners）被禁用了。

## 原因

这是组织级别的配置，不是个人权限问题。可能的原因：
1. 组织管理员禁用了 GitHub Actions
2. 组织策略要求使用自托管运行器（self-hosted runners）
3. 组织有安全策略限制使用托管运行器

## 解决方案

### 方案 1：联系组织管理员启用 Actions（推荐）

1. **联系你的 GitHub Enterprise 管理员**
2. **请求启用 GitHub Actions**：
   - 说明需要启用 Actions 的原因（依赖安全检查）
   - 如果组织有安全策略，询问是否可以例外
   - 或者询问是否可以使用自托管运行器

3. **管理员需要做的操作**：
   - 进入组织设置：**Settings → Actions → General**
   - 启用 "Allow all actions and reusable workflows"
   - 或者配置允许的 actions 列表

### 方案 2：使用自托管运行器

如果组织要求使用自托管运行器：

1. **设置自托管运行器**：
   - 在组织或仓库级别配置自托管运行器
   - 参考：[GitHub 自托管运行器文档](https://docs.github.com/en/actions/hosting-your-own-runners)

2. **修改 workflow 文件**：
   ```yaml
   jobs:
     dependency-check:
       runs-on: self-hosted  # 改为自托管运行器
   ```

### 方案 3：使用 Pre-commit Hook（临时方案）

如果无法使用 GitHub Actions，可以使用 Git pre-commit hook 在本地进行检查：

1. **创建 pre-commit hook**：
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash
   mvn verify -DskipTests
   if [ $? -ne 0 ]; then
     echo "❌ 依赖安全检查失败，请修复后再提交"
     exit 1
   fi
   ```

2. **安装 pre-commit 工具**（可选）：
   - 使用 [pre-commit](https://pre-commit.com/) 框架
   - 可以统一管理多个 hooks

### 方案 4：使用 CI/CD 集成（如果组织有）

如果你的组织使用其他 CI/CD 系统（如 Jenkins、GitLab CI、Azure DevOps）：

1. **迁移 workflow 到其他 CI/CD 系统**
2. **配置相应的 pipeline**
3. **设置状态检查集成**

## 推荐的沟通模板

联系管理员时可以使用以下模板：

```
主题：请求启用 GitHub Actions 用于依赖安全检查

您好，

我在项目 [项目名称] 中需要启用 GitHub Actions 来运行依赖安全检查。

背景：
- 我们使用 OWASP Dependency-Check 来扫描依赖中的安全漏洞
- 需要在 PR 时自动检查，防止高风险依赖被合并
- 这是安全最佳实践

请求：
1. 启用 GitHub Actions 托管运行器
2. 或者提供自托管运行器的配置指导

如果需要，我可以提供：
- 详细的 workflow 配置
- 安全检查的说明文档
- 其他相关信息

谢谢！
```

## 临时解决方案：本地检查脚本

在 Actions 启用之前，可以使用本地检查脚本：

### 创建检查脚本

```bash
#!/bin/bash
# scripts/check-dependencies.sh

echo "🔍 运行依赖安全检查..."
mvn verify -DskipTests

if [ $? -eq 0 ]; then
    echo "✅ 依赖安全检查通过"
    exit 0
else
    echo "❌ 依赖安全检查失败"
    echo "请查看报告: target/dependency-check-reports/dependency-check-report.html"
    exit 1
fi
```

### 使用方式

```bash
# 在提交 PR 前运行
./scripts/check-dependencies.sh

# 或者在 pre-commit hook 中调用
```

## 下一步

1. **立即行动**：联系 GitHub Enterprise 管理员
2. **临时方案**：使用本地检查脚本
3. **长期方案**：根据组织政策选择合适方案（托管运行器/自托管运行器/其他 CI/CD）

## 参考资源

- [GitHub Actions 权限文档](https://docs.github.com/en/enterprise-cloud@latest/admin/policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise)
- [自托管运行器文档](https://docs.github.com/en/actions/hosting-your-own-runners)
- [组织 Actions 设置](https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)


