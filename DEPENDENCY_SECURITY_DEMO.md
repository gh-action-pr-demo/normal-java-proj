---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## GitHub Dependabot 依赖安全检查配置演示
drawings:
  persist: false
transition: slide-left
title: GitHub Dependabot 依赖安全检查
mdc: true
marp: true
---

# 1. 背景

## 问题
如何确保项目依赖的安全性? 漏洞检测

## 预期
- 自动检测依赖漏洞
- PR 级别实时检查
- 灵活控制检查流程
- 自动创建修复 PR

---

# 2. 备选方案

---

## 2.1 自定义规则 + ghaction

- 不好维护 ❌
- 支持黑白名单 ✅

## 2.2 mvn插件 + ghaction

- owasp 漏洞检测插件 
  * 公共服务有限流 ❌
  * 需要申请 api-key 
- 可以提示出要升级到的目标版本 ✅
 
---

## 2.3 dependabot + dependency-review-action

### ✅ 优点
- PR 级别实时检查
- 详细的漏洞报告和修复建议
- 标签控制跳过检查
- Dependabot 自动创建修复 PR
- 配置简单，易于维护

### ❌ 缺点
- 需要手动配置 workflow
- 不能给出要升级的目标版本

---
## 2.3.1 实现效果

1. **触发条件**
   - PR 创建/更新
   - 添加/移除标签

2. **检查流程**
   - 检查是否有 `dependency-check-ignore` 标签
   - 有标签 → 跳过检查，创建成功 Check
   - 无标签 → 执行依赖检查

3. **结果处理**
   - 有漏洞 → 创建失败 Check + 详细报告评论
   - 无漏洞 → 创建成功 Check + 无漏洞评论

---
# 3. 如何配置
---

## 3.1 dependency-review-action

- 实现PR生效
- 实现标签控制开关
- comment 里输出报告

```yaml
# .github/workflows/dependency-review.yml
on:
  pull_request:
    types: [opened, synchronize, reopened]
  issues:
    types: [labeled, unlabeled]

jobs:
  dependency-review:
    steps:
      - uses: actions/dependency-review-action@v4
      - # 检查标签并创建评论
```
---

## 3.2 dependabot

- 自动检查和创建升级 PR, `必须合并到master/main 分支`
- 定时执行

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "maven"
    schedule:
      interval: "weekly"
    groups:
      spring-boot-dependencies: //pr 分组
        patterns:
          - "org.springframework.boot:*"
        update-types:
          - "minor"
          - "patch"
```
---
 # 4. ghaction 实现原理
---

## 4.1 GitHub Dependabot 实现原理

1. **依赖图生成**
   - GitHub 自动扫描仓库，生成依赖关系图，存储在 GitHub 数据库中
   - 集成多个安全数据库CVE、GHSA 等
   - 实时更新漏洞信息
2. **自动检测**
   - 对比依赖版本和漏洞数据库 - 发现匹配的漏洞 - 创建 Dependabot Alert
3. **自动修复**
   - 查找修复版本 - 创建修复 PR - 自动更新依赖(手动 approve)
---

## 4.1.1 Dependabot faq

- 必须在 `master` 分支才能生效, 自动创建 PR是以 master 分支为准的

- 同一个依赖只会创建 1 个 PR, `open-pull-requests-limit`限制 pr数量

- PR 合并期间, 有更新的依赖会自动修改该 pr

- 开发分支修复后合并到`master`, 下次检查时会关闭该 pr

---


## 4.2 GitHub Dependency Review 实现原理

### Dependency Graph API
- 比较两个 commit 之间的依赖变化
- 返回新增/删除的依赖
- 返回版本变更和关联的漏洞信息
- 返回修复版本建议

**限制**
- 默认只显示新引入的漏洞
- 需要 `security-events: read` 权限

---

# 5. demo

- 自动检查并输出检测报告
- 添加标签跳过检查
  * 下次 push 才能触发

---
# 6. todo

- GT 上百个工程的配置分发问题

- 跳过检查（已实现） vs  强制检查

  - **精细化控制**: 必须强制升级某个依赖

- 组织级漏洞统计、升级动作执行情况报告

---


## end
