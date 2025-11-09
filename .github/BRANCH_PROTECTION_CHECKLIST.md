# 分支保护规则配置检查清单

使用此清单快速验证分支保护规则是否正确配置。

## ✅ 配置检查清单

### 1. 基本设置
- [ ] 已进入 **Settings → Branches**
- [ ] 已添加分支保护规则（针对 `main` 或 `master` 分支）
- [ ] 分支名称模式正确（`main` 或 `master`）

### 2. 必需的状态检查（**最关键**）
- [ ] ✅ **已勾选** "Require status checks to pass before merging"
- [ ] ✅ **已勾选** "Require branches to be up to date before merging"
- [ ] ✅ **已添加** 状态检查：`Dependency Security Check / OWASP Dependency Check`
- [ ] 状态检查名称完全匹配（包括大小写和空格）

### 3. 其他推荐设置
- [ ] ✅ **已勾选** "Do not allow bypassing the above settings"（强烈建议）
- [ ] （可选）已配置 PR 审查要求
- [ ] （可选）已配置对话解决要求

### 4. 保存设置
- [ ] 已点击 **Create** 或 **Save changes** 保存设置

## 🔍 验证配置

### 步骤 1：创建测试 PR
- [ ] 创建一个测试 PR（或使用现有的 PR）
- [ ] 等待 workflow 开始运行

### 步骤 2：检查 PR 页面
- [ ] 在 PR 页面的检查部分，能看到 "Dependency Security Check / OWASP Dependency Check"
- [ ] 状态检查显示 "Required" 标签
- [ ] 在 Actions 运行期间，**Merge pull request** 按钮是禁用状态（灰色）
- [ ] 无法点击 **Merge pull request** 按钮

### 步骤 3：测试失败场景（可选）
- [ ] 如果 Actions 失败，**Merge pull request** 按钮仍然是禁用状态
- [ ] 显示错误提示（如 "Required status check failed"）

### 步骤 4：测试成功场景
- [ ] 当所有检查通过后，**Merge pull request** 按钮变为可点击状态
- [ ] 显示 "All checks have passed"

## ❌ 如果配置不正确

如果 **Merge pull request** 按钮在 Actions 运行期间或失败后仍然可以点击，请检查：

1. **是否勾选了 "Require status checks to pass before merging"？**
   - 这是最关键的设置，必须勾选

2. **状态检查名称是否正确？**
   - 格式：`Dependency Security Check / OWASP Dependency Check`
   - 必须完全匹配，包括大小写和空格
   - 如果找不到，先让 workflow 运行一次

3. **workflow 是否已运行过？**
   - 首次配置时，需要先让 workflow 运行一次
   - GitHub 才能识别状态检查

4. **分支名称是否匹配？**
   - 确保分支保护规则的分支名称模式匹配你的主分支

5. **是否允许绕过保护规则？**
   - 确保勾选了 "Do not allow bypassing the above settings"

## 📚 需要帮助？

如果仍然无法解决问题，请参考：
- [详细配置指南](BRANCH_PROTECTION_SETUP.md)
- [常见问题解答](BRANCH_PROTECTION_SETUP.md#常见问题)

