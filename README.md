# Dependabot 依赖安全与自动更新（测试分支）

本分支用于验证 GitHub Dependabot 在 Maven/Gradle 项目中的自动化依赖安全与版本更新能力，并配合 PR 级别的 Dependency Review 做安全拦截。

## 功能
- 自动创建依赖更新 PR（Maven、Gradle、GitHub Actions）
- PR 中自动执行依赖变更审查（高危及以上直接失败并评论摘要）
- 可选：对 Dependabot 的补丁级（semver patch）更新自动合并

## 快速开始
1) 在仓库 Settings → Security → Code security and analysis 开启：
   - Dependabot alerts
   - Dependabot security updates（建议）
2) 在 Actions 页面选择 “Dependency Review” → Run workflow，可随时手动运行校验
3) 立刻触发 Dependabot 更新检查：
   - 轻微修改 `.github/dependabot.yml` 并推送到默认分支（会立即触发一次扫描并创建/更新 PR）
   - 或将 `interval` 设置为 `daily`（Dependabot 不支持小时级）

## 关键文件
- `.github/dependabot.yml`：Dependabot 配置（Maven/Gradle/Actions，Asia/Shanghai 每周一 02:00）
- `.github/workflows/dependency-review.yml`：依赖变更审查（支持手动触发）
- `.github/workflows/dependabot-auto-merge.yml`：补丁级更新自动合并（需仓库开启 Auto-merge）

## 自定义
- 在 `.github/dependabot.yml` 中可配置 `schedule`、`labels`、`open-pull-requests-limit` 等
- 已将 `interval` 设为 `daily`，如需临时立即触发，可对 `.github/dependabot.yml` 做小改动并推送

## 跳过依赖变更审查（评论关键字）
在 PR 中评论以下任意关键字（不区分大小写），本次检查将被跳过并自动回评提示：
- `[skip dependency check]`
- `[skip-dependency-check]`
- `[skip dependency-check]`
- `[skip-dependency check]`

## 说明
- 已移除旧的 OWASP Dependency-Check 工作流、脚本与 suppression 配置；`pom.xml` 中也去除了相关插件
- 如需恢复本地扫描或组织级统一方案，可在其他分支保留相应文件

## 许可证
MIT License