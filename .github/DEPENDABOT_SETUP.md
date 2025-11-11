# Dependabot 自动修复安全漏洞配置指南

## 启用 Dependabot Security Updates

GitHub 的 Dependabot 可以自动创建 PR 来修复安全漏洞。要启用此功能，请按以下步骤操作：

### 1. 在仓库设置中启用 Dependabot Security Updates

1. 进入仓库的 **Settings** 页面
2. 点击左侧菜单的 **Security**
3. 在 **Code security and analysis** 部分，找到 **Dependabot alerts**
4. 点击 **Enable** 启用 Dependabot alerts
5. 在 **Dependabot security updates** 部分，点击 **Enable** 启用自动安全更新

启用后，Dependabot 会：
- 自动检测依赖中的安全漏洞
- 自动创建 PR 来修复这些漏洞
- PR 中包含建议的修复版本

### 2. 配置说明

当前仓库已配置 `.github/dependabot.yml`，包含以下设置：

- **Maven 依赖检查**：每周检查一次
- **GitHub Actions 检查**：每周检查一次
- **PR 限制**：最多同时打开 10 个 Maven 相关的 PR，5 个 Actions 相关的 PR
- **提交消息格式**：使用 `fix` 前缀

### 3. 手动触发检查

如果需要立即检查依赖更新，可以：

1. 进入仓库的 **Security** → **Dependabot** 页面
2. 点击 **Check for updates** 按钮

### 4. 自动修复工作流

仓库中还配置了 `.github/workflows/auto-fix-vulnerabilities.yml`，这是一个自定义的自动修复工作流：

- **触发方式**：
  - 每天 UTC 时间 2:00 自动运行
  - 可以手动在 Actions 页面触发（workflow_dispatch）
  
- **功能**：
  - 获取所有开放的 Dependabot alerts
  - 自动更新 pom.xml 中的漏洞依赖版本
  - 创建修复 PR

**注意**：此工作流需要访问 Dependabot alerts API，可能需要额外的权限配置。

### 5. 查看漏洞报告

当检测到安全漏洞时：

1. **在 PR 评论中**：会显示指向详细报告的链接
2. **在 Actions summary 中**：`dependency-review-action` 会显示完整的漏洞详情，包括修复版本建议
3. **在 Security 页面**：可以查看所有 Dependabot alerts

### 6. 修复版本建议

修复版本信息会在以下位置显示：

- **Actions summary 页面**：`dependency-review-action` 的输出中包含每个漏洞的 `Patched Version`
- **Dependabot 创建的 PR**：PR 描述中会包含建议的升级版本
- **Security 页面**：每个 alert 都会显示建议的修复版本

