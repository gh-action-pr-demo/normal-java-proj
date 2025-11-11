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
 - `.github/dependabot-rules.yml`：外置的 allow/ignore 规则（白名单/黑名单）
 - `.github/workflows/sync-dependabot-rules.yml`：规则同步工作流，自动合并到 `.github/dependabot.yml`
 - `.github/allow-deps.txt` / `.github/ignore-deps.txt`：纯文本白名单/黑名单（一行一个依赖）

## 自定义
- 在 `.github/dependabot.yml` 中可配置 `schedule`、`labels`、`open-pull-requests-limit` 等
- 已将 `interval` 设为 `daily`，如需临时立即触发，可对 `.github/dependabot.yml` 做小改动并推送

## 跳过依赖变更审查（评论关键字）
在 PR 中评论以下任意关键字（不区分大小写），本次检查将被跳过并自动回评提示：
- `[skip dependency check]`
- `[skip-dependency-check]`
- `[skip dependency-check]`
- `[skip-dependency check]`

## 规则配置示例（按需复制到 `.github/dependabot.yml`）
以下示例展示如何“跳过某些依赖的更新”或“只强制更新某些依赖”。将示例片段放到对应 `package-ecosystem` 的条目下。

```yaml
updates:
  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "daily"
      time: "02:00"
      timezone: "Asia/Shanghai"
    # 跳过某些依赖的特定类型更新（示例：忽略 log4j 的主版本升级）
    ignore:
      - dependency-name: "log4j:log4j"
        update-types: ["version-update:semver-major"]
      - dependency-name: "com.fasterxml.jackson.core:jackson-databind"
        update-types: ["version-update:semver-minor"]
    # 只允许某些依赖被更新（强制聚焦某些包；不配置则默认允许全部）
    # 使用后将只对这些依赖创建 PR
    # allow:
    #   - dependency-name: "com.fasterxml.jackson.core:jackson-databind"
    #   - dependency-name: "org.springframework.boot:spring-boot-starter-web"
```

提示：
- ignore 与 allow 可同时使用；allow 会“收窄范围”，仅更新列出的依赖
- 也可以使用 PR 评论命令协助处理（在 Dependabot PR 中评论）：
  - `@dependabot rebase` 重新基于最新分支
  - `@dependabot recreate` 重新创建 PR
  - `@dependabot merge` / `@dependabot squash and merge` 直接合并（需权限与设置允许）
  - `@dependabot ignore this major|minor|patch` 忽略当前版本线

## 使用外置规则文件进行管理（推荐）
我们已引入 `.github/dependabot-rules.yml` 来集中管理 allow/ignore：
- 按 ecosystem（`maven`/`gradle`/`github-actions`）分别维护列表
- 提交该文件后，`Sync Dependabot Rules` 工作流会自动把规则写入 `.github/dependabot.yml`
- 若某个 ecosystem 在规则文件中是空列表，表示不设置该项，保留现状；若希望清空，显式写成空列表即可

触发方式：
1. 直接编辑 `.github/dependabot-rules.yml` 并推送 → 自动同步生成新的 `.github/dependabot.yml` 提交
2. 也可手动运行 `Sync Dependabot Rules` 工作流进行同步

### 使用纯文本黑白名单（更简单）
- 文件：`.github/allow-deps.txt`（强制更新白名单），`.github/ignore-deps.txt`（跳过更新黑名单）
- 写法：每行一个依赖，默认 maven，可加前缀指定生态：
  - `maven:groupId:artifactId`
  - `gradle:group:artifact`
  - `github-actions:owner/action`
  - 无前缀默认视为 `maven:...`
- 推送后工作流会自动同步到 `.github/dependabot.yml` 对应的 `allow` / `ignore` 字段

示例（allow-deps.txt）：
```
maven:com.fasterxml.jackson.core:jackson-databind
maven:com.google.guava:guava
```

示例（ignore-deps.txt）：
```
maven:log4j:log4j
maven:commons-io:commons-io
```

规则文件模板（片段）：
```yaml
ignore:
  maven:
    - dependency-name: "groupId:artifactId"
      update-types: ["version-update:semver-major"]
  gradle: []
  github-actions: []

allow:
  maven:
    - dependency-name: "groupId:artifactId"
  gradle: []
  github-actions: []
```

## 分支保护与必需检查（Dependency Review）
- 若 PR 的目标分支受分支保护并要求“Dependency Review / dependency-review (pull_request)”为必需检查：  
  - 默认会自动执行依赖变更审查  
  - 若评论包含“跳过关键字”，工作流会成功结束，从而满足必需检查要求
- 若要在“当前测试分支”完全不要求该检查：  
  - 到 Settings → Branches 新建一个“更具体匹配当前分支名”的保护规则且不勾选该必需检查；GitHub 会优先使用更具体的规则  
  - 或者临时在主分支保护规则中取消此必需检查（不推荐长期这样）

## 说明
- 已移除旧的 OWASP Dependency-Check 工作流、脚本与 suppression 配置；`pom.xml` 中也去除了相关插件
- 如需恢复本地扫描或组织级统一方案，可在其他分支保留相应文件

## 许可证
MIT License